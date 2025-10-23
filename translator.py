"""
🌍 SARVAM-TRANSLATE Model via Hugging Face
AI4Bharat + Sarvam AI - ALL 22 Indian Languages
"""

import requests
import time
import json

# Sarvam-Translate supported languages
SARVAM_LANGUAGES = [
    "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi",
    "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam",
    "Manipuri", "Marathi", "Nepali", "Odia", "Punjabi",
    "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"
]

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
        self.hf_token = huggingface_token
        
        # Sarvam-Translate model endpoint
        self.model_url = "https://api-inference.huggingface.co/models/sarvamai/sarvam-translate"
        
        self.session = requests.Session()
        self.stats = {"sarvam_translate": 0, "fallback": 0}
        
        print("="*80)
        print("🌍 SARVAM-TRANSLATE (AI4Bharat) via Hugging Face")
        print(f"Token: {'✅ Provided' if huggingface_token else '⚠️  Using public API (slower)'}")
        print("ALL 22 Indian Languages Supported")
        print("="*80)
    
    def translate_sarvam_hf(self, text, target_language):
        """Sarvam-Translate via Hugging Face Inference API"""
        if target_language not in SARVAM_LANGUAGES:
            return None
        
        try:
            headers = {"Content-Type": "application/json"}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            # Format as chat conversation (as per model requirements)
            conversation = [
                {
                    "role": "system",
                    "content": f"Translate the text below to {target_language}."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            payload = {
                "inputs": json.dumps(conversation),
                "parameters": {
                    "max_new_tokens": 256,
                    "temperature": 0.01,
                    "do_sample": True,
                    "return_full_text": False
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": False
                }
            }
            
            response = requests.post(
                self.model_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse response
                translation = None
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        translation = result[0]['generated_text']
                    elif isinstance(result[0], str):
                        translation = result[0]
                elif isinstance(result, dict) and 'generated_text' in result:
                    translation = result['generated_text']
                
                if translation:
                    # Clean the translation
                    translation = translation.strip()
                    
                    # Remove common artifacts
                    remove_prefixes = [
                        "Translation:",
                        f"{target_language}:",
                        "Output:",
                        "Answer:",
                        "assistant\n",
                        "<|assistant|>",
                    ]
                    
                    for prefix in remove_prefixes:
                        if translation.lower().startswith(prefix.lower()):
                            translation = translation[len(prefix):].strip()
                    
                    # Remove quotes if wrapped
                    if translation.startswith('"') and translation.endswith('"'):
                        translation = translation[1:-1]
                    if translation.startswith("'") and translation.endswith("'"):
                        translation = translation[1:-1]
                    
                    if translation and translation != text:
                        self.stats["sarvam_translate"] += 1
                        return translation
            
            # Model loading (503)
            elif response.status_code == 503:
                error_data = response.json()
                if 'estimated_time' in error_data:
                    wait_time = min(error_data['estimated_time'], 10)
                    print(f"Model loading... waiting {wait_time}s")
                    time.sleep(wait_time + 2)
                    # Retry once
                    return self.translate_sarvam_hf(text, target_language)
                else:
                    time.sleep(5)
                    return self.translate_sarvam_hf(text, target_language)
            
            else:
                print(f"HF API error ({target_language}): {response.status_code}")
        
        except Exception as e:
            print(f"Sarvam-Translate error ({target_language}): {str(e)[:60]}")
        
        return None
    
    def translate_fallback(self, text, target_language):
        """Comprehensive fallback dictionary"""
        
        words = {
            "potato": {"Hindi": "आलू", "Bengali": "আলু", "Tamil": "உருளைக்கிழங்கு", "Telugu": "బంగాళాదుంప", "Malayalam": "ഉരുളക്കിഴങ്ങ്", "Kannada": "ಆಲೂಗಡ್ಡೆ", "Marathi": "बटाटा", "Gujarati": "બટાકા", "Odia": "ଆଳୁ", "Punjabi": "ਆਲੂ", "Assamese": "আলু", "Urdu": "آلو", "Maithili": "आलू", "Sanskrit": "आलुकम्", "Konkani": "आळू", "Nepali": "आलु", "Sindhi": "آلو", "Dogri": "आलू", "Manipuri": "আলু", "Bodo": "आलू", "Kashmiri": "آلو", "Santali": "आलू"},
            "apple": {"Hindi": "सेब", "Bengali": "আপেল", "Tamil": "ஆப்பிள்", "Telugu": "ఆపిల్", "Malayalam": "ആപ്പിൾ", "Kannada": "ಸೇಬು", "Marathi": "सफरचंद", "Gujarati": "સફરજન", "Odia": "ସେଓ", "Punjabi": "ਸੇਬ", "Assamese": "আপেল", "Urdu": "سیب", "Maithili": "सेब", "Sanskrit": "सेवम्", "Konkani": "सफरचंद", "Nepali": "स्याउ", "Sindhi": "سيب", "Dogri": "सेब", "Manipuri": "আপেল", "Bodo": "सेब", "Kashmiri": "چھُنٹھ", "Santali": "सेब"},
            "ladyfinger": {"Hindi": "भिंडी", "Bengali": "ঢেঁড়স", "Tamil": "வெண்டைக்காய்", "Telugu": "బెండకాయ", "Malayalam": "വെണ്ടക്ക", "Kannada": "ಬೆಂಡೆಕಾಯಿ", "Marathi": "भेंडी", "Gujarati": "ભીંડા", "Odia": "ଭେଣ୍ଡି", "Punjabi": "ਭਿੰਡੀ", "Assamese": "ভেণ্ডি", "Urdu": "بھنڈی", "Maithili": "भिंडी", "Sanskrit": "भिण्डी", "Konkani": "भेंडें", "Nepali": "भिंडी", "Sindhi": "ڀنڊي", "Dogri": "भिंडी"},
            "tomato": {"Hindi": "टमाटर", "Bengali": "টমেটো", "Tamil": "தக்காளி", "Telugu": "టమాటో", "Malayalam": "തക്കാളി", "Kannada": "ಟೊಮೇಟೊ", "Marathi": "टोमॅटो", "Gujarati": "ટામેટું", "Odia": "ଟମାଟୋ", "Punjabi": "ਟਮਾਟਰ", "Assamese": "টমেটো", "Urdu": "ٹماٹر"},
            "onion": {"Hindi": "प्याज", "Bengali": "পেঁয়াজ", "Tamil": "வெங்காயம்", "Telugu": "ఉల్లిపాయ", "Malayalam": "ഉള്ളി", "Kannada": "ಈರುಳ್ಳಿ", "Marathi": "कांदा", "Gujarati": "ડુંગળી", "Odia": "ପିଆଜ", "Punjabi": "ਪਿਆਜ਼", "Assamese": "পিঁয়াজ", "Urdu": "پیاز"},
            "water": {"Hindi": "पानी", "Bengali": "জল", "Tamil": "நீர்", "Telugu": "నీరు", "Malayalam": "വെള്ളം", "Kannada": "ನೀರು", "Marathi": "पाणी", "Gujarati": "પાણી", "Odia": "ପାଣି", "Punjabi": "ਪਾਣੀ", "Assamese": "পানী", "Urdu": "پانی"},
            "rice": {"Hindi": "चावल", "Bengali": "ভাত", "Tamil": "அரிசி", "Telugu": "అన్నం", "Malayalam": "ചോറ്", "Kannada": "ಅನ್ನ", "Marathi": "तांदूळ", "Gujarati": "ચોખા", "Odia": "ଚାଉଳ", "Punjabi": "ਚੌਲ", "Assamese": "ভাত", "Urdu": "چاول"},
            "food": {"Hindi": "भोजन", "Bengali": "খাবার", "Tamil": "உணவு", "Telugu": "ఆహారం", "Malayalam": "ഭക്ഷണം", "Kannada": "ಆಹಾರ", "Marathi": "अन्न", "Gujarati": "ખોરાક", "Odia": "ଖାଦ୍ୟ", "Punjabi": "ਭੋਜਨ", "Assamese": "খাদ্য", "Urdu": "کھانا"}
        }
        
        if text.lower() in words and target_language in words[text.lower()]:
            self.stats["fallback"] += 1
            return words[text.lower()][target_language]
        
        return None
    
    def translate(self, text, target_language):
        """Main translation function"""
        text = text.strip()
        if not text:
            return "", "none"
        
        # 1. Try Sarvam-Translate model
        result = self.translate_sarvam_hf(text, target_language)
        if result:
            return result, "sarvam_translate"
        
        # 2. Try fallback
        result = self.translate_fallback(text, target_language)
        if result:
            return result, "fallback"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        return f"Sarvam-Translate: {self.stats['sarvam_translate']} | Fallback: {self.stats['fallback']} | Total: {total}"

_translator = None

def get_translator(sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key, huggingface_token, gemini_api_key)
    return _translator
