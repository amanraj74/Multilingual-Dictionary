"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
AUTO-LOAD VERSION - Saves ALL words to Google Sheets
"""

import streamlit as st
import time

# Safe imports
try:
    from translator import get_translator
    from utils.language_utils import get_all_languages, get_language_display_name
    from google_sheets_db import search_word, save_word, get_total_words
    HAS_SHEETS = True
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Multilingual Dictionary",
    page_icon="🌍",
    layout="wide"
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
# AUTO-INITIALIZE TRANSLATOR (NO SETUP PAGE!)
# ═══════════════════════════════════════════════════════════════════════════════

if 'translator' not in st.session_state:
    try:
        # Try to get API keys from Streamlit secrets
        sarvam_key = None
        hf_token = None
        
        try:
            sarvam_key = st.secrets["api_keys"]["sarvam_api_key"]
        except:
            pass
        
        try:
            hf_token = st.secrets["api_keys"]["huggingface_token"]
        except:
            pass
        
        # Initialize translator automatically
        st.session_state.translator = get_translator(
            sarvam_api_key=sarvam_key,
            huggingface_token=hf_token
        )
        
        st.session_state.has_sarvam = bool(sarvam_key)
        st.session_state.has_hf = bool(hf_token)
        
    except Exception as e:
        st.error(f"Initialization error: {e}")
        # Fallback to no API keys
        st.session_state.translator = get_translator()
        st.session_state.has_sarvam = False
        st.session_state.has_hf = False

translator = st.session_state.translator

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">22 Languages • Auto-Save ALL Words</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["📖 Dictionary", "📊 Database"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: DICTIONARY - AUTO-SAVE ALL WORDS
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📖 Smart Dictionary")
    st.info("🎯 Search any word - **Automatically saves ALL words** to Google Sheets!")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word_input = st.text_input(
            "Enter English word:",
            placeholder="e.g., potato, butterfly, computer...",
            key="dict_search"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True, type="primary")
    
    if search_btn and search_word_input:
        search_word_input = search_word_input.strip().lower()
        
        # Search in Google Sheets
        with st.spinner("🔍 Searching database..."):
            result = search_word(search_word_input)
        
        if result:
            # Found in database
            st.success("✅ Found in Google Sheets database!")
            
            english = result.get('english', search_word_input)
            category = result.get('category', 'general')
            
            st.markdown(f"### 🔤 {english.title()}")
            st.caption(f"📂 Category: {category}")
            
            languages = get_all_languages()
            cols = st.columns(3)
            
            stored_count = 0
            for idx, lang in enumerate(languages):
                translation = result.get(lang.lower(), '')
                if translation:
                    stored_count += 1
                    with cols[idx % 3]:
                        native = get_language_display_name(lang)
                        st.markdown(f"""
                        <div class="translation-box">
                            <strong>{lang}</strong> ({native})
                            <span style="display: inline-block; padding: 0.2rem 0.5rem; 
                                         background: #10b981; color: white; border-radius: 8px; 
                                         font-size: 0.7rem; margin-left: 0.5rem;">Saved</span><br>
                            <span class="translation-text">{translation}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.info(f"📊 Database: {stored_count}/22 translations")
        
        else:
            # Not in database - Translate & AUTO-SAVE ALL
            st.warning(f"⚠️ '{search_word_input}' not in database. Translating...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown(f"### 🔤 {search_word_input.title()} (Live Translation)")
            
            cols = st.columns(3)
            languages = get_all_languages()
            
            all_translations = {}
            translation_methods = {}
            success_count = 0
            
            # Translate all 22 languages
            for idx, lang in enumerate(languages):
                status_text.text(f"Translating to {lang}... ({idx+1}/22)")
                
                try:
                    result_text, method = translator.translate(search_word_input, lang)
                    
                    # Check if translation successful
                    is_success = not (
                        result_text.startswith("Translation unavailable") or
                        result_text.strip() == "" or
                        result_text.lower() == search_word_input.lower()
                    )
                    
                    all_translations[lang] = result_text
                    translation_methods[lang] = method
                    
                    if is_success:
                        success_count += 1
                    
                    # Display translation
                    with cols[idx % 3]:
                        native = get_language_display_name(lang)
                        
                        badge_info = {
                            "sarvam": ("🥇 Sarvam", "#10b981"),
                            "indictrans": ("🥈 IndicTrans", "#3b82f6"),
                            "fallback": ("🥉 Fallback", "#f59e0b")
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
                    all_translations[lang] = ""
            
            progress_bar.empty()
            status_text.empty()
            
            # Show stats
            quality_percentage = (success_count / 22) * 100
            
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.metric("✅ Successful", f"{success_count}/22")
            
            with col_m2:
                quality_color = "🟢" if quality_percentage >= 80 else "🟡" if quality_percentage >= 60 else "🔴"
                st.metric("Quality", f"{quality_color} {quality_percentage:.1f}%")
            
            # AUTO-SAVE ALL WORDS (NO QUALITY THRESHOLD!)
            st.markdown("---")
            st.info("💾 Auto-saving ALL words to database...")
            
            with st.spinner("💾 Saving to Google Sheets..."):
                try:
                    # Prepare translations dict - SAVE EVERYTHING including failed ones
                    translations_to_save = {}
                    for lang in languages:
                        db_key = lang.lower()
                        trans = all_translations.get(lang, "")
                        # Save even if empty or failed - just save what we got
                        translations_to_save[db_key] = trans
                    
                    # Save to Google Sheets
                    if save_word(search_word_input, "general", translations_to_save):
                        st.success(f"✅ SAVED: '{search_word_input}' with {success_count}/22 translations!")
                        st.balloons()
                        
                        try:
                            total = get_total_words()
                            st.info(f"📊 Database now has {total} words!")
                        except:
                            st.info("📊 Saved successfully!")
                    else:
                        st.warning("⚠️ Word may already exist in database")
                
                except Exception as e:
                    st.error(f"Save error: {str(e)}")
                    st.info("💡 Word may already be in database or there was a connection issue")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: DATABASE VIEW
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("## 📊 Database Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            word_count = get_total_words()
            st.metric("📚 Total Words", word_count)
        except:
            st.metric("📚 Total Words", "N/A")
    
    with col2:
        st.metric("🌐 Languages", 22)
    
    with col3:
        st.metric("💾 Auto-Save", "ALL Words")
    
    st.markdown("---")
    
    st.markdown("### 🔧 Active Translation Sources")
    
    if st.session_state.get('has_sarvam'):
        st.success("🥇 Sarvam AI - Active (Best quality)")
    else:
        st.info("🥇 Sarvam AI - Not configured")
    
    if st.session_state.get('has_hf'):
        st.success("🥈 IndicTrans2 - Active (Good quality)")
    else:
        st.info("🥈 IndicTrans2 - Not configured")
    
    st.success("🥉 Fallback - Always Active (Common words)")
    st.success("☁️ Google Sheets - Connected")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    1. **Search** any English word
    2. **Translates** to all 22 Indian languages
    3. **Auto-saves** to Google Sheets (no quality threshold!)
    4. **Everyone** can see saved words instantly
    5. **Never asks** for setup - API keys from secrets
    """)
    
    st.markdown("---")
    
    try:
        stats = translator.get_stats()
        st.text_area("Translation Usage:", stats, height=150)
    except:
        st.info("No statistics yet")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌟 Status")
    
    try:
        count = get_total_words()
        st.metric("Words", count)
    except:
        st.metric("Words", "N/A")
    
    st.metric("Languages", 22)
    st.metric("Auto-Save", "ON")
    
    st.markdown("---")
    
    st.markdown("### ✅ Features")
    st.markdown("""
    - 🥇 Sarvam AI
    - 🥈 IndicTrans2
    - 🥉 Fallback
    - ☁️ Google Sheets
    - 💾 Save ALL words
    - 🚀 Auto-initialize
    - 🌐 22 Languages
    """)
    
    st.markdown("---")
    st.caption("🚀 v3.0 - Auto-Save ALL")
