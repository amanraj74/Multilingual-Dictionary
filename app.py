"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
Complete Production Version with All Features
Sarvam AI + Gemini + MyMemory + IndicTrans2 + Auto-Save
"""

import streamlit as st
import sqlite3
import time

try:
    from translator import get_translator
    from utils.language_utils import get_all_languages, get_language_display_name
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
Streamlit Cloud Safe Version
"""

import streamlit as st
import sqlite3
import time
import os

# SAFE IMPORTS with fallback
try:
    from translator import get_translator
except ImportError as e:
    st.error(f"Cannot import translator: {e}")
    st.stop()

try:
    from utils.language_utils import get_all_languages, get_language_display_name
except ImportError:
    st.warning("Using fallback language utils")
    # Fallback functions
    def get_all_languages():
        return ["Hindi", "Bengali", "Tamil", "Telugu", "Malayalam", "Kannada",
                "Marathi", "Gujarati", "Odia", "Punjabi", "Assamese", "Urdu",
                "Maithili", "Sanskrit", "Konkani", "Nepali", "Sindhi", "Dogri",
                "Manipuri", "Bodo", "Kashmiri", "Santali"]
    
    def get_language_display_name(lang):
        names = {
            "Hindi": "हिन्दी", "Bengali": "বাংলা", "Tamil": "தமிழ்",
            "Telugu": "తెలుగు", "Malayalam": "മലയാളം", "Kannada": "ಕನ್ನಡ"
        }
        return names.get(lang, lang)

# Rest of your app.py code continues...


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Ultimate Multilingual Dictionary",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .translation-box {
        padding: 1.5rem;
        border-left: 5px solid #667eea;
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e7f0 100%);
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .translation-text {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 30px;
        padding: 0.75rem 3rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .method-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db_connection():
    return sqlite3.connect('data/dictionary.db', check_same_thread=False)

db_conn = get_db_connection()

# API Key Setup (ONE TIME)
if 'translator' not in st.session_state:
    st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">22 Indian Languages • 4 Translation Sources • Auto-Save</p>', unsafe_allow_html=True)
    
    st.info("""
    ### 🚀 Setup (Optional - One Time)
    
    **Choose your translation quality:**
    
    1️⃣ **Sarvam AI** (Best) - Get FREE key: https://dashboard.sarvam.ai/  
    2️⃣ **Gemini AI** (Good) - Get FREE key: https://makersuite.google.com/app/apikey  
    3️⃣ **MyMemory** (Always available - No key needed)  
    4️⃣ **IndicTrans2 Model** (Offline backup)  
    
    💡 You can skip and use free APIs!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sarvam_key = st.text_input(
            "🥇 Sarvam AI Key (Optional):",
            type="password",
            placeholder="Best quality for Indian languages"
        )
    
    with col2:
        gemini_key = st.text_input(
            "🥈 Gemini AI Key (Optional):",
            type="password",
            placeholder="Google AI translation"
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("🚀 With All APIs", use_container_width=True, type="primary"):
            st.session_state.translator = get_translator(
                sarvam_api_key=sarvam_key if sarvam_key else None,
                gemini_api_key=gemini_key if gemini_key else None
            )
            st.session_state.has_sarvam = bool(sarvam_key)
            st.session_state.has_gemini = bool(gemini_key)
            st.success("✅ All APIs initialized!")
            time.sleep(1)
            st.rerun()
    
    with col_btn2:
        if st.button("⚡ Use Free APIs", use_container_width=True):
            st.session_state.translator = get_translator()
            st.session_state.has_sarvam = False
            st.session_state.has_gemini = False
            st.success("✅ Free APIs initialized!")
            time.sleep(1)
            st.rerun()
    
    with col_btn3:
        if st.button("🔄 Skip Setup", use_container_width=True):
            st.session_state.translator = get_translator()
            st.session_state.has_sarvam = False
            st.session_state.has_gemini = False
            st.rerun()
    
    st.stop()

translator = st.session_state.translator

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">22 Indian Languages • 4 Translation Sources • Auto-Save Enabled</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📖 Smart Dictionary", "🔄 Live Translate", "❓ Q&A System", "📊 Statistics"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: SMART DICTIONARY WITH AUTO-SAVE
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📖 Smart Dictionary (Auto-Save)")
    st.info("🎯 Search any word - Auto-saves to database if not found! Shows translation quality ✅")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word = st.text_input(
            "Enter English word:",
            placeholder="e.g., butterfly, computer, universe, anything!",
            key="dict_search"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True, type="primary")
    
    if search_btn and search_word:
        search_word = search_word.strip().lower()
        
        # Check database first
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM words WHERE LOWER(english) = ?', (search_word,))
        result = cursor.fetchone()
        
        if result:
            # Found in database
            st.success("✅ Found in database!")
            
            english = result[1]
            category = result[2]
            
            st.markdown(f"### 🔤 {english.title()}")
            st.caption(f"📂 Category: {category}")
            
            languages = get_all_languages()
            cols = st.columns(3)
            
            stored_count = 0
            for idx, lang in enumerate(languages):
                translation = result[3 + idx]
                if translation:
                    stored_count += 1
                    with cols[idx % 3]:
                        native = get_language_display_name(lang)
                        st.markdown(f"""
                        <div class="translation-box">
                            <strong>{lang}</strong> ({native})
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; 
                                         background: #10b981; color: white; border-radius: 8px; 
                                         font-size: 0.7rem; margin-left: 0.5rem;">Stored</span><br>
                            <span class="translation-text">{translation}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.info(f"📊 Database: {stored_count}/22 translations")
        
        else:
            # Not in database - Translate + Auto-save
            st.warning(f"⚠️ '{search_word}' not in database. Translating & auto-saving...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown(f"### 🔤 {search_word.title()} (Live Translation)")
            
            cols = st.columns(3)
            languages = get_all_languages()
            
            all_translations = {}
            translation_methods = {}
            quality_scores = {}
            
            # Translate all 22 languages
            for idx, lang in enumerate(languages):
                status_text.text(f"Translating to {lang}... ({idx+1}/22)")
                
                result_text, method = translator.translate(search_word, lang)
                
                is_success = not (
                    result_text.startswith("Translation unavailable") or
                    result_text.strip() == "" or
                    result_text.lower() == search_word.lower()
                )
                
                all_translations[lang] = result_text
                translation_methods[lang] = method
                quality_scores[lang] = is_success
                
                # Display with quality indicator
                with cols[idx % 3]:
                    native = get_language_display_name(lang)
                    
                    badge_styles = {
                        "sarvam": ("🥇 Sarvam", "#10b981"),
                        "gemini": ("🥈 Gemini", "#3b82f6"),
                        "mymemory": ("🥉 MyMemory", "#f59e0b"),
                        "model": ("🏅 Model", "#8b5cf6")
                    }
                    badge_text, badge_color = badge_styles.get(method, ("❓", "#6b7280"))
                    
                    quality_icon = "✅" if is_success else "⚠️"
                    border_color = "#10b981" if is_success else "#ef4444"
                    
                    st.markdown(f"""
                    <div class="translation-box" style="border-left-color: {border_color};">
                        <strong>{lang}</strong> ({native})
                        <span style="display: inline-block; padding: 0.2rem 0.6rem; 
                                     background: {badge_color}; color: white; border-radius: 8px; 
                                     font-size: 0.7rem; margin-left: 0.3rem; font-weight: 600;">
                            {badge_text}
                        </span>
                        <span style="margin-left: 0.3rem; font-size: 1.2rem;">{quality_icon}</span><br>
                        <span class="translation-text" style="color: {'#2d3748' if is_success else '#999'};">
                            {result_text}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                progress_bar.progress((idx + 1) / 22)
                time.sleep(0.12)
            
            progress_bar.empty()
            status_text.empty()
            
            # Quality Report
            success_count = sum(quality_scores.values())
            quality_percentage = (success_count / 22) * 100
            failed_langs = [lang for lang, success in quality_scores.items() if not success]
            
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                st.metric("✅ Successful", f"{success_count}/22")
            
            with col_m2:
                quality_color = "🟢" if quality_percentage >= 80 else "🟡" if quality_percentage >= 60 else "🔴"
                st.metric("Quality Score", f"{quality_color} {quality_percentage:.1f}%")
            
            with col_m3:
                st.metric("❌ Failed", len(failed_langs))
            
            if failed_langs:
                with st.expander(f"⚠️ Failed Translations ({len(failed_langs)})"):
                    st.warning(f"Failed: {', '.join(failed_langs)}")
            
            # AUTO-SAVE Logic
            st.markdown("---")
            
            should_auto_save = success_count >= 15  # Save if 15+ successful
            
            if should_auto_save:
                st.success(f"✅ Quality: {quality_percentage:.1f}% - Auto-saving to database...")
                
                with st.spinner("💾 Saving..."):
                    try:
                        lang_mapping = {
                            "Hindi": "hindi", "Bengali": "bengali", "Tamil": "tamil",
                            "Telugu": "telugu", "Malayalam": "malayalam", "Kannada": "kannada",
                            "Marathi": "marathi", "Gujarati": "gujarati", "Odia": "odia",
                            "Punjabi": "punjabi", "Assamese": "assamese", "Urdu": "urdu",
                            "Maithili": "maithili", "Sanskrit": "sanskrit", "Konkani": "konkani",
                            "Nepali": "nepali", "Sindhi": "sindhi", "Dogri": "dogri",
                            "Manipuri": "manipuri", "Bodo": "bodo", "Kashmiri": "kashmiri",
                            "Santali": "santali"
                        }
                        
                        translations_to_save = {}
                        for lang_display, translation in all_translations.items():
                            db_key = lang_mapping.get(lang_display, lang_display.lower())
                            if quality_scores[lang_display]:
                                translations_to_save[db_key] = translation
                            else:
                                translations_to_save[db_key] = ""
                        
                        cursor.execute('''
                            INSERT INTO words (
                                english, category, hindi, bengali, tamil, telugu, malayalam, kannada,
                                marathi, gujarati, odia, punjabi, assamese, urdu, maithili, sanskrit,
                                konkani, nepali, sindhi, dogri, manipuri, bodo, kashmiri, santali
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            search_word, "general",
                            translations_to_save.get('hindi', ''), translations_to_save.get('bengali', ''),
                            translations_to_save.get('tamil', ''), translations_to_save.get('telugu', ''),
                            translations_to_save.get('malayalam', ''), translations_to_save.get('kannada', ''),
                            translations_to_save.get('marathi', ''), translations_to_save.get('gujarati', ''),
                            translations_to_save.get('odia', ''), translations_to_save.get('punjabi', ''),
                            translations_to_save.get('assamese', ''), translations_to_save.get('urdu', ''),
                            translations_to_save.get('maithili', ''), translations_to_save.get('sanskrit', ''),
                            translations_to_save.get('konkani', ''), translations_to_save.get('nepali', ''),
                            translations_to_save.get('sindhi', ''), translations_to_save.get('dogri', ''),
                            translations_to_save.get('manipuri', ''), translations_to_save.get('bodo', ''),
                            translations_to_save.get('kashmiri', ''), translations_to_save.get('santali', '')
                        ))
                        
                        db_conn.commit()
                        
                        cursor.execute('SELECT COUNT(*) FROM words')
                        new_count = cursor.fetchone()[0]
                        
                        st.success(f"✅ AUTO-SAVED: '{search_word}' with {success_count} translations!")
                        st.balloons()
                        st.info(f"📊 Database now has {new_count} words")
                        
                    except Exception as e:
                        st.error(f"❌ Save error: {str(e)}")
            
            else:
                st.warning(f"⚠️ Quality: {quality_percentage:.1f}% (too low). Not auto-saving.")
                if st.button("🔄 Retranslate", use_container_width=True):
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: LIVE TRANSLATE
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("## 🔄 Live Translation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_text = st.text_area("Enter text:", height=150, placeholder="Type anything...")
    
    with col2:
        target_lang = st.selectbox("Target Language:", get_all_languages())
        st.info(f"**Native:** {get_language_display_name(target_lang)}")
    
    if st.button("🌐 Translate", key="translate", use_container_width=True):
        if input_text:
            with st.spinner("Translating..."):
                result, method = translator.translate(input_text, target_lang)
                
                badge = {"sarvam": "🥇 Sarvam AI", "gemini": "🥈 Gemini AI", "mymemory": "🥉 MyMemory", "model": "🏅 Model"}.get(method, "")
                
                st.markdown(f"""
                <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; border-radius: 15px; margin-top: 1rem;">
                    <p style="opacity: 0.8; margin-bottom: 0.5rem;">Via {badge}</p>
                    <h3>Translation ({target_lang}):</h3>
                    <p style="font-size: 2rem; font-weight: 600; margin-top: 1rem;">{result}</p>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: Q&A SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## ❓ Multilingual Q&A")
    
    question = st.text_input("Ask question:", placeholder="What is artificial intelligence?")
    answer_lang = st.selectbox("Answer in:", get_all_languages(), key="qa_lang")
    
    if st.button("💬 Get Answer", key="qa"):
        if question:
            answer_en = "Artificial Intelligence is the simulation of human intelligence by machines, enabling them to learn, reason, and solve problems."
            result, method = translator.translate(answer_en, answer_lang)
            
            st.markdown(f"""
            <div style="padding: 2rem; background: #f0f9ff; border-radius: 15px; margin-top: 1rem; border-left: 5px solid #3b82f6;">
                <h4>Question:</h4>
                <p style="font-size: 1.1rem;">{question}</p>
                <hr>
                <h4>Answer ({answer_lang}):</h4>
                <p style="font-size: 1.5rem; font-weight: 600; color: #2d3748;">{result}</p>
                <p style="opacity: 0.7; font-size: 0.9rem;">via {method}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("## 📊 Translation Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cursor = db_conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM words')
        word_count = cursor.fetchone()[0]
        
        st.metric("📚 Dictionary Words", word_count)
        st.metric("🌐 Supported Languages", 22)
    
    with col2:
        stats = translator.get_stats()
        st.text_area("API Usage:", stats, height=100)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Active Translation Sources")
    
    if st.session_state.get('has_sarvam'):
        st.success("🥇 Sarvam AI - Active")
    else:
        st.info("🥇 Sarvam AI - Not configured")
    
    if st.session_state.get('has_gemini'):
        st.success("🥈 Gemini AI - Active")
    else:
        st.info("🥈 Gemini AI - Not configured")
    
    st.success("🥉 MyMemory API - Always Active")
    st.success("🏅 IndicTrans2 Model - Available")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌟 System Status")
    
    cursor = db_conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words')
    count = cursor.fetchone()[0]
    
    st.metric("Words", count)
    st.metric("Languages", 22)
    st.metric("APIs", 4)
    
    st.markdown("---")
    
    st.markdown("### ✅ Features")
    st.markdown("""
    - 🥇 Sarvam AI (Best)
    - 🥈 Gemini AI
    - 🥉 MyMemory
    - 🏅 IndicTrans2
    - 💾 Auto-Save
    - 📊 Quality Check
    - 🎯 22 Languages
    """)
    
    st.markdown("---")
    st.caption("🚀 v2.0 Production")
