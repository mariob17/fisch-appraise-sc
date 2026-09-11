"""
Manajemen konfigurasi dengan file JSON
"""

import json
import os

CONFIG_FILE = "appraiser_config.json"

class ConfigManager:
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.data = self.load()
    
    def load(self):
        """Load konfigurasi dari file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_config()
        return self._default_config()
    
    def _default_config(self):
        """Konfigurasi default"""
        return {
            "mutations": ["Mythical", "Abyssal", "Greedy", "Shiny", "Sparkling"],
            "roi": None,
            "interval": 0.5,
            "version": "1.0"
        }
    
    def save(self):
        """Simpan konfigurasi ke file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Config] Save error: {e}")
            return False
    
    # ========== MUTASI ==========
    def get_mutations(self):
        return self.data.get('mutations', [])
    
    def add_mutation(self, name):
        name = name.strip()
        if name and name not in self.data['mutations']:
            self.data['mutations'].append(name)
            self.save()
            return True
        return False
    
    def edit_mutation(self, old_name, new_name):
        old_name = old_name.strip()
        new_name = new_name.strip()
        if old_name in self.data['mutations'] and new_name:
            idx = self.data['mutations'].index(old_name)
            self.data['mutations'][idx] = new_name
            self.save()
            return True
        return False
    
    def delete_mutation(self, name):
        name = name.strip()
        if name in self.data['mutations']:
            self.data['mutations'].remove(name)
            self.save()
            return True
        return False
    
    # ========== ROI ==========
    def get_roi(self):
        return self.data.get('roi')
    
    def save_roi(self, roi):
        if roi and len(roi) == 4:
            self.data['roi'] = list(roi)
            self.save()
            return True
        return False
    
    # ========== INTERVAL ==========
    def get_interval(self):
        return self.data.get('interval', 0.5)
    
    def save_interval(self, interval):
        self.data['interval'] = float(interval)
        self.save()
        return True