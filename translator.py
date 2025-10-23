"""
🌍 INDICTRANS2 - AI4Bharat via Hugging Face
ALL 22 Indian Languages - FAST & RELIABLE
"""

import requests
import time

# IndicTrans2 language codes
INDICTRANS_CODES = {
    "Hindi": "hin_Deva", "Bengali": "ben_Beng", "Tamil": "tam_Taml",
    "Telugu": "tel_Telu", "Malayalam": "mal_Mlym", "Kannada": "kan_Knda",
    "Marathi": "mar_Deva", "Gujarati": "guj_Gujr", "Odia": "ory_Orya",
    "Punjabi": "pan_Guru", "Assamese": "asm_Beng", "Urdu": "urd_Arab",
    "Maithili": "mai_Deva", "Sanskrit": "san_Deva", "Konkani": "gom_Deva",
    "Nepali": "npi_Deva", "Sindhi": "snd_Deva", "Dogri": "doi_Deva",
    "Manipuri": "mni_Mtei", "Bodo": "brx_Deva", "Kashmiri": "kas_Arab",
    "Santali": "sat_Olck"
}

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
        self.hf_token = huggingface_token
        
        # IndicTrans2 model (FAST & RELIABLE!)
        self.model_url = "https://api-inference.huggingface.co/models/ai4bharat/indictrans2-en-indic-1B"
        
        self.session = requests.Session()
        self.stats = {"indictrans": 0, "fallback": 0}
        
        print("="*80)
        print("🌍 INDICTRANS2 (AI4Bharat) via Hugging Face")
        print(f"Token: {'✅' if huggingface_token else '⚠️  Public (works but slower)'}")
        print("="*80)
    
    def translate_indictrans(self, text, target_language):
        """IndicTrans2 - FAST & RELIABLE"""
        if target_language not in INDICTRANS_CODES:
            return None
        
        try:
            headers = {}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            payload = {
                "inputs": text,
                "parameters": {
                    "src_lang": "eng_Latn",
                    "tgt_lang": INDICTRANS_CODES[target_language],
                    "max_length": 256
                }
            }
            
            response = requests.post(
                self.model_url,
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                
                translation = None
                if isinstance(result, list) and len(result) > 0:
                    if 'translation_text' in result[0]:
                        translation = result[0]['translation_text']
                    elif 'generated_text' in result[0]:
                        translation = result[0]['generated_text']
                    elif isinstance(result[0], str):
                        translation = result[0]
                elif isinstance(result, dict):
                    translation = result.get('translation_text') or result.get('generated_text')
                
                if translation:
                    translation = translation.strip()
                    if translation and translation != text:
                        self.stats["indictrans"] += 1
                        return translation
            
            # Model loading
            elif response.status_code == 503:
                print(f"Loading model for {target_language}...")
                time.sleep(5)
                return self.translate_indictrans(text, target_language)
        
        except Exception as e:
            print(f"IndicTrans error ({target_language}): {str(e)[:50]}")
        
        return None
    
    def translate_fallback(self, text, target_language):
        """Fallback dictionary - 10+ common words"""
        
        words = {
            "potato": {"Hindi": "आलू", "Bengali": "আলু", "Tamil": "உருளைக்கிழங்கு", "Telugu": "బంగాళాదుంప", "Malayalam": "ഉരുളക്കിഴങ്ങ്", "Kannada": "ಆಲೂಗಡ್ಡೆ", "Marathi": "बटाटा", "Gujarati": "બટાકા", "Odia": "ଆଳୁ", "Punjabi": "ਆਲੂ", "Assamese": "আলু", "Urdu": "آلو", "Maithili": "आलू", "Sanskrit": "आलुकम्", "Konkani": "आळू", "Nepali": "आलु", "Sindhi": "آلو", "Dogri": "आलू", "Manipuri": "আলু", "Bodo": "आलू", "Kashmiri": "آلو", "Santali": "आलू"},
            "apple": {"Hindi": "सेब", "Bengali": "আপেল", "Tamil": "ஆப்பிள்", "Telugu": "ఆపిల్", "Malayalam": "ആപ്പിൾ", "Kannada": "ಸೇಬು", "Marathi": "सफरचंद", "Gujarati": "સફરજન", "Odia": "ସେଓ", "Punjabi": "ਸੇਬ", "Assamese": "আপেল", "Urdu": "سیب", "Maithili": "सेब", "Sanskrit": "सेवम्", "Konkani": "सफरचंद", "Nepali": "स्याउ", "Sindhi": "سيب", "Dogri": "सेब", "Manipuri": "আপেল", "Bodo": "सेब", "Kashmiri": "چھُنٹھ", "Santali": "सेब"},
            "pineapple": {"Hindi": "अनानास", "Bengali": "আনারস", "Tamil": "அன்னாசி", "Telugu": "అనాసపండు", "Malayalam": "കൈതച്ചക്ക", "Kannada": "ಅನಾನಸ್", "Marathi": "अननस", "Gujarati": "અનાનસ", "Odia": "ଆନନ୍ନା", "Punjabi": "ਅਨਾਨਾਸ", "Assamese": "মধুৰি আম", "Urdu": "انناس", "Maithili": "अनानास", "Sanskrit": "अनानासम्", "Konkani": "अननस", "Nepali": "भुइँ काँटा", "Sindhi": "انناس", "Dogri": "अनानास", "Manipuri": "আনারস", "Bodo": "अनानास", "Kashmiri": "اناناس", "Santali": "अनानास"},
            "ladyfinger": {"Hindi": "भिंडी", "Bengali": "ঢেঁড়স", "Tamil": "வெண்டைக்காய்", "Telugu": "బెండకాయ", "Malayalam": "വെണ്ടക്ക", "Kannada": "ಬೆಂಡೆಕಾಯಿ", "Marathi": "भेंडी", "Gujarati": "ભીંડા", "Odia": "ଭେଣ୍ଡି", "Punjabi": "ਭਿੰਡੀ", "Assamese": "ভেণ্ডি", "Urdu": "بھنڈی"},
            "tomato": {"Hindi": "टमाटर", "Bengali": "টমেটো", "Tamil": "தக்காளி", "Telugu": "టమాటో", "Malayalam": "തക്കാളി", "Kannada": "ಟೊಮೇಟೊ", "Marathi": "टोमॅटो", "Gujarati": "ટામેટું", "Odia": "ଟମାଟୋ", "Punjabi": "ਟਮਾਟਰ", "Assamese": "টমেটো", "Urdu": "ٹماٹر"},
            "onion": {"Hindi": "प्याज", "Bengali": "পেঁয়াজ", "Tamil": "வெங்காயம்", "Telugu": "ఉల్లిపాయ", "Malayalam": "ഉള്ളി", "Kannada": "ಈರುಳ್ಳಿ", "Marathi": "कांदा", "Gujarati": "ડુંગળી", "Odia": "ପିଆଜ", "Punjabi": "ਪਿਆਜ਼", "Assamese": "পিঁয়াজ", "Urdu": "پیاز"},
            "water": {"Hindi": "पानी", "Bengali": "জল", "Tamil": "நீர்", "Telugu": "నీరు", "Malayalam": "വെള്ളം", "Kannada": "ನೀರು", "Marathi": "पाणी", "Gujarati": "પાણી", "Odia": "ପାଣି", "Punjabi": "ਪਾਣੀ", "Assamese": "পানী", "Urdu": "پانی"},
            "rice": {"Hindi": "चावल", "Bengali": "ভাত", "Tamil": "அரிசி", "Telugu": "అన్నం", "Malayalam": "ചോറ്", "Kannada": "ಅನ್ನ", "Marathi": "तांदूळ", "Gujarati": "ચોખા", "Odia": "ଚାଉଳ", "Punjabi": "ਚੌਲ", "Assamese": "ভাত", "Urdu": "چاول"},
            "bread": {"Hindi": "रोटी", "Bengali": "রুটি", "Tamil": "ரொட்டி", "Telugu": "రొట్టె", "Malayalam": "റൊട്ടി", "Kannada": "ರೊಟ್ಟಿ", "Marathi": "पाव", "Gujarati": "રોટલી", "Odia": "ରୁଟି", "Punjabi": "ਰੋਟੀ", "Assamese": "ৰুটী", "Urdu": "روٹی"},
            "milk": {"Hindi": "दूध", "Bengali": "দুধ", "Tamil": "பால்", "Telugu": "పాలు", "Malayalam": "പാൽ", "Kannada": "ಹಾಲು", "Marathi": "दूध", "Gujarati": "દૂધ", "Odia": "କ୍ଷୀର", "Punjabi": "ਦੁੱਧ", "Assamese": "গাখীৰ", "Urdu": "دودھ"}
        }
        
        if text.lower() in words and target_language in words[text.lower()]:
            self.stats["fallback"] += 1
            return words[text.lower()][target_language]
        
        return None
    
    def translate(self, text, target_language):
        text = text.strip()
        if not text:
            return "", "none"
        
        # Try IndicTrans2
        result = self.translate_indictrans(text, target_language)
        if result:
            return result, "indictrans"
        
        # Try fallback
        result = self.translate_fallback(text, target_language)
        if result:
            return result, "fallback"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        return f"IndicTrans2: {self.stats['indictrans']} | Fallback: {self.stats['fallback']} | Total: {total}"

_translator = None

def get_translator(sarvam_api_key=None, huggingface_token=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key, huggingface_token, gemini_api_key)
    return _translator
