"""
GUI utama aplikasi menggunakan Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import ConfigManager
from auto_clicker import AutoAppraiser
from roi_selector import ROISelector
from hotkey_handler import HotkeyHandler

class AppraiserGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fisch Auto Appraiser v1.0")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Inisialisasi
        self.config = ConfigManager()
        self.bot = AutoAppraiser()
        # Pastikan callback dijalankan di thread UI (Tkinter) untuk menghentikan segera tanpa menjalankan perintah selanjutnya
        self.bot.on_mutation_found = lambda detected_text: self.root.after(0, lambda: self.on_mutation_found(detected_text))
        
        # Setup UI
        self.setup_ui()
        self.load_config()
        
        # Hotkey
        self.hotkey = HotkeyHandler(self.start_bot, self.stop_bot)
        self.hotkey.start()
        
        # Event close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        # ============ FRAME 1: MUTASI ============
        frame_mut = ttk.LabelFrame(self.root, text="📋 Daftar Mutasi (CRUD)", padding=10)
        frame_mut.pack(fill=tk.X, padx=10, pady=5)
        
        # Listbox + Scroll
        listbox_frame = ttk.Frame(frame_mut)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(listbox_frame, height=6, font=('Arial', 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scroll.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_mutation)
        
        # Tombol CRUD
        btn_frame = ttk.Frame(frame_mut)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        ttk.Label(btn_frame, text="Nama Mutasi:").pack()
        self.entry_mut = ttk.Entry(btn_frame, width=15)
        self.entry_mut.pack(pady=2)
        
        ttk.Button(btn_frame, text="➕ Add", command=self.add_mutation, width=12).pack(pady=1)
        ttk.Button(btn_frame, text="✏️ Edit", command=self.edit_mutation, width=12).pack(pady=1)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_mutation, width=12).pack(pady=1)
        
        # ============ FRAME 2: PENGATURAN ============
        frame_settings = ttk.LabelFrame(self.root, text="⚙️ Pengaturan", padding=10)
        frame_settings.pack(fill=tk.X, padx=10, pady=5)
        
        # Interval klik
        ttk.Label(frame_settings, text="Jeda Klik (detik):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.interval_spin = ttk.Spinbox(frame_settings, from_=0.1, to=2.0, increment=0.1, width=10)
        self.interval_spin.set(0.5)
        self.interval_spin.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Tombol Select Area
        ttk.Button(frame_settings, text="🖱️ Select Area Deteksi", 
                   command=self.open_roi_selector).grid(row=0, column=2, padx=10)
        
        # Info area
        self.roi_label = ttk.Label(frame_settings, text="📍 Area: Belum diatur", foreground="gray")
        self.roi_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5, padx=5)
        
        # ============ FRAME 3: KONTROL ============
        frame_control = ttk.LabelFrame(self.root, text="🎮 Kontrol", padding=10)
        frame_control.pack(fill=tk.X, padx=10, pady=5)
        
        # Hotkey info
        ttk.Label(frame_control, text="▶️ Start: F6  |  ⏹️ Stop: F7", 
                  font=('Arial', 10, 'bold')).pack()
        
        # Target terpilih
        self.target_label = ttk.Label(frame_control, text="🎯 Target: (Pilih mutasi dari daftar)", 
                                      foreground="blue", font=('Arial', 10))
        self.target_label.pack(pady=5)
        
        # Status
        self.status_label = ttk.Label(frame_control, text="⚪ Status: Bot Stopped", 
                                      foreground="gray", font=('Arial', 9))
        self.status_label.pack(pady=5)
        
        # Tombol manual
        btn_manual = ttk.Frame(frame_control)
        btn_manual.pack(pady=5)
        ttk.Button(btn_manual, text="▶️ Start (F6)", command=self.start_bot, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_manual, text="⏹️ Stop (F7)", command=self.stop_bot, width=15).pack(side=tk.LEFT, padx=5)
        
        # Informasi tambahan
        ttk.Label(frame_control, text="💡 Arahkan mouse ke tombol 'Appraise' sebelum Start", 
                  foreground="gray", font=('Arial', 8)).pack(pady=2)
        
        # ============ FRAME 4: STATISTIK ============
        frame_stats = ttk.LabelFrame(self.root, text="📊 Statistik", padding=10)
        frame_stats.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = ttk.Label(frame_stats, text="Total Klik: 0 | Deteksi Terakhir: -", 
                                     font=('Arial', 9))
        self.stats_label.pack()
    
    # ================== FUNGSI CRUD ==================
    
    def load_config(self):
        """Load konfigurasi dari JSON"""
        data = self.config.load()
        if data:
            # Mutasi
            for mut in data.get('mutations', []):
                self.listbox.insert(tk.END, mut)
            # ROI
            roi = data.get('roi')
            if roi:
                self.roi_label.config(text=f"📍 Area: {roi}")
                self.bot.ocr.set_roi(*roi)
            # Interval
            self.interval_spin.set(data.get('interval', 0.5))
            # Pilih default
            if self.listbox.size() > 0:
                self.listbox.selection_set(0)
                self.on_select_mutation(None)
    
    def add_mutation(self):
        val = self.entry_mut.get().strip()
        if val:
            if val not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, val)
                self.config.add_mutation(val)
                self.entry_mut.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", f"Mutasi '{val}' sudah ada!")
    
    def edit_mutation(self):
        sel = self.listbox.curselection()
        if sel and self.entry_mut.get().strip():
            idx = sel[0]
            old = self.listbox.get(idx)
            new = self.entry_mut.get().strip()
            if new != old:
                self.listbox.delete(idx)
                self.listbox.insert(idx, new)
                self.config.edit_mutation(old, new)
                self.entry_mut.delete(0, tk.END)
    
    def delete_mutation(self):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            val = self.listbox.get(idx)
            if messagebox.askyesno("Konfirmasi", f"Hapus mutasi '{val}'?"):
                self.listbox.delete(idx)
                self.config.delete_mutation(val)
    
    def on_select_mutation(self, event):
        sel = self.listbox.curselection()
        if sel:
            target = self.listbox.get(sel[0])
            self.target_label.config(text=f"🎯 Target: {target}")
    
    # ================== FUNGSI ROI ==================
    
    def open_roi_selector(self):
        if self.bot.is_running:
            messagebox.showwarning("Warning", "Hentikan bot terlebih dahulu!")
            return
        ROISelector(self.root, self.on_roi_selected)
    
    def on_roi_selected(self, roi):
        self.roi_label.config(text=f"📍 Area: {roi}")
        self.bot.ocr.set_roi(*roi)
        self.config.save_roi(roi)
        messagebox.showinfo("Sukses", f"Area deteksi berhasil disimpan!\n{roi}")
    
    # ================== FUNGSI BOT ==================
    
    def start_bot(self):
        # Validasi
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Pilih mutasi tujuan dari daftar!")
            return
        if not self.bot.ocr.roi:
            messagebox.showerror("Error", "Atur area deteksi terlebih dahulu!")
            return
        
        target = self.listbox.get(sel[0])
        interval = float(self.interval_spin.get())
        
        self.bot.start(target, interval)
        self.status_label.config(text="🔴 Status: BOT BERJALAN...", foreground="red")
        self.update_stats()
    
    def stop_bot(self):
        self.bot.stop()
        self.status_label.config(text="⏹️ Status: Bot Berhenti", foreground="orange")
        self.update_stats()
    
    def on_mutation_found(self, detected_text):
        self.status_label.config(text=f"✅ Status: MUTASI DITEMUKAN!", foreground="green")
        self.update_stats()
        messagebox.showinfo("🎉 MUTATION FOUND!", 
                            f"Mutasi '{self.bot.target_mutation}' berhasil ditemukan!\n"
                            f"Teks terdeteksi: {detected_text}\n\n"
                            f"Total klik: {self.bot._click_count}\n"
                            "Bot berhenti otomatis.")
    
    def update_stats(self):
        """Update statistik di UI"""
        stats = self.bot.get_stats()
        last_detected = stats.get('last_detected', '-') or '-'
        self.stats_label.config(
            text=f"Total Klik: {stats['total_clicks']} | "
                 f"Deteksi Terakhir: {last_detected[:30]}..."
        )
        # Update setiap 1 detik jika bot berjalan
        if self.bot.is_running:
            self.root.after(1000, self.update_stats)
    
    # ================== CLOSE ==================
    
    def on_close(self):
        self.stop_bot()
        if hasattr(self, 'hotkey'):
            self.hotkey.stop()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()