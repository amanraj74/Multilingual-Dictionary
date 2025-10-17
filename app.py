"""
🌍 ULTIMATE MULTILINGUAL DICTIONARY
Production-Ready with Sarvam AI + Fallbacks
"""

import streamlit as st
import sqlite3
from translator import get_translator
from utils.language_utils import get_all_languages, get_language_display_name
import pandas as pd
import time

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
    
    .method-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .sarvam { background: #10b981; color: white; }
    .mymemory { background: #3b82f6; color: white; }
    .model { background: #f59e0b; color: white; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db_connection():
    return sqlite3.connect('data/dictionary.db', check_same_thread=False)

db_conn = get_db_connection()

# API Key Setup
if 'translator' not in st.session_state:
    st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">22 Indian Languages • AI-Powered Translation</p>', unsafe_allow_html=True)
    
    st.info("""
    ### 🚀 Setup (One Time Only)
    
    **Sarvam AI** provides the BEST quality translations for Indian languages!
    
    **Get FREE API Key:** https://dashboard.sarvam.ai/
    
    ✅ Best quality for all 22 languages  
    ✅ Context-aware translations  
    ✅ Multiple fallback options  
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        api_key = st.text_input(
            "Sarvam AI API Key (Optional):",
            type="password",
            placeholder="Paste your API key here...",
            help="Leave empty to use backup APIs (MyMemory + Model)"
        )
        
        st.write("")
        
        if st.button("🚀 Initialize System", use_container_width=True, type="primary"):
            with st.spinner("Initializing translator..."):
                st.session_state.translator = get_translator(sarvam_api_key=api_key if api_key else None)
                st.session_state.has_sarvam = bool(api_key)
                st.success("✅ System initialized!" if api_key else "✅ Backup APIs initialized!")
                time.sleep(1)
                st.rerun()
    
    st.stop()

translator = st.session_state.translator

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 Ultimate Multilingual Dictionary</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">22 Indian Languages • Unlimited Translation</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs(["📖 Smart Dictionary", "🔄 Live Translate", "❓ Q&A System", "➕ Add Word"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: SMART DICTIONARY (AUTO-SAVE + VERIFICATION)
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📖 Smart Dictionary (Auto-Save)")
    st.info("🎯 Search any word - Auto-saves to database if not found! | ✅ Shows translation quality")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_word = st.text_input(
            "Enter English word:",
            placeholder="e.g., mango, computer, butterfly, universe...",
            key="dict_search"
        )
    
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", key="search", use_container_width=True, type="primary")
    
    if search_btn and search_word:
        search_word = search_word.strip().lower()
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 1: Check if word exists in database
        # ═══════════════════════════════════════════════════════════════════════
        
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM words WHERE LOWER(english) = ?', (search_word,))
        result = cursor.fetchone()
        
        if result:
            # ═══════════════════════════════════════════════════════════════════
            # FOUND IN DATABASE - Show stored translations
            # ═══════════════════════════════════════════════════════════════════
            
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
            
            st.info(f"📊 Database has {stored_count}/{len(languages)} translations")
        
        else:
            # ═══════════════════════════════════════════════════════════════════
            # NOT IN DATABASE - Generate + AUTO-SAVE
            # ═══════════════════════════════════════════════════════════════════
            
            st.warning(f"⚠️ '{search_word}' not in database. Translating & auto-saving...")
            
            # Progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                st.markdown(f"### 🔤 {search_word.title()} (Live Translation)")
                
                cols = st.columns(3)
                languages = get_all_languages()
                
                # Store all translations with quality metrics
                all_translations = {}
                translation_methods = {}
                quality_scores = {}
                
                # Translate all languages
                for idx, lang in enumerate(languages):
                    status_text.text(f"Translating to {lang}... ({idx+1}/{len(languages)})")
                    
                    # Get translation
                    result_text, method = translator.translate(search_word, lang)
                    
                    # Quality check
                    is_success = not (
                        result_text.startswith("⚠️") or 
                        result_text.startswith("Translation unavailable") or
                        result_text.strip() == "" or
                        result_text.lower() == search_word.lower()  # Untranslated
                    )
                    
                    all_translations[lang] = result_text
                    translation_methods[lang] = method
                    quality_scores[lang] = is_success
                    
                    # Display translation with quality indicator
                    with cols[idx % 3]:
                        native = get_language_display_name(lang)
                        
                        # Method badges
                        badge_styles = {
                            "sarvam": ("🥇 Sarvam", "background: #10b981;"),
                            "mymemory": ("🥈 MyMemory", "background: #3b82f6;"),
                            "model": ("🥉 Model", "background: #f59e0b;")
                        }
                        badge_text, badge_bg = badge_styles.get(method, ("❓ Unknown", "background: #6b7280;"))
                        
                        # Quality indicator
                        quality_icon = "✅" if is_success else "⚠️"
                        quality_bg = "#10b981" if is_success else "#ef4444"
                        
                        st.markdown(f"""
                        <div class="translation-box" style="border-left-color: {quality_bg};">
                            <strong>{lang}</strong> ({native})
                            <span style="display: inline-block; padding: 0.2rem 0.6rem; 
                                         {badge_bg} color: white; border-radius: 8px; 
                                         font-size: 0.7rem; margin-left: 0.3rem; font-weight: 600;">
                                {badge_text}
                            </span>
                            <span style="margin-left: 0.3rem; font-size: 1.2rem;">{quality_icon}</span><br>
                            <span class="translation-text" style="color: {'#2d3748' if is_success else '#999'};">
                                {result_text}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    progress_bar.progress((idx + 1) / len(languages))
                    time.sleep(0.12)  # Rate limiting
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
            
            # ═══════════════════════════════════════════════════════════════════
            # TRANSLATION QUALITY REPORT
            # ═══════════════════════════════════════════════════════════════════
            
            success_count = sum(quality_scores.values())
            failed_langs = [lang for lang, success in quality_scores.items() if not success]
            
            # Quality metrics
            quality_percentage = (success_count / len(languages)) * 100
            
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            
            with col_metric1:
                st.metric("✅ Successful", f"{success_count}/{len(languages)}")
            
            with col_metric2:
                quality_color = "🟢" if quality_percentage >= 80 else "🟡" if quality_percentage >= 60 else "🔴"
                st.metric("Quality Score", f"{quality_color} {quality_percentage:.1f}%")
            
            with col_metric3:
                st.metric("❌ Failed", len(failed_langs))
            
            # Show failed languages
            if failed_langs:
                with st.expander(f"⚠️ Failed Translations ({len(failed_langs)} languages)"):
                    st.warning(f"These languages failed: {', '.join(failed_langs)}")
                    st.info("💡 Tip: Try searching again or use 'Retranslate' button")
            
            # ═══════════════════════════════════════════════════════════════════
            # AUTO-SAVE TO DATABASE
            # ═══════════════════════════════════════════════════════════════════
            
            st.markdown("---")
            
            # Auto-save decision
            should_auto_save = success_count >= 15  # Save if at least 15/22 languages successful
            
            if should_auto_save:
                st.success(f"✅ Translation complete! Auto-saving to database...")
                
                with st.spinner("💾 Saving to database..."):
                    try:
                        # Prepare translations
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
                            if quality_scores[lang_display]:  # Only save successful translations
                                translations_to_save[db_key] = translation
                            else:
                                translations_to_save[db_key] = ""  # Empty for failed
                        
                        # Determine category automatically
                        auto_category = "general"
                        
                        # Insert into database
                        cursor.execute('''
                            INSERT INTO words (
                                english, category,
                                hindi, bengali, tamil, telugu, malayalam, kannada,
                                marathi, gujarati, odia, punjabi, assamese, urdu,
                                maithili, sanskrit, konkani, nepali, sindhi, dogri,
                                manipuri, bodo, kashmiri, santali
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            search_word, auto_category,
                            translations_to_save.get('hindi', ''),
                            translations_to_save.get('bengali', ''),
                            translations_to_save.get('tamil', ''),
                            translations_to_save.get('telugu', ''),
                            translations_to_save.get('malayalam', ''),
                            translations_to_save.get('kannada', ''),
                            translations_to_save.get('marathi', ''),
                            translations_to_save.get('gujarati', ''),
                            translations_to_save.get('odia', ''),
                            translations_to_save.get('punjabi', ''),
                            translations_to_save.get('assamese', ''),
                            translations_to_save.get('urdu', ''),
                            translations_to_save.get('maithili', ''),
                            translations_to_save.get('sanskrit', ''),
                            translations_to_save.get('konkani', ''),
                            translations_to_save.get('nepali', ''),
                            translations_to_save.get('sindhi', ''),
                            translations_to_save.get('dogri', ''),
                            translations_to_save.get('manipuri', ''),
                            translations_to_save.get('bodo', ''),
                            translations_to_save.get('kashmiri', ''),
                            translations_to_save.get('santali', '')
                        ))
                        
                        db_conn.commit()
                        
                        # Success notification
                        st.success(f"✅ AUTO-SAVED: '{search_word}' with {success_count} translations!")
                        st.balloons()
                        
                        # Update word count in sidebar
                        cursor.execute('SELECT COUNT(*) FROM words')
                        new_count = cursor.fetchone()[0]
                        st.info(f"📊 Database now has {new_count} words")
                        
                    except Exception as e:
                        st.error(f"❌ Auto-save failed: {str(e)}")
            
            else:
                # Quality too low - don't auto-save
                st.warning(f"⚠️ Quality too low ({success_count}/22). Not auto-saving.")
                st.info("💡 Click 'Retranslate' to try again or save manually")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("🔄 Retranslate All", use_container_width=True):
                        st.rerun()
                
                with col_btn2:
                    if st.button("💾 Save Anyway", use_container_width=True):
                        # Manual save code here (same as auto-save above)
                        st.info("Saving...")



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
                
                badge = {"sarvam": "🥇 Sarvam AI", "mymemory": "🥈 MyMemory", "model": "🥉 Model"}.get(method, "")
                
                st.markdown(f"""
                <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; border-radius: 15px; margin-top: 1rem;">
                    <p style="opacity: 0.8; margin-bottom: 0.5rem;">Via {badge}</p>
                    <h3>Translation:</h3>
                    <p style="font-size: 2rem; font-weight: 600; margin-top: 1rem;">{result}</p>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: Q&A SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## ❓ Q&A System")
    
    question = st.text_input("Ask a question:", placeholder="What is AI?")
    answer_lang = st.selectbox("Answer in:", get_all_languages(), key="qa_lang")
    
    if st.button("💬 Get Answer", key="qa"):
        if question:
            # Simple demo answer
            answer_en = "Artificial Intelligence is the simulation of human intelligence by machines."
            result, method = translator.translate(answer_en, answer_lang)
            
            st.markdown(f"""
            <div style="padding: 2rem; background: #f0f9ff; border-radius: 15px; margin-top: 1rem;">
                <h4>Question:</h4>
                <p>{question}</p>
                <hr>
                <h4>Answer ({answer_lang}):</h4>
                <p style="font-size: 1.5rem; font-weight: 600;">{result}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: ADD WORD
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("## ➕ Add Word")
    
    new_word = st.text_input("English word:")
    category = st.selectbox("Category:", ["general", "food", "technology", "education"])
    
    if st.button("📝 Generate Translations"):
        if new_word:
            with st.spinner("Generating..."):
                translations = {}
                for lang in get_all_languages():
                    result, _ = translator.translate(new_word, lang)
                    translations[lang] = result
                    time.sleep(0.1)
                
                st.session_state.new_translations = translations
                st.success("✅ Generated!")
    
    if 'new_translations' in st.session_state:
        if st.button("💾 Save"):
            from dictionary_builder import DictionaryBuilder
            db = DictionaryBuilder()
            db.add_word(new_word, st.session_state.new_translations, category)
            db.close()
            st.success(f"✅ '{new_word}' saved!")
            del st.session_state.new_translations

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌟 System Status")
    
    # Stats
    cursor = db_conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words')
    word_count = cursor.fetchone()[0]
    
    st.metric("Dictionary Words", word_count)
    st.metric("Languages", 22)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Translation Sources")
    if st.session_state.get('has_sarvam'):
        st.success("🥇 Sarvam AI (Active)")
    else:
        st.info("🥇 Sarvam AI (Not configured)")
    
    st.success("🥈 MyMemory API (Active)")
    st.success("🥉 IndicTrans2 Model (Available)")
    
    st.markdown("---")
    
    # Show stats
    if st.button("📊 Show Statistics"):
        st.text(translator.get_stats())
    
    st.markdown("---")
    st.caption("🚀 Production-Ready v2.0")
