"""
🌍 ULTIMATE TRANSLATOR - Best Free APIs for Indian Languages
1. IndicTrans2 API (AI4Bharat) - BEST for Indian languages
2. Gemini AI (if key provided)
3. MyMemory API (backup)
"""

import requests
import time
import streamlit as st

# Language codes for IndicTrans2
INDICTRANS_CODES = {
    "Hindi": "hi", "Bengali": "bn", "Tamil": "ta", "Telugu": "te",
    "Malayalam": "ml", "Kannada": "kn", "Marathi": "mr", "Gujarati": "gu",
    "Odia": "or", "Punjabi": "pa", "Assamese": "as", "Urdu": "ur",
    "Maithili": "mai", "Sanskrit": "sa", "Konkani": "gom", "Nepali": "ne",
    "Sindhi": "sd", "Dogri": "doi", "Manipuri": "mni", "Bodo": "brx",
    "Kashmiri": "ks", "Santali": "sat"
}

# MyMemory codes
MYMEMORY_CODES = {
    "Hindi": "hi", "Bengali": "bn", "Tamil": "ta", "Telugu": "te",
    "Malayalam": "ml", "Kannada": "kn", "Marathi": "mr", "Gujarati": "gu",
    "Odia": "or", "Punjabi": "pa", "Assamese": "as", "Urdu": "ur",
    "Nepali": "ne", "Sanskrit": "sa", "Maithili": "mai", "Sindhi": "sd"
}

class UltimateTranslator:
    def __init__(self, sarvam_api_key=None, gemini_api_key=None):
        self.gemini_key = gemini_api_key
        self.gemini_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        self.mymemory_url = "https://api.mymemory.translated.net/get"
        self.indictrans_url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
        self.session = requests.Session()
        
        self.stats = {"indictrans": 0, "gemini": 0, "mymemory": 0}
        
        print("\n" + "="*80)
        print("🌍 TRANSLATOR INITIALIZED - BEST FOR INDIAN LANGUAGES")
        print("="*80)
        print(f"1️⃣  IndicTrans2 API: ✅ FREE (AI4Bharat)")
        print(f"2️⃣  Gemini AI:       {'✅' if gemini_api_key else '❌'}")
        print(f"3️⃣  MyMemory:        ✅ FREE")
        print("="*80 + "\n")
    
    def translate_indictrans(self, text, target_language):
        """PRIMARY: IndicTrans2 API - BEST for Indian languages"""
        if target_language not in INDICTRANS_CODES:
            return None
        
        try:
            # IndicTrans2 API call
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": INDICTRANS_CODES[target_language]
                            }
                        }
                    }
                ],
                "inputData": {
                    "input": [{"source": text}]
                }
            }
            
            response = requests.post(
                self.indictrans_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'pipelineResponse' in result:
                    translation = result['pipelineResponse'][0]['output'][0]['target']
                    if translation and translation.strip():
                        self.stats["indictrans"] += 1
                        return translation.strip()
        except Exception as e:
            print(f"IndicTrans error: {str(e)[:50]}")
        
        return None
    
    def translate_gemini(self, text, target_language):
        """SECONDARY: Gemini AI"""
        if not self.gemini_key:
            return None
        
        try:
            url = f"{self.gemini_url}?key={self.gemini_key}"
            
            # Better prompt for Indian languages
            prompt = f"""Translate this English word/phrase to {target_language}. 
Provide only the direct translation in native script, no explanations.

English: {text}
{target_language}:"""
            
            response = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.1, "maxOutputTokens": 100}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    translation = result['candidates'][0]['content']['parts'][0]['text']
                    self.stats["gemini"] += 1
                    return translation.strip().strip('"\'')
        except:
            pass
        
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
    
    def translate(self, text, target_language):
        """Smart fallback: IndicTrans2 → Gemini → MyMemory"""
        text = text.strip()
        if not text:
            return "", "none"
        
        # 1. Try IndicTrans2 (BEST for Indian languages)
        result = self.translate_indictrans(text, target_language)
        if result:
            return result, "indictrans"
        
        # 2. Try Gemini AI
        result = self.translate_gemini(text, target_language)
        if result:
            return result, "gemini"
        
        # 3. Try MyMemory
        result = self.translate_mymemory(text, target_language)
        if result:
            return result, "mymemory"
        
        return "Translation unavailable", "none"
    
    def get_stats(self):
        total = sum(self.stats.values())
        if total == 0:
            return "No translations yet"
        
        return f"""Translation Usage:
• IndicTrans2: {self.stats['indictrans']} ({self.stats['indictrans']/total*100:.1f}%)
• Gemini AI: {self.stats['gemini']} ({self.stats['gemini']/total*100:.1f}%)
• MyMemory: {self.stats['mymemory']} ({self.stats['mymemory']/total*100:.1f}%)
• Total: {total} translations"""

_translator = None

def get_translator(sarvam_api_key=None, gemini_api_key=None):
    global _translator
    if _translator is None:
        _translator = UltimateTranslator(sarvam_api_key=None, gemini_api_key=gemini_api_key)
    return _translator
