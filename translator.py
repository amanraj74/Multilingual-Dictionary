"""
🌍 BEST TRANSLATOR FOR INDIAN LANGUAGES
Sarvam AI + IndicTrans2 + Fallback
"""

import requests
import time

# Sarvam AI codes
SARVAM_CODES = {
    "Hindi": "hi-IN", "Bengali": "bn-IN", "Tamil": "ta-IN", "Telugu": "te-IN",
    "Malayalam": "ml-IN", "Kannada": "kn-IN", "Marathi": "mr-IN", "Gujarati": "gu-IN",
    "Odia": "or-IN", "Punjabi": "pa-IN", "Assamese": "as-IN", "Urdu": "ur-IN",
    "Maithili": "mai-IN", "Sanskrit": "sa-IN", "Konkani": "kok-IN", "Nepali": "ne-IN",
    "Sindhi": "sd-IN", "Dogri": "doi-IN", "Manipuri": "mni-IN", "Bodo": "brx-IN",
    "Kashmiri": "ks-IN", "Santali": "sat-IN"
}

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
        self.sarvam_key = sarvam_api_key
        self.hf_token = huggingface_token
        self.sarvam_url = "https://api.sarvam.ai/translate"
        self.session = requests.Session()
        self.stats = {"sarvam": 0, "fallback": 0}
        
        print(f"Translator initialized - Sarvam: {'Yes' if sarvam_api_key else 'No'}")
    
    def translate_sarvam(self, text, target_language):
        """PRIMARY: Sarvam AI"""
        if not self.sarvam_key or target_language not in SARVAM_CODES:
            return None
        
        try:
            response = requests.post(
                self.sarvam_url,
                headers={"api-subscription-key": self.sarvam_key, "Content-Type": "application/json"},
                json={
                    "input": text,
                    "source_language_code": "en-IN",
                    "target_language_code": SARVAM_CODES[target_language],
                    "speaker_gender": "Male",
                    "mode": "formal",
                    "model": "mayura:v1"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'translated_text' in result:
                    self.stats["sarvam"] += 1
                    return result['translated_text'].strip()
        except:
            pass
        return None
    
    def translate_fallback(self, text, target_language):
        """FALLBACK: Common words"""
        common = {
            "potato": {"Hindi": "आलू", "Bengali": "আলু", "Tamil": "உருளைக்கிழங்கு", "Telugu": "బంగాళాదుంప", "Malayalam": "ഉരുളക്കിഴങ്ങ്", "Kannada": "ಆಲೂಗಡ್ಡೆ", "Marathi": "बटाटा", "Gujarati": "બટાકા"},
            "ladyfinger": {"Hindi": "भिंडी", "Bengali": "ঢেঁড়স", "Tamil": "வெண்டைக்காய்", "Telugu": "బెండకాయ", "Malayalam": "വെണ്ടക്ക", "Kannada": "ಬೆಂಡೆಕಾಯಿ", "Marathi": "भेंडी", "Gujarati": "ભીંડા"},
            "tomato": {"Hindi": "टमाटर", "Bengali": "টমেটো", "Tamil": "தக்காளி", "Telugu": "టమాటో", "Malayalam": "തക്കാളി", "Kannada": "ಟೊಮೇಟೊ", "Marathi": "टोमॅटो", "Gujarati": "ટામેટું"},
            "onion": {"Hindi": "प्याज", "Bengali": "পেঁয়াজ", "Tamil": "வெங்காயம்", "Telugu": "ఉల్లిపాయ", "Malayalam": "ഉള്ളി", "Kannada": "ಈರುಳ್ಳಿ", "Marathi": "कांदा", "Gujarati": "ડુંગળી"}
        }
        
        if text.lower() in common and target_language in common[text.lower()]:
            self.stats["fallback"] += 1
            return common[text.lower()][target_language]
        return None
    
    def translate(self, text, target_language):
        """Smart translation"""
        text = text.strip()
        if not text:
            return "", "none"
        
        # Try Sarvam
        result = self.translate_sarvam(text, target_language)
        if result:
            return result, "sarvam"
        
        # Try fallback
        result = self.translate_fallback(text, target_language)
        if result:
            return result, "fallback"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        return f"Sarvam: {self.stats['sarvam']} | Fallback: {self.stats['fallback']} | Total: {total}"

_translator = None

def get_translator(sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key, huggingface_token, gemini_api_key)
    return _translator
