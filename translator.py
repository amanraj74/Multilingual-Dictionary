"""
🌍 ULTIMATE PRODUCTION TRANSLATOR
Sarvam AI (Best) → MyMemory (Backup) → IndicTrans2 (Offline)
100% Working with all fallbacks!
"""

import requests
import time
import os

# Add at the top of translator.py after imports

# Common vegetable name corrections
COMMON_WORDS_MAPPING = {
    "ladyfinger": "okra",  # More standard term
    "brinjal": "eggplant",
    "capsicum": "bell pepper",
}

# In translate method, add before translation:
def translate(self, text, target_language):
    text = text.strip()
    if not text:
        return "", "none"
    
    # Check for common word mappings
    text_lower = text.lower()
    if text_lower in COMMON_WORDS_MAPPING:
        text = COMMON_WORDS_MAPPING[text_lower]
    
    # ... rest of code

# Try transformers for model backup
try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch
    HAS_TRANSFORMERS = True
except:
    HAS_TRANSFORMERS = False

from utils.language_utils import get_language_code

# ═══════════════════════════════════════════════════════════════════════════════
# LANGUAGE CODES FOR ALL APIs
# ═══════════════════════════════════════════════════════════════════════════════

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

ALL_LANGUAGES = list(SARVAM_CODES.keys())

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TRANSLATOR CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class UltimateTranslator:
    """Production-grade translator with triple fallback"""
    
    def __init__(self, sarvam_api_key=None):
        self.sarvam_key = sarvam_api_key
        self.sarvam_url = "https://api.sarvam.ai/translate"
        self.mymemory_url = "https://api.mymemory.translated.net/get"
        self.session = requests.Session()
        
        # Model
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if HAS_TRANSFORMERS and torch.cuda.is_available() else "cpu"
        
        # Stats
        self.stats = {"sarvam": 0, "mymemory": 0, "model": 0, "failed": 0}
        
        self._print_banner()
    
    def _print_banner(self):
        print("\n" + "="*80)
        print("🌍 ULTIMATE TRANSLATOR - Production Ready")
        print("="*80)
        print(f"1️⃣  Sarvam AI:    {'✅ ACTIVE (Best Quality!)' if self.sarvam_key else '❌ No API Key'}")
        print(f"2️⃣  MyMemory API: ✅ ACTIVE (Backup)")
        print(f"3️⃣  Model:        {'✅ AVAILABLE' if HAS_TRANSFORMERS else '❌ Not Installed'}")
        print("="*80 + "\n")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # METHOD 1: SARVAM AI (PRIMARY - BEST QUALITY)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def translate_sarvam(self, text, target_language):
        """Sarvam AI - Best quality for Indian languages"""
        if not self.sarvam_key:
            return None
        
        target_code = SARVAM_CODES.get(target_language)
        if not target_code:
            return None
        
        try:
            headers = {
                "api-subscription-key": self.sarvam_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "input": text,
                "source_language_code": "en-IN",
                "target_language_code": target_code,
                "speaker_gender": "Male",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": True
            }
            
            response = requests.post(self.sarvam_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'translated_text' in result:
                    self.stats["sarvam"] += 1
                    return result['translated_text'].strip()
            
            return None
        except:
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # METHOD 2: MYMEMORY API (BACKUP)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def translate_mymemory(self, text, target_language):
        """MyMemory API - Fast and reliable backup"""
        target_code = MYMEMORY_CODES.get(target_language)
        if not target_code:
            return None
        
        try:
            params = {'q': text, 'langpair': f'en|{target_code}'}
            response = self.session.get(self.mymemory_url, params=params, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                if 'responseData' in data:
                    translation = data['responseData'].get('translatedText', '')
                    if translation and translation.strip() != text.strip():
                        self.stats["mymemory"] += 1
                        return ' '.join(translation.split()).strip()
            
            return None
        except:
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # METHOD 3: INDICTRANS2 MODEL (OFFLINE BACKUP)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def load_model(self):
        """Load IndicTrans2 model (one-time)"""
        if not HAS_TRANSFORMERS:
            return False
        
        if self.model is not None:
            return True
        
        try:
            print("📥 Loading IndicTrans2 model (first time only)...")
            model_name = "ai4bharat/indictrans2-en-indic-1B"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(self.device)
            
            print(f"✅ Model loaded on {self.device}\n")
            return True
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            return False
    
    def translate_model(self, text, target_language):
        """IndicTrans2 model - Offline backup"""
        if not self.load_model():
            return None
        
        try:
            tgt_lang = get_language_code(target_language)
            
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=256
            )
            
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
                    num_beams=5,
                    early_stopping=True
                )
            
            translation = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
            self.stats["model"] += 1
            return translation.strip()
            
        except:
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN TRANSLATE METHOD (SMART FALLBACK)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def translate(self, text, target_language):
        """
        Smart translation with triple fallback
        Returns: (translation, method_used)
        """
        text = text.strip()
        if not text:
            return "", "none"
        
        # 1. Try Sarvam AI (BEST)
        result = self.translate_sarvam(text, target_language)
        if result:
            return result, "sarvam"
        
        # 2. Try MyMemory (FAST)
        result = self.translate_mymemory(text, target_language)
        if result:
            return result, "mymemory"
        
        # 3. Try Model (OFFLINE)
        result = self.translate_model(text, target_language)
        if result:
            return result, "model"
        
        # All failed
        self.stats["failed"] += 1
        return f"⚠️ Translation unavailable", "none"
    
    def translate_simple(self, text, target_language):
        """Simple translate (just return text, no method info)"""
        result, _ = self.translate(text, target_language)
        return result
    
    def translate_batch(self, texts, target_language):
        """Batch translation with rate limiting"""
        results = []
        for text in texts:
            result, method = self.translate(text, target_language)
            results.append((result, method))
            time.sleep(0.15)  # Rate limiting
        return results
    
    def get_stats(self):
        """Get usage statistics"""
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        
        return f"""
Translation Statistics:
  Sarvam AI:   {self.stats['sarvam']} ({self.stats['sarvam']/total*100:.1f}%)
  MyMemory:    {self.stats['mymemory']} ({self.stats['mymemory']/total*100:.1f}%)
  Model:       {self.stats['model']} ({self.stats['model']/total*100:.1f}%)
  Failed:      {self.stats['failed']} ({self.stats['failed']/total*100:.1f}%)
  Total:       {total}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

_translator = None

def get_translator(sarvam_api_key=None):
    """Get or create translator instance"""
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key=sarvam_api_key)
    return _translator

# ═══════════════════════════════════════════════════════════════════════════════
# TEST CODE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*80)
    print("🧪 TESTING ULTIMATE TRANSLATOR")
    print("="*80)
    
    # Get API key (optional)
    print("\n💡 Sarvam AI Key: https://dashboard.sarvam.ai/")
    api_key = input("Enter Sarvam API key (or Enter to skip): ").strip()
    
    translator = get_translator(sarvam_api_key=api_key if api_key else None)
    
    # Test cases
    tests = [
        ("Hello, how are you?", "Hindi"),
        ("Good morning", "Tamil"),
        ("Thank you very much", "Telugu"),
        ("I love programming", "Malayalam"),
        ("Welcome to India", "Bengali")
    ]
    
    print("\n" + "="*80)
    print("Testing all methods...")
    print("="*80)
    
    for text, lang in tests:
        result, method = translator.translate(text, lang)
        print(f"\n{lang} (via {method}):")
        print(f"  Input:  {text}")
        print(f"  Output: {result}")
    
    # Show stats
    print("\n" + "="*80)
    print(translator.get_stats())
    print("="*80)
