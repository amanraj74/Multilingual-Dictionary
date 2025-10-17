"""
🌍 ULTIMATE TRANSLATOR - Cloud Safe Version
Works on both localhost and Streamlit Cloud
"""

import requests
import time

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch
    HAS_TRANSFORMERS = True
except:
    HAS_TRANSFORMERS = False

# Fallback language codes if utils not available
try:
    from utils.language_utils import get_language_code
except ImportError:
    print("⚠️  utils.language_utils not found, using fallback")
    def get_language_code(language):
        codes = {
            "Hindi": "hin_Deva", "Bengali": "ben_Beng", "Tamil": "tam_Taml",
            "Telugu": "tel_Telu", "Malayalam": "mal_Mlym", "Kannada": "kan_Knda",
            "Marathi": "mar_Deva", "Gujarati": "guj_Gujr", "Odia": "ory_Orya",
            "Punjabi": "pan_Guru", "Assamese": "asm_Beng", "Urdu": "urd_Arab",
            "Maithili": "mai_Deva", "Sanskrit": "san_Deva", "Konkani": "gom_Deva",
            "Nepali": "npi_Deva", "Sindhi": "snd_Deva", "Dogri": "doi_Deva",
            "Manipuri": "mni_Mtei", "Bodo": "brx_Deva", "Kashmiri": "kas_Deva",
            "Santali": "sat_Olck"
        }
        return codes.get(language, "hin_Deva")

SARVAM_CODES = {
    "Hindi": "hi-IN", "Bengali": "bn-IN", "Tamil": "ta-IN", "Telugu": "te-IN",
    "Malayalam": "ml-IN", "Kannada": "kn-IN", "Marathi": "mr-IN", "Gujarati": "gu-IN",
    "Odia": "or-IN", "Punjabi": "pa-IN", "Assamese": "as-IN", "Urdu": "ur-IN",
    "Maithili": "mai-IN", "Sanskrit": "sa-IN", "Konkani": "kok-IN", "Nepali": "ne-IN",
    "Sindhi": "sd-IN", "Dogri": "doi-IN", "Manipuri": "mni-IN", "Bodo": "brx-IN",
    "Kashmiri": "ks-IN", "Santali": "sat-IN"
}

MYMEMORY_CODES = {
    "Hindi": "hi", "Bengali": "bn", "Tamil": "ta", "Telugu": "te",
    "Malayalam": "ml", "Kannada": "kn", "Marathi": "mr", "Gujarati": "gu",
    "Odia": "or", "Punjabi": "pa", "Assamese": "as", "Urdu": "ur",
    "Nepali": "ne", "Sanskrit": "sa", "Maithili": "mai", "Sindhi": "sd"
}

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, gemini_api_key=None):
        self.sarvam_key = sarvam_api_key
        self.gemini_key = gemini_api_key
        self.sarvam_url = "https://api.sarvam.ai/translate"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        self.mymemory_url = "https://api.mymemory.translated.net/get"
        self.session = requests.Session()
        
        self.model = None
        self.tokenizer = None
        self.device = "cpu"  # Cloud uses CPU
        
        self.stats = {"sarvam": 0, "gemini": 0, "mymemory": 0, "model": 0}
        
        print("\n" + "="*80)
        print("🌍 TRANSLATOR INITIALIZED")
        print("="*80)
        print(f"Sarvam: {'✅' if sarvam_api_key else '❌'}")
        print(f"Gemini: {'✅' if gemini_api_key else '❌'}")
        print(f"MyMemory: ✅")
        print(f"Model: {'✅' if HAS_TRANSFORMERS else '❌'}")
        print("="*80 + "\n")
    
    def translate_sarvam(self, text, target_language):
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
    
    def translate_gemini(self, text, target_language):
        if not self.gemini_key:
            return None
        try:
            url = f"{self.gemini_url}?key={self.gemini_key}"
            response = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": f"Translate to {target_language}: {text}\n\nOnly provide the translation."}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 256}
                },
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    self.stats["gemini"] += 1
                    return text.strip().strip('"\'')
        except:
            pass
        return None
    
    def translate_mymemory(self, text, target_language):
        if target_language not in MYMEMORY_CODES:
            return None
        try:
            response = self.session.get(
                self.mymemory_url,
                params={'q': text, 'langpair': f'en|{MYMEMORY_CODES[target_language]}'},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if 'responseData' in data:
                    translation = data['responseData'].get('translatedText', '')
                    if translation and translation.strip() != text.strip():
                        self.stats["mymemory"] += 1
                        return translation.strip()
        except:
            pass
        return None
    
    def translate_model(self, text, target_language):
        # Disabled on cloud (too slow)
        return None
    
    def translate(self, text, target_language):
        text = text.strip()
        if not text:
            return "", "none"
        
        result = self.translate_sarvam(text, target_language)
        if result:
            return result, "sarvam"
        
        result = self.translate_gemini(text, target_language)
        if result:
            return result, "gemini"
        
        result = self.translate_mymemory(text, target_language)
        if result:
            return result, "mymemory"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        return f"Sarvam: {self.stats['sarvam']} | Gemini: {self.stats['gemini']} | MyMemory: {self.stats['mymemory']} | Total: {total}"

_translator = None

def get_translator(sarvam_api_key=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key=sarvam_api_key, gemini_api_key=gemini_api_key)
    return _translator
