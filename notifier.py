"""
Sistem Notifikasi untuk mutasi ditemukan
"""

import tkinter as tk
from tkinter import messagebox
import threading

class Notifier:
    @staticmethod
    def show_mutation_found(mutation_name, detected_text=""):
        """Tampilkan notifikasi mutasi ditemukan"""
        title = "🎉 MUTATION FOUND!"
        message = f"Mutasi '{mutation_name}' berhasil ditemukan!"
        if detected_text:
            message += f"\n\nTeks terdeteksi: {detected_text}"
        message += "\n\nBot berhenti otomatis."
        
        try:
            root = tk._default_root
            if root:
                root.after(0, lambda: messagebox.showinfo(title, message))
            else:
                threading.Thread(target=lambda: messagebox.showinfo(title, message)).start()
        except:
            print(f"[Notifier] {title}: {message}")
    
    @staticmethod
    def show_error(message):
        """Tampilkan notifikasi error"""
        try:
            root = tk._default_root
            if root:
                root.after(0, lambda: messagebox.showerror("Error", message))
            else:
                threading.Thread(target=lambda: messagebox.showerror("Error", message)).start()
        except:
            print(f"[Notifier] Error: {message}")
    
    @staticmethod
    def show_warning(message):
        """Tampilkan notifikasi warning"""
        try:
            root = tk._default_root
            if root:
                root.after(0, lambda: messagebox.showwarning("Warning", message))
            else:
                threading.Thread(target=lambda: messagebox.showwarning("Warning", message)).start()
        except:
            print(f"[Notifier] Warning: {message}")
    
    @staticmethod
    def show_info(message):
        """Tampilkan notifikasi info"""
        try:
            root = tk._default_root
            if root:
                root.after(0, lambda: messagebox.showinfo("Info", message))
            else:
                threading.Thread(target=lambda: messagebox.showinfo("Info", message)).start()
        except:
            print(f"[Notifier] Info: {message}")