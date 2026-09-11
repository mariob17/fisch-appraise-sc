"""
Auto Appraiser Bot - VERSI INSTAN STOP
"""

import pyautogui
import time
import threading
from ocr_engine import OCRDetector

class AutoAppraiser:
    def __init__(self):
        self.ocr = OCRDetector()
        self.is_running = False
        self.stop_event = threading.Event()
        self.target_mutation = ""
        self.click_interval = 0.5
        self.on_mutation_found = None
        self._thread = None
        self._click_count = 0
        self._detected_list = []
        
    def start(self, target_mutation, interval=0.5):
        if self.is_running:
            return
        
        self.target_mutation = target_mutation.lower().strip()
        self.click_interval = interval
        self.is_running = True
        self.stop_event.clear()
        self._click_count = 0
        self._detected_list = []
        
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print(f"[Bot] Started, target: '{self.target_mutation}'")
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            print(f"[Bot] Stopped, total clicks: {self._click_count}")
    
    def _run(self):
        print("[Bot] Loop started")
        
        # ========== DETEKSI AWAL ==========
        print("[Bot] Deteksi awal...")
        initial_detection = self.ocr.detect_text().lower().strip()
        if initial_detection and self.target_mutation in initial_detection:
            print(f"[Bot] ✅ TARGET SUDAH ADA: '{initial_detection}'")
            self.is_running = False
            if self.on_mutation_found:
                self.on_mutation_found(initial_detection)
            return
        
        # ========== LOOP UTAMA ==========
        while self.is_running and not self.stop_event.is_set():
            # 0. CEK SEBELUM KLIK: deteksi cepat untuk menghindari klik ekstra
            try:
                pre_detect = self.ocr.detect_text_fast().lower().strip()
            except Exception:
                pre_detect = ""

            if pre_detect and self.target_mutation in pre_detect:
                print(f"[Bot] ✅ TARGET FOUND (pre-click): '{pre_detect}'")
                self.is_running = False
                self.stop_event.set()
                if self.on_mutation_found:
                    try:
                        self.on_mutation_found(pre_detect)
                    except Exception as e:
                        print(f"[Bot] Callback error: {e}")
                break

            # 1. KLIK
            try:
                pyautogui.click()
                self._click_count += 1
                print(f"[Bot] Click #{self._click_count}")
            except Exception as e:
                print(f"[Bot] Click error: {e}")
                break

            # 2. TUNGGU MINIMAL (0.1 detik cukup)
            time.sleep(0.1)

            # 3. DETEKSI SETELAH KLIK
            detected = self.ocr.detect_text().lower().strip()

            # 4. LOG
            if detected:
                self._detected_list.append(detected)
                print(f"[Bot] Detected: '{detected}'")

            # 5. CEK TARGET - LANGSUNG STOP!
            if detected and self.target_mutation in detected:
                print(f"[Bot] ✅ TARGET FOUND: '{detected}'")
                self.is_running = False
                self.stop_event.set()
                if self.on_mutation_found:
                    try:
                        self.on_mutation_found(detected)
                    except Exception as e:
                        print(f"[Bot] Callback error: {e}")
                break

            # 6. TUNGGU INTERVAL
            # PERBAIKAN: Gunakan polling singkat agar stop lebih responsif
            for _ in range(int(self.click_interval * 10)):
                if not self.is_running or self.stop_event.is_set():
                    break
                time.sleep(0.1)
                time.sleep(0.1)
        
        # Pastikan status berhenti
        self.is_running = False
        print("[Bot] Loop ended")
    
    def get_stats(self):
        return {
            "is_running": self.is_running,
            "total_clicks": self._click_count,
            "target": self.target_mutation,
            "last_detected": self.ocr.last_detection,
            "detection_count": len(self._detected_list)
        }