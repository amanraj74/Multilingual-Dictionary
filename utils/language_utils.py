"""Language utilities for 22 Indic languages"""

# 22 Indic languages with IndicTrans2 codes
LANGUAGES = {
    "Hindi": "hin_Deva",
    "Bengali": "ben_Beng",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Malayalam": "mal_Mlym",
    "Kannada": "kan_Knda",
    "Marathi": "mar_Deva",
    "Gujarati": "guj_Gujr",
    "Odia": "ory_Orya",
    "Punjabi": "pan_Guru",
    "Assamese": "asm_Beng",
    "Urdu": "urd_Arab",
    "Maithili": "mai_Deva",
    "Sanskrit": "san_Deva",
    "Konkani": "gom_Deva",
    "Nepali": "npi_Deva",
    "Sindhi": "snd_Deva",
    "Dogri": "doi_Deva",
    "Manipuri": "mni_Mtei",
    "Bodo": "brx_Deva",
    "Kashmiri": "kas_Deva",
    "Santali": "sat_Olck"
}

# Language display names
LANGUAGE_NAMES = {
    "Hindi": "हिन्दी",
    "Bengali": "বাংলা",
    "Tamil": "தமிழ்",
    "Telugu": "తెలుగు",
    "Malayalam": "മലയാളം",
    "Kannada": "ಕನ್ನಡ",
    "Marathi": "मराठी",
    "Gujarati": "ગુજરાતી",
    "Odia": "ଓଡ଼ିଆ",
    "Punjabi": "ਪੰਜਾਬੀ",
    "Assamese": "অসমীয়া",
    "Urdu": "اردو",
    "Maithili": "मैथिली",
    "Sanskrit": "संस्कृत",
    "Konkani": "कोंकणी",
    "Nepali": "नेपाली",
    "Sindhi": "सिन्धी",
    "Dogri": "डोगरी",
    "Manipuri": "মৈতৈলোন্",
    "Bodo": "बर'",
    "Kashmiri": "कॉशुर",
    "Santali": "ᱥᱟᱱᱛᱟᱲᱤ"
}

def get_language_code(language_name):
    """Get IndicTrans2 code for language"""
    return LANGUAGES.get(language_name, "hin_Deva")

def get_all_languages():
    """Get list of all supported languages"""
    return list(LANGUAGES.keys())

def get_language_display_name(lang):
    """Get native language name"""
    return LANGUAGE_NAMES.get(lang, lang)
