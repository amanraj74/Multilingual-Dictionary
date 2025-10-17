"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
Production Version - Works on Localhost & Streamlit Cloud
"""

import streamlit as st
import sqlite3
import time
import os

# Safe imports with fallback
try:
    from translator import get_translator
    from utils.language_utils import get_all_languages, get_language_display_name
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Make sure all files are uploaded to GitHub")
    st.stop()

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
# CSS
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
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE INIT (CLOUD SAFE)
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_database():
    """Initialize database - works on cloud and localhost"""
    try:
        # Try to use existing database
        if os.path.exists('data/dictionary.db'):
            conn = sqlite3.connect('data/dictionary.db', check_same_thread=False)
            return conn
        else:
            # Create new in-memory database for cloud
            st.warning("⚠️ Database file not found. Creating temporary database.")
            conn = sqlite3.connect(':memory:', check_same_thread=False)
            
            # Create table
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    english TEXT NOT NULL,
                    category TEXT,
                    hindi TEXT, bengali TEXT, tamil TEXT, telugu TEXT, malayalam TEXT,
                    kannada TEXT, marathi TEXT, gujarati TEXT, odia TEXT, punjabi TEXT,
                    assamese TEXT, urdu TEXT, maithili TEXT, sanskrit TEXT, konkani TEXT,
                    nepali TEXT, sindhi TEXT, dogri TEXT, manipuri TEXT, bodo TEXT,
                    kashmiri TEXT, santali TEXT
                )
            ''')
            conn.commit()
            return conn
    except Exception as e:
        st.error(f"Database error: {e}")
        # Fallback to in-memory
        return sqlite3.connect(':memory:', check_same_thread=False)

db_conn = init_database()

# ═══════════════════════════════════════════════════════════════════════════════
# TRANSLATOR INIT (CLOUD SAFE)
# ═══════════════════════════════════════════════════════════════════════════════

if 'translator' not in st.session_state:
    st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">22 Indian Languages • 4 Translation Sources</p>', unsafe_allow_html=True)
    
    st.info("""
    ### 🚀 Quick Setup (Optional)
    
    **Get FREE API Keys:**
    - 🥇 **Sarvam AI** (Best for Indian languages): https://dashboard.sarvam.ai/
    - 🥈 **Gemini AI** (Google): https://makersuite.google.com/app/apikey
    
    💡 **Or skip** and use free MyMemory API!
    """)
    
    with st.expander("ℹ️ About Translation Sources", expanded=False):
        st.markdown("""
        **Translation Priority:**
        1. 🥇 **Sarvam AI** - Best quality for Indian languages (requires API key)
        2. 🥈 **Gemini AI** - Google's AI (requires API key)
        3. 🥉 **MyMemory** - Free, always available
        4. 🏅 **IndicTrans2 Model** - Offline backup (localhost only)
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sarvam_key = st.text_input(
            "🥇 Sarvam AI Key (Optional):",
            type="password",
            placeholder="Enter key or leave empty",
            help="Get from: https://dashboard.sarvam.ai/"
        )
    
    with col2:
        gemini_key = st.text_input(
            "🥈 Gemini AI Key (Optional):",
            type="password",
            placeholder="Enter key or leave empty",
            help="Get from: https://makersuite.google.com/app/apikey"
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🚀 Initialize with APIs", use_container_width=True, type="primary"):
            try:
                with st.spinner("Initializing..."):
                    st.session_state.translator = get_translator(
                        sarvam_api_key=sarvam_key.strip() if sarvam_key else None,
                        gemini_api_key=gemini_key.strip() if gemini_key else None
                    )
                    st.session_state.has_sarvam = bool(sarvam_key)
                    st.session_state.has_gemini = bool(gemini_key)
                    st.success("✅ Initialized with your API keys!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Trying with backup APIs...")
                try:
                    st.session_state.translator = get_translator()
                    st.session_state.has_sarvam = False
                    st.session_state.has_gemini = False
                    st.warning("⚠️ Using backup APIs only")
                    time.sleep(1)
                    st.rerun()
                except Exception as e2:
                    st.error(f"Critical error: {str(e2)}")
                    st.stop()
    
    with col_btn2:
        if st.button("⚡ Skip (Use Free API)", use_container_width=True):
            try:
                with st.spinner("Initializing free APIs..."):
                    st.session_state.translator = get_translator()
                    st.session_state.has_sarvam = False
                    st.session_state.has_gemini = False
                    st.success("✅ Free APIs ready!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
    
    with col_btn3:
        if st.button("ℹ️ More Info", use_container_width=True):
            st.info("""
            **Why use API keys?**
            - Better translation quality
            - Faster responses
            - More accurate for Indian languages
            
            **Free tier limits:**
            - MyMemory: 1000/day
            - Sarvam: Check their website
            - Gemini: 60/minute
            """)
    
    st.stop()

translator = st.session_state.translator

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">22 Languages • Auto-Save • Quality Verified</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📖 Dictionary", "🔄 Live Translate", "❓ Q&A", "📊 Statistics"])

# TAB 1: DICTIONARY WITH AUTO-SAVE
with tab1:
    st.markdown("## 📖 Smart Dictionary")
    st.info("🎯 Search any word - Auto-saves if not in database! Shows quality for each language ✅")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word = st.text_input(
            "Enter English word:",
            placeholder="e.g., butterfly, universe, technology...",
            key="dict_search"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True, type="primary")
    
    if search_btn and search_word:
        search_word = search_word.strip().lower()
        
        try:
            cursor = db_conn.cursor()
            cursor.execute('SELECT * FROM words WHERE LOWER(english) = ?', (search_word,))
            result = cursor.fetchone()
            
            if result:
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
                st.warning(f"⚠️ '{search_word}' not in database. Translating...")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                st.markdown(f"### 🔤 {search_word.title()} (Live Translation)")
                
                cols = st.columns(3)
                languages = get_all_languages()
                
                all_translations = {}
                translation_methods = {}
                quality_scores = {}
                
                for idx, lang in enumerate(languages):
                    status_text.text(f"Translating to {lang}... ({idx+1}/22)")
                    
                    try:
                        result_text, method = translator.translate(search_word, lang)
                        
                        is_success = not (
                            result_text.startswith("Translation unavailable") or
                            result_text.strip() == "" or
                            result_text.lower() == search_word.lower()
                        )
                        
                        all_translations[lang] = result_text
                        translation_methods[lang] = method
                        quality_scores[lang] = is_success
                        
                        with cols[idx % 3]:
                            native = get_language_display_name(lang)
                            
                            badge_info = {
                                "sarvam": ("🥇 Sarvam", "#10b981"),
                                "gemini": ("🥈 Gemini", "#3b82f6"),
                                "mymemory": ("🥉 MyMemory", "#f59e0b"),
                                "model": ("🏅 Model", "#8b5cf6")
                            }
                            badge_text, badge_color = badge_info.get(method, ("❓", "#6b7280"))
                            
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
                    
                    except Exception as e:
                        st.error(f"Error translating {lang}: {e}")
                
                progress_bar.empty()
                status_text.empty()
                
                # Quality Report
                success_count = sum(quality_scores.values())
                quality_percentage = (success_count / 22) * 100
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.metric("✅ Successful", f"{success_count}/22")
                
                with col_m2:
                    quality_color = "🟢" if quality_percentage >= 80 else "🟡" if quality_percentage >= 60 else "🔴"
                    st.metric("Quality Score", f"{quality_color} {quality_percentage:.1f}%")
                
                with col_m3:
                    failed_count = 22 - success_count
                    st.metric("❌ Failed", failed_count)
                
                # AUTO-SAVE
                st.markdown("---")
                
                if success_count >= 15:
                    st.success(f"✅ Quality good ({quality_percentage:.1f}%) - Auto-saving...")
                    
                    with st.spinner("💾 Saving to database..."):
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
                            
                            translations_to_save = []
                            for lang in languages:
                                trans = all_translations.get(lang, "")
                                if quality_scores.get(lang, False):
                                    translations_to_save.append(trans)
                                else:
                                    translations_to_save.append("")
                            
                            cursor.execute('''
                                INSERT INTO words (
                                    english, category, hindi, bengali, tamil, telugu, malayalam, kannada,
                                    marathi, gujarati, odia, punjabi, assamese, urdu, maithili, sanskrit,
                                    konkani, nepali, sindhi, dogri, manipuri, bodo, kashmiri, santali
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', tuple([search_word, "general"] + translations_to_save))
                            
                            db_conn.commit()
                            
                            cursor.execute('SELECT COUNT(*) FROM words')
                            new_count = cursor.fetchone()[0]
                            
                            st.success(f"✅ AUTO-SAVED: '{search_word}' with {success_count} translations!")
                            st.balloons()
                            st.info(f"📊 Database now has {new_count} words")
                            
                        except Exception as e:
                            st.error(f"Save error: {str(e)}")
                else:
                    st.warning(f"⚠️ Quality: {quality_percentage:.1f}% (too low). Not auto-saving.")
                    if st.button("🔄 Retranslate", use_container_width=True):
                        st.rerun()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# TAB 2: LIVE TRANSLATE
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
                try:
                    result, method = translator.translate(input_text, target_lang)
                    
                    badge = {
                        "sarvam": "🥇 Sarvam AI",
                        "gemini": "🥈 Gemini AI",
                        "mymemory": "🥉 MyMemory",
                        "model": "🏅 Model"
                    }.get(method, "")
                    
                    st.markdown(f"""
                    <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; border-radius: 15px; margin-top: 1rem;">
                        <p style="opacity: 0.8; margin-bottom: 0.5rem;">Via {badge}</p>
                        <h3>Translation ({target_lang}):</h3>
                        <p style="font-size: 2rem; font-weight: 600; margin-top: 1rem;">{result}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Translation error: {e}")

# TAB 3: Q&A
with tab3:
    st.markdown("## ❓ Q&A System")
    
    question = st.text_input("Ask:", placeholder="What is AI?")
    answer_lang = st.selectbox("Answer in:", get_all_languages(), key="qa_lang")
    
    if st.button("💬 Get Answer", key="qa"):
        if question:
            answer_en = "Artificial Intelligence is the simulation of human intelligence by machines."
            try:
                result, method = translator.translate(answer_en, answer_lang)
                
                st.markdown(f"""
                <div style="padding: 2rem; background: #f0f9ff; border-radius: 15px; border-left: 5px solid #3b82f6;">
                    <h4>Question:</h4>
                    <p>{question}</p>
                    <hr>
                    <h4>Answer ({answer_lang}):</h4>
                    <p style="font-size: 1.5rem; font-weight: 600;">{result}</p>
                    <p style="opacity: 0.7;">via {method}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

# TAB 4: STATISTICS
with tab4:
    st.markdown("## 📊 Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            cursor = db_conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM words')
            word_count = cursor.fetchone()[0]
            st.metric("📚 Dictionary Words", word_count)
        except:
            st.metric("📚 Dictionary Words", "N/A")
        
        st.metric("🌐 Languages", 22)
        st.metric("🔧 APIs", 4)
    
    with col2:
        try:
            stats = translator.get_stats()
            st.text_area("Translation Usage:", stats, height=200)
        except:
            st.info("No statistics yet")
    
    st.markdown("---")
    st.markdown("### 🔧 Active Sources")
    
    if st.session_state.get('has_sarvam'):
        st.success("🥇 Sarvam AI - Active")
    else:
        st.info("🥇 Sarvam AI - Not configured")
    
    if st.session_state.get('has_gemini'):
        st.success("🥈 Gemini AI - Active")
    else:
        st.info("🥈 Gemini AI - Not configured")
    
    st.success("🥉 MyMemory API - Always Active")

# SIDEBAR
with st.sidebar:
    st.markdown("## 🌟 System Info")
    
    try:
        cursor = db_conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM words')
        count = cursor.fetchone()[0]
        st.metric("Words", count)
    except:
        st.metric("Words", "N/A")
    
    st.metric("Languages", 22)
    
    st.markdown("---")
    st.markdown("### ✅ Features")
    st.markdown("""
    - 🥇 Sarvam AI
    - 🥈 Gemini AI
    - 🥉 MyMemory
    - 🏅 IndicTrans2
    - 💾 Auto-Save
    - 📊 Quality Check
    """)
    
    st.markdown("---")
    st.caption("🚀 v2.0 Production")
