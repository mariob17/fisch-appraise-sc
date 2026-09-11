"""
Script untuk test OCR sebelum menjalankan aplikasi utama
Gunakan untuk memastikan RapidOCR berfungsi
"""

from ocr_engine import OCRDetector
import time

def test_ocr():
    print("=" * 50)
    print("  FISCH AUTO APPRAISER - OCR TEST")
    print("=" * 50)
    print("\n🔍 Memulai OCR Engine...")
    
    ocr = OCRDetector()
    
    print("✅ OCR Engine siap")
    print("\n📝 Petunjuk:")
    print("1. Buka game Fisch")
    print("2. Arahkan ke area yang menampilkan teks mutasi")
    print("3. Di aplikasi ini, klik & drag untuk memilih area")
    print("4. Setelah area dipilih, OCR akan membaca teksnya")
    print("5. Tekan ESC untuk keluar\n")
    
    # Buka ROI selector
    import tkinter as tk
    from roi_selector import ROISelector
    
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window utama
    
    def on_roi_selected(roi):
        print(f"\n📍 Area terpilih: {roi}")
        ocr.set_roi(*roi)
        
        print("\n🔄 Deteksi teks (10x)...")
        for i in range(10):
            text = ocr.detect_text()
            if text:
                print(f"  [{i+1}] ✅ '{text}'")
            else:
                print(f"  [{i+1}] ❌ Tidak ada teks")
            time.sleep(0.5)
        
        print("\n✅ Selesai!")
        root.quit()
    
    # Buka selector
    ROISelector(root, on_roi_selected)
    root.mainloop()

if __name__ == "__main__":
    test_ocr()