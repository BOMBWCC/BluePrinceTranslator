import json
import os
from thefuzz import fuzz, process
from src.config.settings import settings

class Translator:
    def __init__(self):
        self.db_path = settings.get("translation_db_path", "data/translation_db.json")
        self.db = {}
        self.load_db()

    def load_db(self):
        # Update path from settings in case it changed
        self.db_path = settings.get("translation_db_path", "data/translation_db.json")
        
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.db = json.load(f)
                print(f"[DEBUG] Translation DB loaded: {len(self.db)} entries from {self.db_path}")
            except Exception as e:
                print(f"Error loading translation DB: {e}")
                self.db = {}
        else:
            print(f"Translation DB not found: {self.db_path}")
            self.db = {}

    def reload_db(self):
        """Public method to force reload of the database"""
        print("[DEBUG] Reloading translation database...")
        self.load_db()

    def translate(self, text):
        """
        根据 OCR 识别的文本进行匹配
        """
        if not text or not self.db:
            return None

        # Clean text (remove extra newlines/spaces)
        cleaned_text = text.replace("\n", " ").strip()
        
        # 1. Exact match
        if cleaned_text in self.db:
            return self.db[cleaned_text]

        # 2. Fuzzy match
        # keys = list(self.db.keys())
        # best_match, score = process.extractOne(cleaned_text, keys, scorer=fuzz.token_sort_ratio)
        
        # Alternative: iterate and find best match to handle multiline or partial matches better
        best_score = 0
        best_translation = None
        threshold = settings.get("matching_threshold", 85)

        for original, translated in self.db.items():
            # Use ratio or token_sort_ratio
            score = fuzz.token_sort_ratio(cleaned_text, original)
            if score > best_score:
                best_score = score
                best_translation = translated

        if best_score >= threshold:
            return best_translation
        
        return None

translator_service = Translator()
