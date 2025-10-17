"""
🌍 ULTIMATE TRANSLATOR - All 4 Translation Sources
Sarvam AI → Gemini AI → MyMemory API → IndicTrans2 Model
"""

import requests
import time

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch
    HAS_TRANSFORMERS = True
except:
    HAS_TRANSFORMERS = False
    print("⚠️  transformers not available (model backup disabled)")

try:
    from utils.language_utils import get_language_code
except:
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
        print("\n" + "="*80)
        print("🌍 INITIALIZING ULTIMATE TRANSLATOR")
        print("="*80)
        
        self.sarvam_key = sarvam_api_key
        self.gemini_key = gemini_api_key
        self.sarvam_url = "https://api.sarvam.ai/translate"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        self.mymemory_url = "https://api.mymemory.translated.net/get"
        self.session = requests.Session()
        
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        if HAS_TRANSFORMERS and torch.cuda.is_available():
            self.device = "cuda"
        
        self.stats = {"sarvam": 0, "gemini": 0, "mymemory": 0, "model": 0}
        
        print(f"1️⃣  Sarvam AI:    {'✅ ACTIVE' if sarvam_api_key else '❌ Not configured'}")
        print(f"2️⃣  Gemini AI:    {'✅ ACTIVE' if gemini_api_key else '❌ Not configured'}")
        print(f"3️⃣  MyMemory:     ✅ ACTIVE (always available)")
        print(f"4️⃣  IndicTrans2:  {'✅ AVAILABLE' if HAS_TRANSFORMERS else '❌ Not installed'}")
        print("="*80 + "\n")
    
    def translate_sarvam(self, text, target_language):
        """PRIMARY: Sarvam AI - Best for Indian languages"""
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
                    "model": "mayura:v1",
                    "enable_preprocessing": True
                },
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if 'translated_text' in result:
                    self.stats["sarvam"] += 1
                    return result['translated_text'].strip()
        except Exception as e:
            print(f"Sarvam error: {str(e)[:50]}")
        return None
    
    def translate_gemini(self, text, target_language):
        """SECONDARY: Gemini AI"""
        if not self.gemini_key:
            return None
        try:
            url = f"{self.gemini_url}?key={self.gemini_key}"
            prompt = f"Translate this English text to {target_language}. Only provide the direct translation without quotes or explanations.\n\nText: {text}"
            
            response = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 256}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    translation = result['candidates'][0]['content']['parts'][0]['text']
                    self.stats["gemini"] += 1
                    return translation.strip().strip('"\'')
        except Exception as e:
            print(f"Gemini error: {str(e)[:50]}")
        return None
    
    def translate_mymemory(self, text, target_language):
        """TERTIARY: MyMemory API"""
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
    
    def load_model(self):
        """Load IndicTrans2 Model"""
        if not HAS_TRANSFORMERS or self.model is not None:
            return self.model is not None
        try:
            print("📥 Loading IndicTrans2 model (first time only)...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "ai4bharat/indictrans2-en-indic-1B", 
                trust_remote_code=True
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                "ai4bharat/indictrans2-en-indic-1B",
                trust_remote_code=True
            ).to(self.device)
            print(f"✅ Model loaded on {self.device}")
            return True
        except Exception as e:
            print(f"❌ Model load error: {e}")
            return False
    
    def translate_model(self, text, target_language):
        """QUATERNARY: IndicTrans2 Model"""
        if not self.load_model():
            return None
        try:
            tgt_lang = get_language_code(target_language)
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
            
            if self.device == "cuda":
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            self.tokenizer.tgt_lang = tgt_lang
            
            with torch.no_grad():
                generated = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.lang_code_to_id.get(
                        tgt_lang, 
                        self.tokenizer.bos_token_id
                    ),
                    max_length=256,
                    num_beams=5
                )
            
            translation = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
            self.stats["model"] += 1
            return translation.strip()
        except:
            return None
    
    def translate(self, text, target_language):
        """Smart fallback: Sarvam → Gemini → MyMemory → Model"""
        text = text.strip()
        if not text:
            return "", "none"
        
        # 1. Try Sarvam AI (BEST)
        result = self.translate_sarvam(text, target_language)
        if result:
            return result, "sarvam"
        
        # 2. Try Gemini AI
        result = self.translate_gemini(text, target_language)
        if result:
            return result, "gemini"
        
        # 3. Try MyMemory
        result = self.translate_mymemory(text, target_language)
        if result:
            return result, "mymemory"
        
        # 4. Try Model
        result = self.translate_model(text, target_language)
        if result:
            return result, "model"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        return f"""Translation Usage:
• Sarvam AI: {self.stats['sarvam']} ({self.stats['sarvam']/total*100:.1f}%)
• Gemini AI: {self.stats['gemini']} ({self.stats['gemini']/total*100:.1f}%)
• MyMemory: {self.stats['mymemory']} ({self.stats['mymemory']/total*100:.1f}%)
• Model: {self.stats['model']} ({self.stats['model']/total*100:.1f}%)
• Total: {total} translations"""

_translator = None

def get_translator(sarvam_api_key=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key=sarvam_api_key, gemini_api_key=gemini_api_key)
    return _translator
