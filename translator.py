"""🌍 SARVAM-TRANSLATE via Local API"""
import requests

SARVAM_LANGUAGES = ["Hindi", "Bengali", "Tamil", "Telugu", "Malayalam", "Kannada", "Marathi", "Gujarati", "Odia", "Punjabi", "Assamese", "Urdu", "Maithili", "Sanskrit", "Konkani", "Nepali", "Sindhi", "Dogri", "Manipuri", "Bodo", "Kashmiri", "Santali"]

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
        try:
            import streamlit as st
            self.api_url = st.secrets.get("local_api", {}).get("sarvam_url", "")
        except:
            self.api_url = ""
        self.stats = {"sarvam": 0, "fallback": 0}
        print(f"🌍 Sarvam: {'✅' if self.api_url else '❌'}")
    
    def translate_sarvam(self, text, target_language):
        if not self.api_url or target_language not in SARVAM_LANGUAGES:
            return None
        try:
            response = requests.post(f"{self.api_url}/translate", json={"text": text, "target_language": target_language}, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.stats["sarvam"] += 1
                    return result.get('translation', '').strip()
        except: pass
        return None
    
    def translate_fallback(self, text, target_language):
        words = {"hello": {"Hindi": "नमस्ते"}, "potato": {"Hindi": "आलू"}}
        if text.lower() in words and target_language in words[text.lower()]:
            self.stats["fallback"] += 1
            return words[text.lower()][target_language]
        return None
    
    def translate(self, text, target_language):
        text = text.strip()
        if not text: return "", "none"
        result = self.translate_sarvam(text, target_language)
        if result: return result, "sarvam"
        result = self.translate_fallback(text, target_language)
        if result: return result, "fallback"
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        return f"Sarvam: {self.stats['sarvam']} | Fallback: {self.stats['fallback']}" if total else "No translations yet"

_translator = None
def get_translator(sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key, huggingface_token, gemini_api_key)
    return _translator
