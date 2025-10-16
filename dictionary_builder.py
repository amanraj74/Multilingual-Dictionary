"""
Dictionary Database Builder
SQLite database for multilingual dictionary
"""

import sqlite3
import json
import os

class DictionaryBuilder:
    def __init__(self, db_path="data/dictionary.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = None
        self.create_database()
    
    def create_database(self):
        """Create dictionary database"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create words table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                english TEXT NOT NULL UNIQUE,
                category TEXT,
                hindi TEXT,
                bengali TEXT,
                tamil TEXT,
                telugu TEXT,
                malayalam TEXT,
                kannada TEXT,
                marathi TEXT,
                gujarati TEXT,
                odia TEXT,
                punjabi TEXT,
                assamese TEXT,
                urdu TEXT,
                maithili TEXT,
                sanskrit TEXT,
                konkani TEXT,
                nepali TEXT,
                sindhi TEXT,
                dogri TEXT,
                manipuri TEXT,
                bodo TEXT,
                kashmiri TEXT,
                santali TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Database created")
    
    def load_from_json(self, json_path="data/common_words.json"):
        """Load words from JSON file"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cursor = self.conn.cursor()
        count = 0
        
        for category, words in data.items():
            for english, translations in words.items():
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO words (
                            english, category, hindi, bengali, tamil, telugu,
                            malayalam, kannada, marathi, gujarati, odia, punjabi,
                            assamese, urdu, maithili, sanskrit, konkani, nepali,
                            sindhi, dogri, manipuri, bodo, kashmiri, santali
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        english, category,
                        translations.get('hindi', ''),
                        translations.get('bengali', ''),
                        translations.get('tamil', ''),
                        translations.get('telugu', ''),
                        translations.get('malayalam', ''),
                        translations.get('kannada', ''),
                        translations.get('marathi', ''),
                        translations.get('gujarati', ''),
                        translations.get('odia', ''),
                        translations.get('punjabi', ''),
                        translations.get('assamese', ''),
                        translations.get('urdu', ''),
                        translations.get('maithili', ''),
                        translations.get('sanskrit', ''),
                        translations.get('konkani', ''),
                        translations.get('nepali', ''),
                        translations.get('sindhi', ''),
                        translations.get('dogri', ''),
                        translations.get('manipuri', ''),
                        translations.get('bodo', ''),
                        translations.get('kashmiri', ''),
                        translations.get('santali', '')
                    ))
                    count += 1
                except Exception as e:
                    print(f"Error inserting {english}: {e}")
        
        self.conn.commit()
        print(f"✅ Loaded {count} words")
    
    def search_word(self, english_word):
        """Search for a word"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM words WHERE english LIKE ?', (f'%{english_word}%',))
        return cursor.fetchall()
    
    def get_translation(self, english_word, language):
        """Get specific language translation"""
        cursor = self.conn.cursor()
        lang_col = language.lower()
        cursor.execute(f'SELECT {lang_col} FROM words WHERE english = ?', (english_word,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def add_word(self, english, translations, category="general"):
        """Add new word to dictionary"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO words (
                    english, category, hindi, bengali, tamil, telugu,
                    malayalam, kannada, marathi, gujarati, odia, punjabi,
                    assamese, urdu, maithili, sanskrit, konkani, nepali,
                    sindhi, dogri, manipuri, bodo, kashmiri, santali
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                english, category,
                translations.get('Hindi', ''),
                translations.get('Bengali', ''),
                translations.get('Tamil', ''),
                translations.get('Telugu', ''),
                translations.get('Malayalam', ''),
                translations.get('Kannada', ''),
                translations.get('Marathi', ''),
                translations.get('Gujarati', ''),
                translations.get('Odia', ''),
                translations.get('Punjabi', ''),
                translations.get('Assamese', ''),
                translations.get('Urdu', ''),
                translations.get('Maithili', ''),
                translations.get('Sanskrit', ''),
                translations.get('Konkani', ''),
                translations.get('Nepali', ''),
                translations.get('Sindhi', ''),
                translations.get('Dogri', ''),
                translations.get('Manipuri', ''),
                translations.get('Bodo', ''),
                translations.get('Kashmiri', ''),
                translations.get('Santali', '')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Initialize database
if __name__ == "__main__":
    db = DictionaryBuilder()
    db.load_from_json()
    print("✅ Dictionary database ready!")
    db.close()
