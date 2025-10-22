"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
Production Version with Google Sheets Database
Works on Localhost & Streamlit Cloud
"""

import streamlit as st
import time

# Import translator
try:
    from translator import get_translator
    from utils.language_utils import get_all_languages, get_language_display_name
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Import Google Sheets database
try:
    from google_sheets_db import search_word, save_word, get_total_words
    HAS_SHEETS = True
except ImportError:
    st.warning("⚠️ Google Sheets not configured. Using session state.")
    HAS_SHEETS = False

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
# TRANSLATOR INIT
# ═══════════════════════════════════════════════════════════════════════════════

if 'translator' not in st.session_state:
    st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">22 Indian Languages • Cloud Database</p>', unsafe_allow_html=True)
    
    st.info("""
    ### 🚀 Quick Setup (Optional)
    
    **Get FREE API Keys for better translations:**
    - 🥇 **Sarvam AI**: https://dashboard.sarvam.ai/
    - 🥈 **Gemini AI**: https://makersuite.google.com/app/apikey
    
    💡 **Or skip** and use free MyMemory API!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sarvam_key = st.text_input(
            "🥇 Sarvam AI Key (Optional):",
            type="password",
            placeholder="Leave empty to skip"
        )
    
    with col2:
        gemini_key = st.text_input(
            "🥈 Gemini AI Key (Optional):",
            type="password",
            placeholder="Leave empty to skip"
        )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🚀 Start with APIs", use_container_width=True, type="primary"):
            try:
                st.session_state.translator = get_translator(
                    sarvam_api_key=sarvam_key.strip() if sarvam_key else None,
                    gemini_api_key=gemini_key.strip() if gemini_key else None
                )
                st.session_state.has_sarvam = bool(sarvam_key)
                st.session_state.has_gemini = bool(gemini_key)
                st.success("✅ APIs initialized!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.translator = get_translator()
                st.session_state.has_sarvam = False
                st.session_state.has_gemini = False
                time.sleep(1)
                st.rerun()
    
    with col_btn2:
        if st.button("⚡ Skip (Use Free APIs)", use_container_width=True):
            try:
                st.session_state.translator = get_translator()
                st.session_state.has_sarvam = False
                st.session_state.has_gemini = False
                st.success("✅ Free APIs ready!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()
    
    st.stop()

translator = st.session_state.translator

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">22 Languages • Shared Cloud Database • Auto-Save</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📖 Dictionary", "🔄 Live Translate", "❓ Q&A", "📊 Statistics"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: DICTIONARY WITH GOOGLE SHEETS
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📖 Smart Dictionary")
    
    if HAS_SHEETS:
        st.info("🎯 Search any word - Auto-saves to Google Sheets! Everyone can see saved words.")
    else:
        st.warning("⚠️ Google Sheets not configured. Translations only (no saving).")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word_input = st.text_input(
            "Enter English word:",
            placeholder="e.g., butterfly, universe, technology...",
            key="dict_search"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True, type="primary")
    
    if search_btn and search_word_input:
        search_word_input = search_word_input.strip().lower()
        
        # Search in Google Sheets
        if HAS_SHEETS:
            with st.spinner("🔍 Searching database..."):
                result = search_word(search_word_input)
        else:
            result = None
        
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
            
            st.info(f"📊 Database: {stored_count}/22 translations | 🌐 Shared with all users")
        
        else:
            # Not in database - Generate translations
            st.warning(f"⚠️ '{search_word_input}' not in database. Generating live translations...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown(f"### 🔤 {search_word_input.title()} (Live Translation)")
            
            cols = st.columns(3)
            languages = get_all_languages()
            
            all_translations = {}
            translation_methods = {}
            quality_scores = {}
            
            # Translate all 22 languages
            for idx, lang in enumerate(languages):
                status_text.text(f"Translating to {lang}... ({idx+1}/22)")
                
                try:
                    result_text, method = translator.translate(search_word_input, lang)
                    
                    is_success = not (
                        result_text.startswith("Translation unavailable") or
                        result_text.strip() == "" or
                        result_text.lower() == search_word_input.lower()
                    )
                    
                    all_translations[lang] = result_text
                    translation_methods[lang] = method
                    quality_scores[lang] = is_success
                    
                    # Display translation
                    with cols[idx % 3]:
                        native = get_language_display_name(lang)
                        
                        badge_info = {
                            "indictrans": ("🥇 IndicTrans", "#10b981"),
                            "gemini": ("🥈 Gemini", "#3b82f6"),
                            "mymemory": ("🥉 MyMemory", "#f59e0b"),
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
            
            # AUTO-SAVE TO GOOGLE SHEETS
            st.markdown("---")
            
            if success_count >= 15:
                st.success(f"✅ Quality: {quality_percentage:.1f}% - Ready to save!")
                
                if HAS_SHEETS:
                    with st.spinner("💾 Saving to Google Sheets..."):
                        try:
                            # Prepare translations dict
                            translations_to_save = {}
                            for lang in languages:
                                db_key = lang.lower()
                                if quality_scores.get(lang, False):
                                    translations_to_save[db_key] = all_translations.get(lang, "")
                                else:
                                    translations_to_save[db_key] = ""
                            
                            # Save to Google Sheets
                            if save_word(search_word_input, "general", translations_to_save):
                                st.success(f"✅ AUTO-SAVED to Google Sheets: '{search_word_input}'!")
                                st.balloons()
                                
                                # Get updated word count
                                try:
                                    total = get_total_words()
                                    st.info(f"📊 Database now has {total} words | 🌐 Visible to everyone!")
                                except:
                                    st.info("📊 Saved successfully!")
                            else:
                                st.warning("⚠️ Word may already exist or save failed")
                        
                        except Exception as e:
                            st.error(f"Save error: {str(e)}")
                else:
                    st.warning("⚠️ Google Sheets not configured. Cannot save.")
            
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
                try:
                    result, method = translator.translate(input_text, target_lang)
                    
                    badge = {
                        "indictrans": "🥇 IndicTrans2 API",
                        "gemini": "🥈 Gemini AI",
                        "mymemory": "🥉 MyMemory",
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

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: Q&A
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## ❓ Q&A System")
    
    question = st.text_input("Ask:", placeholder="What is artificial intelligence?")
    answer_lang = st.selectbox("Answer in:", get_all_languages(), key="qa_lang")
    
    if st.button("💬 Get Answer", key="qa"):
        if question:
            answer_en = "Artificial Intelligence is the simulation of human intelligence by machines, enabling them to learn and solve problems."
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

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("## 📊 Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if HAS_SHEETS:
            try:
                word_count = get_total_words()
                st.metric("📚 Words in Database", word_count)
                st.caption("🌐 Shared across all users")
            except:
                st.metric("📚 Words in Database", "N/A")
        else:
            st.metric("📚 Words in Database", "Not configured")
        
        st.metric("🌐 Supported Languages", 22)
        st.metric("🔧 Translation Sources", 4)
    
    with col2:
        try:
            stats = translator.get_stats()
            st.text_area("API Usage:", stats, height=200)
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
    
    if HAS_SHEETS:
        st.success("☁️ Google Sheets Database - Connected")
    else:
        st.warning("☁️ Google Sheets Database - Not configured")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌟 System Info")
    
    if HAS_SHEETS:
        try:
            count = get_total_words()
            st.metric("Words", count)
            st.caption("☁️ Cloud Database")
        except:
            st.metric("Words", "N/A")
    else:
        st.metric("Words", "N/A")
        st.caption("⚠️ No database")
    
    st.metric("Languages", 22)
    st.metric("APIs", 4)
    
    st.markdown("---")
    
    st.markdown("### ✅ Features")
    st.markdown("""
    - 🥇 Sarvam AI
    - 🥈 Gemini AI
    - 🥉 MyMemory
    - 🏅 IndicTrans2
    - ☁️ Cloud Database
    - 💾 Auto-Save
    - 📊 Quality Check
    - 🌐 Shared Data
    """)
    
    st.markdown("---")
    st.caption("🚀 v2.1 - Google Sheets Edition")
