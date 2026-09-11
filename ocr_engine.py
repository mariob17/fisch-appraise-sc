"""
OCR Engine menggunakan RapidOCR
Ringan, akurat, cross-platform - VERSI OPTIMASI
"""

from rapidocr_onnxruntime import RapidOCR
from PIL import Image
import mss
import time
import numpy as np

class OCRDetector:
    def __init__(self):
        # OPTIMASI: Gunakan model dengan parameter lebih ringan
        self.engine = RapidOCR(
            use_angle_cls=False,  # Nonaktifkan deteksi sudut (lebih cepat)
            use_gpu=False,        # Gunakan CPU (lebih stabil)
        )
        self.roi = None  # (x, y, width, height)
        self.last_detection = ""
        self.detection_time = 0
        self._initialized = True
        
        # OPTIMASI: Cache untuk gambar terakhir
        self._last_img_hash = None
        self._cached_result = ""
        
    def set_roi(self, x, y, w, h):
        """Set area deteksi (Region of Interest)"""
        if w > 0 and h > 0:
            self.roi = (x, y, w, h)
            return True
        return False
    
    def capture_roi(self):
        """Tangkap area ROI dari layar menggunakan mss"""
        if not self.roi:
            return None
        x, y, w, h = self.roi
        try:
            with mss.mss() as sct:
                monitor = {"top": y, "left": x, "width": w, "height": h}
                img = sct.grab(monitor)
                # Konversi ke PIL Image
                return Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        except Exception as e:
            print(f"[OCR] Error capture: {e}")
            return None
    
    def detect_text(self):
        """
        Deteksi teks dari area ROI
        Return: string teks yang terdeteksi, atau string kosong
        """
        if not self.roi:
            return ""
        
        img = self.capture_roi()
        if img is None:
            return ""
        
        # OPTIMASI 1: Resize gambar jika terlalu besar (percepat OCR)
        # Area deteksi biasanya hanya ~200x50 pixel, ini cukup
        if img.width > 400 or img.height > 150:
            # Resize dengan rasio yang menjaga kualitas
            ratio = min(400 / img.width, 150 / img.height, 1.0)
            if ratio < 1.0:
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # OPTIMASI 2: Konversi ke grayscale untuk mempercepat
        # (RapidOCR sudah handle ini, tapi kita bisa bantu)
        if img.mode != 'L':
            img = img.convert('L')
        
        # OPTIMASI 3: Tingkatkan kontras untuk OCR lebih akurat
        # (opsional, bisa diaktifkan jika teks kurang jelas)
        # from PIL import ImageEnhance
        # enhancer = ImageEnhance.Contrast(img)
        # img = enhancer.enhance(1.5)
        
        try:
            # RapidOCR detection
            result = self.engine(img)
            
            # Format: [[[koordinat], text, confidence], ...]
            if result and result[0]:
                # Gabungkan semua teks
                texts = [item[1] for item in result[0]]
                detected = " ".join(texts).strip()
                self.last_detection = detected
                self.detection_time = time.time()
                return detected
            return ""
        except Exception as e:
            print(f"[OCR] Error detect: {e}")
            return ""
    
    def detect_text_with_confidence(self):
        """
        Deteksi teks dengan confidence score
        Return: (text, confidence) atau ("", 0)
        """
        if not self.roi:
            return "", 0
        
        img = self.capture_roi()
        if img is None:
            return "", 0
        
        # OPTIMASI: Resize jika perlu
        if img.width > 400 or img.height > 150:
            ratio = min(400 / img.width, 150 / img.height, 1.0)
            if ratio < 1.0:
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        try:
            result = self.engine(img)
            if result and result[0]:
                # Ambil teks dengan confidence tertinggi
                best = max(result[0], key=lambda x: x[2])
                return best[1], best[2]
            return "", 0
        except Exception as e:
            print(f"[OCR] Error: {e}")
            return "", 0
    
    def detect_text_fast(self):
        """
        Deteksi teks dengan kecepatan maksimum (trade-off akurasi)
        Hanya untuk kondisi teks yang sangat jelas
        """
        if not self.roi:
            return ""
        
        img = self.capture_roi()
        if img is None:
            return ""
        
        # Resize lebih agresif untuk kecepatan
        if img.width > 200 or img.height > 80:
            ratio = min(200 / img.width, 80 / img.height, 1.0)
            if ratio < 1.0:
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Konversi ke grayscale
        if img.mode != 'L':
            img = img.convert('L')
        
        try:
            result = self.engine(img)
            if result and result[0]:
                texts = [item[1] for item in result[0]]
                detected = " ".join(texts).strip()
                self.last_detection = detected
                self.detection_time = time.time()
                return detected
            return ""
        except Exception as e:
            print(f"[OCR] Error: {e}")
            return ""