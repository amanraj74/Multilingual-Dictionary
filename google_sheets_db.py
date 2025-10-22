"""Google Sheets Database Handler"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import time

def connect_to_sheet():
    """Connect to Google Sheet"""
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Multilingual_Dictionary").sheet1
        return sheet
    except Exception as e:
        st.error(f"❌ Google Sheets error: {e}")
        return None

def search_word(english_word):
    """Search for word"""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return None
        all_records = sheet.get_all_records()
        for record in all_records:
            if record.get('english', '').lower() == english_word.lower():
                return record
        return None
    except:
        return None

def save_word(english, category, translations):
    """Save word to sheet"""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return False
        
        existing = search_word(english)
        if existing:
            st.warning(f"'{english}' already exists!")
            return False
        
        row = [
            english, category,
            translations.get('hindi', ''), translations.get('bengali', ''),
            translations.get('tamil', ''), translations.get('telugu', ''),
            translations.get('malayalam', ''), translations.get('kannada', ''),
            translations.get('marathi', ''), translations.get('gujarati', ''),
            translations.get('odia', ''), translations.get('punjabi', ''),
            translations.get('assamese', ''), translations.get('urdu', ''),
            translations.get('maithili', ''), translations.get('sanskrit', ''),
            translations.get('konkani', ''), translations.get('nepali', ''),
            translations.get('sindhi', ''), translations.get('dogri', ''),
            translations.get('manipuri', ''), translations.get('bodo', ''),
            translations.get('kashmiri', ''), translations.get('santali', '')
        ]
        
        sheet.append_row(row)
        time.sleep(0.5)
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False

def get_total_words():
    """Get word count"""
    try:
        sheet = connect_to_sheet()
        if not sheet:
            return 0
        return len(sheet.get_all_records())
    except:
        return 0
