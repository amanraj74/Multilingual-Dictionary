"""Language utilities for 22 Indian languages"""

def get_all_languages():
    """Return list of all 22 Indian languages"""
    return [
        "Hindi", "Bengali", "Tamil", "Telugu", "Malayalam", "Kannada",
        "Marathi", "Gujarati", "Odia", "Punjabi", "Assamese", "Urdu",
        "Maithili", "Sanskrit", "Konkani", "Nepali", "Sindhi", "Dogri",
        "Manipuri", "Bodo", "Kashmiri", "Santali"
    ]

def get_language_display_name(language):
    """Get native script name for display"""
    native_names = {
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
        "Sanskrit": "संस्कृतम्",
        "Konkani": "कोंकणी",
        "Nepali": "नेपाली",
        "Sindhi": "سنڌي",
        "Dogri": "डोगरी",
        "Manipuri": "মৈতৈলোন্",
        "Bodo": "बड़ो",
        "Kashmiri": "कॉशुर",
        "Santali": "ᱥᱟᱱᱛᱟᱲᱤ"
    }
    return native_names.get(language, language)
