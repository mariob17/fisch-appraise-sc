"""
ROI Selector - Overlay untuk memilih area deteksi
"""

import tkinter as tk

class ROISelector:
    def __init__(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        # Buat window overlay transparan fullscreen
        self.window = tk.Toplevel(parent)
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-alpha', 0.25)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='black')
        self.window.focus_set()
        
        # Canvas untuk menggambar
        self.canvas = tk.Canvas(self.window, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Binding mouse
        self.window.bind('<ButtonPress-1>', self.on_mouse_down)
        self.window.bind('<B1-Motion>', self.on_mouse_move)
        self.window.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.window.bind('<Escape>', self.cancel)
        self.window.bind('<KeyPress-Escape>', self.cancel)
        
        # Instruksi
        screen_w = self.window.winfo_screenwidth()
        self.canvas.create_text(
            screen_w // 2, 40,
            text="🔍 KLIK & DRAG untuk memilih area deteksi teks mutasi",
            fill="white", font=("Arial", 18, "bold")
        )
        self.canvas.create_text(
            screen_w // 2, 75,
            text="Tekan ESC untuk batal",
            fill="white", font=("Arial", 12)
        )
        
        # Koordinat live
        self.coord_text = self.canvas.create_text(
            20, self.window.winfo_screenheight() - 30,
            text="", fill="white", font=("Arial", 10), anchor="sw"
        )
    
    def on_mouse_down(self, event):
        self.start_x = self.window.winfo_pointerx()
        self.start_y = self.window.winfo_pointery()
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_mouse_move(self, event):
        if self.start_x is None:
            return
        end_x = self.window.winfo_pointerx()
        end_y = self.window.winfo_pointery()
        
        if self.rect:
            self.canvas.delete(self.rect)
        
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, end_x, end_y,
            outline='red', width=3, fill='red', stipple='gray50'
        )
        
        # Update koordinat
        w = abs(end_x - self.start_x)
        h = abs(end_y - self.start_y)
        x = min(self.start_x, end_x)
        y = min(self.start_y, end_y)
        self.canvas.itemconfig(self.coord_text, text=f"Area: {x}, {y} | {w} x {h}")
        self.canvas.tag_raise(self.coord_text)
    
    def on_mouse_up(self, event):
        if self.start_x is None:
            return
        
        end_x = self.window.winfo_pointerx()
        end_y = self.window.winfo_pointery()
        
        # Pastikan area valid
        if abs(end_x - self.start_x) < 10 or abs(end_y - self.start_y) < 10:
            self.window.destroy()
            return
        
        x1, x2 = min(self.start_x, end_x), max(self.start_x, end_x)
        y1, y2 = min(self.start_y, end_y), max(self.start_y, end_y)
        roi = (x1, y1, x2 - x1, y2 - y1)
        
        self.window.destroy()
        self.on_complete(roi)
    
    def cancel(self, event=None):
        self.window.destroy()