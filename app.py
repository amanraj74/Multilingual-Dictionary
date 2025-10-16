"""
🌍 Multilingual Dictionary & QA System
Supports 22 Indic Languages
"""

import streamlit as st
import sqlite3
from translator import get_translator
from utils.language_utils import get_all_languages, get_language_display_name
import pandas as pd
import time


# Page config
st.set_page_config(
    page_title="Multilingual Dictionary - 22 Languages",
    page_icon="🌍",
    layout="wide"
)


# API Key Input (FIRST TIME ONLY)
if 'translator' not in st.session_state:
    st.markdown("## 🔑 Setup - One Time Only!")
    st.info("Get your FREE Gemini API key from: https://makersuite.google.com/app/apikey")
    
    api_key = st.text_input(
        "Paste your Gemini API Key here:",
        type="password",
        placeholder="AIzaSyAAhC6G2rMaK8RZ7vxyBV-R7VhAKm5vGjQ",
        help="FREE API with 60 requests/minute - supports all 22 languages"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Initialize System", use_container_width=True):
            if api_key:
                st.session_state.translator = get_translator(gemini_api_key=api_key)
                st.session_state.api_key = api_key
                st.success("✅ System initialized!")
                st.rerun()
            else:
                st.warning("⚠️ API key required. You can still use without it (will use backup APIs)")
                st.session_state.translator = get_translator()
                st.rerun()
    
    st.stop()

# Get translator from session
translator = st.session_state.translator

# Rest of your app.py code continues here...


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .language-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .translation-box {
        padding: 1rem;
        border-left: 4px solid #4ECDC4;
        background: #f8f9fa;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def init_translator():
    return get_translator()

@st.cache_resource
def get_db_connection():
    return sqlite3.connect('data/dictionary.db', check_same_thread=False)

translator = init_translator()
db_conn = get_db_connection()

# Header
st.markdown('<h1 class="main-header">🌍 Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown("### 22 Indic Languages Dictionary & Translation System")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📖 Dictionary", "🔄 Translate", "❓ Ask Question", "➕ Add Word"])

# TAB 1: SMART DICTIONARY (Shows ALL words!)
with tab1:
    st.markdown("## 📖 Smart Dictionary Lookup")
    st.info("🎯 Search our database OR get live translations for ANY word!")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word = st.text_input(
            "Enter English word:",
            placeholder="e.g., mango, computer, artificial intelligence, anything!",
            help="Works for ANY English word - not just database words!"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True)
    
    if search_btn and search_word:
        # First, try database
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM words WHERE english LIKE ?', (f'%{search_word}%',))
        results = cursor.fetchall()
        
        if results:
            # Found in database - show stored translations
            st.success(f"✅ Found in database!")
            
            for result in results:
                english = result[1]
                category = result[2]
                
                st.markdown(f"### 🔤 {english.title()}")
                st.caption(f"📂 Category: {category}")
                
                # Show all 22 language translations from database
                languages = get_all_languages()
                cols = st.columns(3)
                
                for idx, lang in enumerate(languages):
                    translation = result[3 + idx]
                    if translation:
                        with cols[idx % 3]:
                            native_name = get_language_display_name(lang)
                            st.markdown(f"""
                            <div class="translation-box">
                                <strong>{lang}</strong> ({native_name})<br>
                                <span class="translation-text">{translation}</span>
                            </div>
                            """, unsafe_allow_html=True)
        
        else:
            # NOT in database - get LIVE translations for ALL 22 languages!
            st.warning(f"⚠️ '{search_word}' not in database. Generating live translations...")
            
            with st.spinner("🌐 Translating to all 22 languages..."):
                st.markdown(f"### 🔤 {search_word.title()} (Live Translation)")
                st.caption("📡 Generated using AI translation")
                
                # Create columns for translations
                cols = st.columns(3)
                
                # Translate to ALL 22 languages
                languages = get_all_languages()
                
                for idx, lang in enumerate(languages):
                    with cols[idx % 3]:
                        # Get live translation
                        translation = translator.translate(search_word, lang)
                        native_name = get_language_display_name(lang)
                        
                        # Show translation
                        st.markdown(f"""
                        <div class="translation-box">
                            <strong>{lang}</strong> ({native_name})<br>
                            <span class="translation-text">{translation}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.1)
                
                st.success("✅ Live translations complete!")
                
                # Option to save to database
                st.markdown("---")
                if st.button("💾 Save these translations to database"):
                    # Create translations dict
                    translations_dict = {}
                    for lang in languages:
                        translation = translator.translate(search_word, lang)
                        translations_dict[lang] = translation
                        time.sleep(0.1)
                    
                    # Save to database
                    try:
                        from dictionary_builder import DictionaryBuilder
                        db = DictionaryBuilder()
                        success = db.add_word(search_word, translations_dict, "general")
                        db.close()
                        
                        if success:
                            st.success(f"✅ '{search_word}' saved to database!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to save")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")


# TAB 2: Translate
with tab2:
    st.markdown("## 🔄 Live Translation")
    st.info("Translate English text to any of 22 Indic languages using AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        input_text = st.text_area("Enter English text:", height=150, 
                                   placeholder="e.g., Good morning! How are you?")
    
    with col2:
        target_lang = st.selectbox("Target Language:", get_all_languages())
    
    translate_btn = st.button("🌐 Translate", key="translate")
    
    if translate_btn and input_text:
        with st.spinner(f"Translating to {target_lang}..."):
            try:
                translation = translator.translate(input_text, target_lang)
                
                st.markdown(f"""
                <div class="language-card">
                    <h3>📝 Original (English):</h3>
                    <p style="font-size: 1.2rem;">{input_text}</p>
                    <hr style="border-color: white;">
                    <h3>✨ Translation ({target_lang} - {get_language_display_name(target_lang)}):</h3>
                    <p style="font-size: 1.8rem;">{translation}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Translation error: {str(e)}")

# TAB 3: Ask Question
with tab3:
    st.markdown("## ❓ Ask Questions in Any Language")
    st.info("Ask a question in English and get answer in any Indic language")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        question = st.text_input("Ask your question:", placeholder="What is the capital of India?")
    
    with col2:
        answer_lang = st.selectbox("Answer Language:", get_all_languages(), key="answer_lang")
    
    ask_btn = st.button("💬 Get Answer", key="ask")
    
    if ask_btn and question:
        with st.spinner("Generating answer..."):
            try:
                # Simple QA (you can integrate with LLM here)
                # For now, translating the question to show functionality
                answer_english = f"The capital of India is New Delhi."  # Hardcoded for demo
                
                # Translate answer
                answer_translated = translator.translate(answer_english, answer_lang)
                
                st.markdown(f"""
                <div class="language-card">
                    <h3>❓ Question:</h3>
                    <p>{question}</p>
                    <hr style="border-color: white;">
                    <h3>✅ Answer in {answer_lang}:</h3>
                    <p style="font-size: 1.5rem;">{answer_translated}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# TAB 4: Add Word
with tab4:
    st.markdown("## ➕ Add New Word to Dictionary")
    
    english_word = st.text_input("English Word:")
    category = st.selectbox("Category:", ["vegetables", "fruits", "animals", "general"])
    
    st.markdown("### Translations:")
    
    translations = {}
    cols = st.columns(2)
    
    for idx, lang in enumerate(get_all_languages()[:12]):  # Show first 12
        with cols[idx % 2]:
            translations[lang] = st.text_input(f"{lang}:", key=f"trans_{lang}")
    
    add_btn = st.button("➕ Add to Dictionary")
    
    if add_btn and english_word:
        try:
            from dictionary_builder import DictionaryBuilder
            db = DictionaryBuilder()
            success = db.add_word(english_word, translations, category)
            db.close()
            
            if success:
                st.success(f"✅ Word '{english_word}' added successfully!")
            else:
                st.error("❌ Failed to add word")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("## 🌟 About")
    st.info("""
    **Multilingual Dictionary System**
    
    Supports 22 scheduled Indian languages:
    - Hindi, Bengali, Tamil, Telugu
    - Malayalam, Kannada, Marathi
    - Gujarati, Odia, Punjabi
    - Assamese, Urdu, Maithili
    - Sanskrit, Konkani, Nepali
    - Sindhi, Dogri, Manipuri
    - Bodo, Kashmiri, Santali
    
    **Features:**
    - Dictionary lookup
    - Real-time translation
    - Multilingual QA
    - Add custom words
    """)
    
    st.markdown("## 📊 Statistics")
    cursor = db_conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words')
    word_count = cursor.fetchone()[0]
    st.metric("Total Words", word_count)
    
    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("- IndicTrans2")
    st.markdown("- Streamlit")
    st.markdown("- AI4Bharat")
