"""
Global Hotkey Handler menggunakan pynput
F6 = Start, F7 = Stop
"""

from pynput import keyboard

class HotkeyHandler:
    def __init__(self, on_start, on_stop):
        self.on_start = on_start
        self.on_stop = on_stop
        self.listener = None
        self.is_running = False
    
    def start(self):
        """Mulai listener hotkey"""
        if self.is_running:
            return
        
        def on_press(key):
            try:
                if key == keyboard.Key.f6:
                    print("[Hotkey] F6 pressed -> Start")
                    self.on_start()
                elif key == keyboard.Key.f7:
                    print("[Hotkey] F7 pressed -> Stop")
                    self.on_stop()
            except Exception as e:
                print(f"[Hotkey] Error: {e}")
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.daemon = True
        self.listener.start()
        self.is_running = True
        print("[Hotkey] Listener started (F6=Start, F7=Stop)")
    
    def stop(self):
        """Hentikan listener"""
        if self.listener and self.is_running:
            self.listener.stop()
            self.is_running = False
            print("[Hotkey] Listener stopped")