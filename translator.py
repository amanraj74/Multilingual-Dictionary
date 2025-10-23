"""
🌍 SARVAM-TRANSLATE via Hugging Face Serverless
NO DOWNLOAD - Uses HF Token for API access
ALL 22 Indian Languages
"""

import requests
import json
import time

SARVAM_LANGUAGES = [
    "Hindi", "Bengali", "Tamil", "Telugu", "Malayalam", "Kannada",
    "Marathi", "Gujarati", "Odia", "Punjabi", "Assamese", "Urdu",
    "Maithili", "Sanskrit", "Konkani", "Nepali", "Sindhi", "Dogri",
    "Manipuri", "Bodo", "Kashmiri", "Santali"
]

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
        self.hf_token = huggingface_token
        
        if not huggingface_token:
            print("⚠️  WARNING: No HF token - translations will use fallback only")
        
        # Sarvam-Translate via HF API
        self.api_url = "https://api-inference.huggingface.co/models/sarvamai/sarvam-translate"
        
        self.session = requests.Session()
        self.stats = {"sarvam": 0, "fallback": 0}
        
        print("="*80)
        print("🌍 SARVAM-TRANSLATE (No Download)")
        print(f"HF Token: {'✅ Provided' if huggingface_token else '❌ Missing'}")
        print("="*80)
    
    def translate_sarvam(self, text, target_language):
        """Sarvam-Translate via HF Inference API"""
        if not self.hf_token or target_language not in SARVAM_LANGUAGES:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare prompt - Sarvam model uses text-generation
            payload = {
                "inputs": f"<|system|>Translate the text below to {target_language}.<|end|><|user|>{text}<|end|><|assistant|>",
                "parameters": {
                    "max_new_tokens": 200,
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
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60  # Longer timeout for model loading
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract translation
                translation = None
                if isinstance(result, list) and len(result) > 0:
                    translation = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    translation = result.get('generated_text', '')
                
                if translation:
                    # Clean output
                    translation = translation.strip()
                    
                    # Remove artifacts
                    artifacts = ["<|assistant|>", "<|end|>", "Translation:", f"{target_language}:"]
                    for artifact in artifacts:
                        translation = translation.replace(artifact, "")
                    
                    translation = translation.strip().strip('"\'')
                    
                    if translation and translation != text:
                        self.stats["sarvam"] += 1
                        print(f"✅ {target_language}: {translation[:30]}...")
                        return translation
            
            # Model loading (503)
            elif response.status_code == 503:
                error = response.json()
                estimated_time = error.get('estimated_time', 20)
                print(f"⏳ Model loading... {estimated_time}s")
                time.sleep(min(estimated_time + 5, 30))
                # Retry once
                return self.translate_sarvam(text, target_language)
            
            # Rate limit (429)
            elif response.status_code == 429:
                print(f"⏸️ Rate limit - waiting 10s")
                time.sleep(10)
                return self.translate_sarvam(text, target_language)
            
            else:
                print(f"❌ API error ({target_language}): {response.status_code}")
        
        except Exception as e:
            print(f"❌ Error ({target_language}): {str(e)[:60]}")
        
        return None
    
    def translate_fallback(self, text, target_language):
        """Comprehensive fallback for common words"""
        words = {
            "potato": {"Hindi": "आलू", "Bengali": "আলু", "Tamil": "உருளைக்கிழங்கு", "Telugu": "బంగాళాదుంప", "Malayalam": "ഉരുളക്കിഴങ്ങ്", "Kannada": "ಆಲೂಗಡ್ಡೆ", "Marathi": "बटाटा", "Gujarati": "બટાકા", "Odia": "ଆଳୁ", "Punjabi": "ਆਲੂ", "Assamese": "আলু", "Urdu": "آلو", "Maithili": "आलू", "Sanskrit": "आलुकम्", "Konkani": "आळू", "Nepali": "आलु", "Sindhi": "آلو", "Dogri": "आलू", "Manipuri": "আলু", "Bodo": "आलू", "Kashmiri": "آلو", "Santali": "आलू"},
            "apple": {"Hindi": "सेब", "Bengali": "আপেল", "Tamil": "ஆப்பிள்", "Telugu": "ఆపిల్", "Malayalam": "ആപ്പിൾ", "Kannada": "ಸೇಬು", "Marathi": "सफरचंद", "Gujarati": "સફરજન", "Odia": "ସେଓ", "Punjabi": "ਸੇਬ", "Assamese": "আপেল", "Urdu": "سیب", "Maithili": "सेब", "Sanskrit": "सेवम्", "Konkani": "सफरचंद", "Nepali": "स्याउ", "Sindhi": "سيب", "Dogri": "सेब", "Manipuri": "আপেল", "Bodo": "सेब", "Kashmiri": "چھُنٹھ", "Santali": "सेब"},
            "pineapple": {"Hindi": "अनानास", "Bengali": "আনারস", "Tamil": "அன்னாசி", "Telugu": "అనాసపండు", "Malayalam": "കൈതച്ചക്ക", "Kannada": "ಅನಾನಸ್", "Marathi": "अननस", "Gujarati": "અનાનસ", "Odia": "ଆନନ୍ନା", "Punjabi": "ਅਨਾਨਾਸ", "Assamese": "মধুৰি আম", "Urdu": "انناس", "Maithili": "अनानास", "Sanskrit": "अनानासम्", "Konkani": "अननस", "Nepali": "भुइँ काँटा", "Sindhi": "انناس", "Dogri": "अनानास", "Manipuri": "আনারস", "Bodo": "अनानास", "Kashmiri": "اناناس", "Santali": "अनानास"},
            "ladyfinger": {"Hindi": "भिंडी", "Bengali": "ঢেঁড়স", "Tamil": "வெண்டைக்காய்", "Telugu": "బెండకాయ", "Malayalam": "വെണ്ടക്ക", "Kannada": "ಬೆಂಡೆಕಾಯಿ", "Marathi": "भेंडी", "Gujarati": "ભીંડા", "Odia": "ଭେଣ୍ଡି", "Punjabi": "ਭਿੰਡੀ", "Assamese": "ভেণ্ডি", "Urdu": "بھنڈی", "Maithili": "भिंडी", "Sanskrit": "भिण्डी", "Konkani": "भेंडें", "Nepali": "भिंडी", "Sindhi": "ڀنڊي", "Dogri": "भिंडी"},
            "tomato": {"Hindi": "टमाटर", "Bengali": "টমেটো", "Tamil": "தக்காளி", "Telugu": "టమాటో", "Malayalam": "തക്കാളി", "Kannada": "ಟೊಮೇಟೊ", "Marathi": "टोमॅटो", "Gujarati": "ટામેટું", "Odia": "ଟମାଟୋ", "Punjabi": "ਟਮਾਟਰ", "Assamese": "টমেটো", "Urdu": "ٹماٹر", "Maithili": "टमाटर", "Sanskrit": "रक्तफलम्", "Konkani": "टोमॅटो", "Nepali": "गोलभेडा", "Sindhi": "ٽماٽو", "Dogri": "टमाटर"},
            "onion": {"Hindi": "प्याज", "Bengali": "পেঁয়াজ", "Tamil": "வெங்காயம்", "Telugu": "ఉల్లిపాయ", "Malayalam": "ഉള്ളി", "Kannada": "ಈರುಳ್ಳಿ", "Marathi": "कांदा", "Gujarati": "ડુંગળી", "Odia": "ପିଆଜ", "Punjabi": "ਪਿਆਜ਼", "Assamese": "পিঁয়াজ", "Urdu": "پیاز", "Maithili": "प्याज", "Sanskrit": "पलाण्डुः", "Konkani": "कांदो", "Nepali": "प्याज"},
            "water": {"Hindi": "पानी", "Bengali": "জল", "Tamil": "நீர்", "Telugu": "నీరు", "Malayalam": "വെള്ളം", "Kannada": "ನೀರು", "Marathi": "पाणी", "Gujarati": "પાણી", "Odia": "ପାଣି", "Punjabi": "ਪਾਣੀ", "Assamese": "পানী", "Urdu": "پانی", "Maithili": "पानी", "Sanskrit": "जलम्"},
            "rice": {"Hindi": "चावल", "Bengali": "ভাত", "Tamil": "அரிசி", "Telugu": "అన్నం", "Malayalam": "ചോറ്", "Kannada": "ಅನ್ನ", "Marathi": "तांदूळ", "Gujarati": "ચોખા", "Odia": "ଚାଉଳ", "Punjabi": "ਚੌਲ", "Assamese": "ভাত", "Urdu": "چاول"},
            "bread": {"Hindi": "रोटी", "Bengali": "রুটি", "Tamil": "ரொட்டி", "Telugu": "రొట్టె", "Malayalam": "റൊട്ടി", "Kannada": "ರೊಟ್ಟಿ", "Marathi": "पाव", "Gujarati": "રોટલી", "Odia": "ରୁଟି", "Punjabi": "ਰੋਟੀ", "Assamese": "ৰুটী", "Urdu": "روٹی"},
            "milk": {"Hindi": "दूध", "Bengali": "দুধ", "Tamil": "பால்", "Telugu": "పాలు", "Malayalam": "പാൽ", "Kannada": "ಹಾಲು", "Marathi": "दूध", "Gujarati": "દૂધ", "Odia": "କ୍ଷୀର", "Punjabi": "ਦੁੱਧ", "Assamese": "গাখীৰ", "Urdu": "دودھ"},
            "food": {"Hindi": "भोजन", "Bengali": "খাবার", "Tamil": "உணவு", "Telugu": "ఆహారం", "Malayalam": "ഭക്ഷണം", "Kannada": "ಆಹಾರ", "Marathi": "अन्न", "Gujarati": "ખોરાક", "Odia": "ଖାଦ୍ୟ", "Punjabi": "ਭੋਜਨ", "Assamese": "খাদ্য", "Urdu": "کھانا"}
        }
        
        if text.lower() in words and target_language in words[text.lower()]:
            self.stats["fallback"] += 1
            return words[text.lower()][target_language]
        return None
    
    def translate(self, text, target_language):
        text = text.strip()
        if not text:
            return "", "none"
        
        # Try Sarvam-Translate (with HF token)
        result = self.translate_sarvam(text, target_language)
        if result:
            return result, "sarvam"
        
        # Fallback to dictionary
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
