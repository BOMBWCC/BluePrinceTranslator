import json
import os

class Settings:
    _instance = None
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.data = self.get_defaults()
        else:
            self.data = self.get_defaults()
            self.save()

    def get_defaults(self):
        return {
            "font_size": 18,
            "background_opacity": 0.7,
            "hotkey_translate": "alt+q",
            "hotkey_hide": "esc",
            "translation_db_path": "data/translation_db.json",
            "matching_threshold": 85,
            "window_pos": [100, 100],
            "window_size": [400, 200]
        }

    def save(self):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

# Singleton instance
settings = Settings()
