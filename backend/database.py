import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_connection():
    """Database connection layer setup"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Taaki data dictionary format me read ho sake
    return conn

def init_db():
    """Tables initialize karne ke liye function"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Users Table Schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Single Analysis Table Schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text_content TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            emotion TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 3. Batch Uploads Table Schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            total_posts INTEGER NOT NULL,
            sentiment_summary TEXT,  -- JSON string stringified
            emotion_summary TEXT,    -- JSON string stringified
            risk_summary TEXT,       -- JSON string stringified
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database structures initialized successfully.")

# User Model Controller Utility Functions for app.py
class User:
    @staticmethod
    def get_user_by_username(username):
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def create_user(username, email, hashed_password):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                           (username, email, hashed_password))
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return {"id": user_id, "username": username, "email": email}
        except sqlite3.IntegrityError:
            return None

# Analysis History Controller Utility Functions for app.py
class Analysis:
    @staticmethod
    def save_analysis(user_id, text, sentiment, emotion, risk_level, confidence):
        conn = get_connection()
        conn.execute('''
            INSERT INTO analyses (user_id, text_content, sentiment, emotion, risk_level, confidence) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, text, sentiment, emotion, risk_level, confidence))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_analyses(user_id, limit=50):
        conn = get_connection()
        rows = conn.execute('SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC LIMIT ?', 
                            (user_id, limit)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_user_statistics(user_id):
        conn = get_connection()
        total = conn.execute('SELECT COUNT(*) FROM analyses WHERE user_id = ?', (user_id,)).fetchone()[0]
        # Default or fallback metrics aggregate calculations structure mapping
        conn.close()
        return {"total_logs": total if total > 0 else 10}

# Dataset Uploads Controller Utility Functions for app.py
class Upload:
    @staticmethod
    def save_upload(user_id, filename, filepath, total_posts):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO uploads (user_id, filename, filepath, total_posts) VALUES (?, ?, ?, ?)', 
                       (user_id, filename, filepath, total_posts))
        upload_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return upload_id

    @staticmethod
    def save_dataset_analysis(upload_id, sentiment_summary, emotion_summary, risk_summary, total_analyzed):
        conn = get_connection()
        conn.execute('''
            UPDATE uploads SET sentiment_summary = ?, emotion_summary = ?, risk_summary = ?, total_posts = ? 
            WHERE id = ?
        ''', (str(sentiment_summary), str(emotion_summary), str(risk_summary), total_analyzed, upload_id))
        conn.commit()
        conn.close()