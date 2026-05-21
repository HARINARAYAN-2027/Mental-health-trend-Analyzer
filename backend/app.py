import os
import sys

# PROTECTION LAYER: Render runtime runtime environments path matching config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import nltk

# PRODUCTION BOOT FIX: Auto-download lexical corpora tokens if missing on cloud container
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Cloud Sandbox Setup: Fetching clean lexical NLTK arrays markers...")
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

import models
from database import User, Analysis, Upload, init_db, get_connection
from utils import (
    hash_password, verify_password, save_uploaded_file, 
    read_csv_file, generate_pdf_report, get_random_quote, 
    get_trending_topics, UPLOAD_FOLDER
)
import pandas as pd
import json
import sqlite3

app = Flask(__name__)

try:
    MentalHealthEngine = models.MentalHealthEngine
except AttributeError as e:
    raise ImportError("models.py does not define MentalHealthEngine") from e

# IMPORTANT: Cross-Origin Resource Sharing initialization for distributed ports layout
CORS(app)

# Core internal operational systems parameters
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check structures dependencies and execute initial schemas mapping
init_db()

# Local Machine Learning Parsing Core interface object instance
engine = MentalHealthEngine()

# Helper Utility Function: Frontend UI templates (Glassmorphism cards) 
# ko structural control color code dene ke liye backend metadata logic
def attach_ui_metadata(result):
    sentiment = result['sentiment']
    risk = result['risk_level']
    
    # Isse javascript api.js ko manual conditions nahi likhni padengi
    colors = {
        "sentiment_color": "#10b981" if sentiment == "Positive" else "#ef4444" if sentiment == "Negative" else "#94a3b8",
        "risk_color": "#ef4444" if risk == "High Risk" else "#f59e0b" if risk == "Moderate Risk" else "#10b981"
    }
    result.update(colors)
    return result

# ==================== 1. Authentication Routes ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """To securely register a new user in the SQLite database"""
    data = request.json or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    
    if not all([username, email, password, confirm_password]):
        return jsonify({"error": "All fields must be filled!"}), 400
    
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400
    
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400
    
    if User.get_user_by_username(username):
        return jsonify({"error": "This username is already taken."}), 400
    
    hashed = hash_password(password)
    user = User.create_user(username, email, hashed)
    
    if user:
        return jsonify({"message": "Registration complete successfully", "user": user}), 201
    else:
        return jsonify({"error": "This email is already registered."}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login check and standard verification layer"""
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400
    
    user = User.get_user_by_username(username)
    if not user or not verify_password(password, user['password']):
        return jsonify({"error": "Invalid username or password."}), 401
    
    return jsonify({
        "message": "Login authorization successful",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "email": user['email']
        },
        "token": f"token_secure_session_{user['id']}" 
    }), 200

# ==================== 2. Real-Time Text Analysis Routes ====================

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """To handle single line input box (Real-time analyzer UI)"""
    data = request.json or {}
    text = data.get('text')
    user_id = data.get('userId')
    
    if not text:
        return jsonify({"error": "Please enter some text!"}), 400
    
    if len(text.strip()) < 5:
        return jsonify({"error": "Please enter at least 5 characters for analysis."}), 400
    
    result = engine.analyze_sentiment(text)
    result = attach_ui_metadata(result)
    
    if user_id:
        try:
            Analysis.save_analysis(
                user_id=user_id,
                text=text,
                sentiment=result['sentiment'],
                emotion=result['emotion'],
                risk_level=result['risk_level'],
                confidence=result['confidence']
            )
        except Exception as e:
            print(f"Database tracking log error: {str(e)}")
    
    return jsonify(result), 200

@app.route('/api/user/<int:user_id>/analyses', methods=['GET'])
def get_user_analyses(user_id):
    """User's analytical history tracking layer"""
    limit = request.args.get('limit', 50, type=int)
    analyses = Analysis.get_user_analyses(user_id, limit)
    return jsonify(analyses), 200

@app.route('/api/user/<int:user_id>/statistics', methods=['GET'])
def get_user_stats(user_id):
    """To supply total numeric values to dashboard interface widgets"""
    stats = Analysis.get_user_statistics(user_id)
    return jsonify(stats), 200

# ==================== 3. Batch Processing (CSV File Upload) ====================

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Bulk dataset (.csv) file mapping and iteration automation pipelines"""
    if 'file' not in request.files:
        return jsonify({"error": "File object not found"}), 400
    
    file = request.files['file']
    user_id = request.form.get('userId')
    
    if not user_id:
        return jsonify({"error": "Session error: Valid User ID is required"}), 400
    
    if file.filename == '':
        return jsonify({"error": "No selected file detected"}), 400
    
    filepath = save_uploaded_file(file)
    if not filepath:
        return jsonify({"error": "Format issue: Use only standard .csv format!"}), 400
    
    df = read_csv_file(filepath)
    if df is None:
        return jsonify({"error": "CSV core file template parsing crash!"}), 400
    
    if len(df) == 0:
        return jsonify({"error": "Uploaded CSV file is empty."}), 400
    
    upload_id = Upload.save_upload(user_id, file.filename, filepath, len(df))
    
    results_array = []
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    emotion_counts = {}
    risk_counts = {'Low Risk': 0, 'Moderate Risk': 0, 'High Risk': 0}
    
    for idx, row in df.iterrows():
        text_content = row.get('text')
        if pd.isna(text_content):
            continue
        
        analysis_output = engine.analyze_sentiment(str(text_content))
        results_array.append(analysis_output)
        
        sentiment_counts[analysis_output['sentiment']] += 1
        risk_counts[analysis_output['risk_level']] += 1
        
        emo_tag = analysis_output['emotion']
        emotion_counts[emo_tag] = emotion_counts.get(emo_tag, 0) + 1
        
        Analysis.save_analysis(
            user_id=user_id,
            text=str(text_content),
            sentiment=analysis_output['sentiment'],
            emotion=analysis_output['emotion'],
            risk_level=analysis_output['risk_level'],
            confidence=analysis_output['confidence']
        )
    
    Upload.save_dataset_analysis(
        upload_id=upload_id,
        sentiment_summary=sentiment_counts,
        emotion_summary=emotion_counts,
        risk_summary=risk_counts,
        total_analyzed=len(results_array)
    )
    
    return jsonify({
        "message": "Dataset collection fully analyzed and synchronized.",
        "uploadId": upload_id,
        "total": len(results_array),
        "sentimentSummary": sentiment_counts,
        "riskSummary": risk_counts
    }), 200

# ==================== 4. Administrative Dashboard Live Metrics Synchronization ====================

@app.route('/api/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """Live SQLite database logs count metrics parser for charts.js pipelines"""
    user_id = request.args.get('userId', default=1, type=int)
    try:
        conn = get_connection() if 'get_connection' in globals() else sqlite3.connect(os.path.join(os.path.dirname(__abspath__), 'database.db'))
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ?", (user_id,))
        total_logs = cursor.fetchone()[0]

        if total_logs == 0:
            return jsonify({
                "total_logs": 0, "prevailing_risk": "Low Risk", "risk_color": "#10b981", "positive_ratio": 0,
                "counts": {"positive": 0, "negative": 0, "neutral": 0, "low_risk": 0, "mod_risk": 0, "high_risk": 0}
            }), 200

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND sentiment = 'Positive'", (user_id,))
        positive = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND sentiment = 'Negative'", (user_id,))
        negative = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND sentiment = 'Neutral'", (user_id,))
        neutral = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND risk_level = 'Low Risk'", (user_id,))
        low_risk = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND risk_level = 'Moderate Risk'", (user_id,))
        mod_risk = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND risk_level = 'High Risk'", (user_id,))
        high_risk = cursor.fetchone()[0]

        conn.close()

        positive_ratio = round((positive / total_logs) * 100) if total_logs > 0 else 0

        if high_risk >= mod_risk and high_risk > 0:
            prevailing_risk = "High Risk"
            risk_color = "#ef4444"
        elif mod_risk > 0:
            prevailing_risk = "Moderate"
            risk_color = "#f59e0b"
        else:
            prevailing_risk = "Low Risk"
            risk_color = "#10b981"

        return jsonify({
            "total_logs": total_logs,
            "prevailing_risk": prevailing_risk,
            "risk_color": risk_color,
            "positive_ratio": positive_ratio,
            "counts": {
                "positive": positive,
                "negative": negative,
                "neutral": neutral,
                "low_risk": low_risk,
                "mod_risk": mod_risk,
                "high_risk": high_risk
            }
        }), 200

    except Exception as e:
        print(f"Metrics engine extraction routine termination exception: {str(e)}")
        return jsonify({"error": "Failed to compute database system metrics context arrays"}), 500

# ==================== 5. Historical Trends Series Processing Endpoints ====================

@app.route('/api/trend-series', methods=['GET'])
def get_trend_series():
    """Fetches real-time timeline data points and high frequency density keywords from DB"""
    user_id = request.args.get('userId', default=1, type=int)
    try:
        conn = get_connection() if 'get_connection' in globals() else sqlite3.connect(os.path.join(os.path.dirname(__abspath__), 'database.db'))
        cursor = conn.cursor()

        # FIXED ALIGNMENT SCHEMA BUG: Changed column selection reference from 'text' to 'text_content'
        cursor.execute("SELECT text_content FROM analyses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

        exams_hits = 0
        stress_hits = 0
        lonely_hits = 0

        for row in rows:
            txt = str(row[0]).lower()
            if any(x in txt for x in ['exam', 'pressure', 'university', 'test', 'submission']):
                exams_hits += 1
            if any(x in txt for x in ['stress', 'stressed', 'tired', 'overwhelmed', 'work', 'mountain of stress']):
                stress_hits += 1
            if any(x in txt for x in ['hopeless', 'lonely', 'depressed', 'sad', 'stuck', 'lost']):
                lonely_hits += 1

        cursor.execute("SELECT emotion FROM analyses WHERE user_id = ? ORDER BY id ASC", (user_id,))
        emotions = [r[0] for r in cursor.fetchall()]
        conn.close()

        total = len(emotions)
        if total < 5:
            anxiety_series = [15, 22, 30, 25, 20]
            stress_series = [25, 28, 40, 35, 30]
            labels = ['P1', 'P2', 'P3', 'P4', 'P5']
        else:
            chunk = max(1, total // 5)
            anxiety_series = []
            stress_series = []
            labels = ['Interval 1', 'Interval 2', 'Interval 3', 'Interval 4', 'Interval 5']
            
            for i in range(5):
                subset = emotions[i*chunk : (i+1)*chunk]
                anxiety_series.append(sum(1 for e in subset if e == 'Anxiety') * 20 + 15)
                stress_series.append(sum(1 for e in subset if e in ['Stress', 'Sadness/Stress', 'Severe Distress']) * 25 + 20)

        return jsonify({
            "labels": labels,
            "anxiety_series": anxiety_series,
            "stress_series": stress_series,
            "keywords": {
                "exams": max(exams_hits, 0),
                "stress": max(stress_hits, 0),
                "lonely": max(lonely_hits, 0)
            }
        }), 200

    except Exception as e:
        print(f"Trend processing runtime crash exception: {str(e)}")
        return jsonify({"error": "Failed to extract dynamic time-series maps"}), 500

# ==================== 6. Dynamic Document Reporting Layer ====================

@app.route('/api/user/<int:user_id>/report/pdf', methods=['GET'])
def generate_report(user_id):
    """User logs aggregate trace report PDF on-demand routing endpoint"""
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Target user sequence not found"}), 404
    
    analyses = Analysis.get_user_analyses(user_id, limit=200)
    
    try:
        generated_path = generate_pdf_report(user, analyses)
        return send_file(generated_path, as_attachment=True, download_name=os.path.basename(generated_path))
    except Exception as e:
        return jsonify({"error": f"PDF processing routine exceptional termination: {str(e)}"}), 500

# ==================== 7. Utilities Metrics ====================

@app.route('/api/quote', methods=['GET'])
def get_quote():
    return jsonify({"quote": get_random_quote()}), 200

@app.route('/api/trending', methods=['GET'])
def get_trending():
    return jsonify({"topics": get_trending_topics()}), 200

@app.route('/api/health-check', methods=['GET'])
def health():
    return jsonify({
        "status": "Active",
        "system": "Mental Health Trend Analyzer AI Core Execution Sandbox",
        "port": 5000
    }), 200

# ==================== 8. Global Error Handling Router Modules ====================

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({"error": "Requested structural URL path not found on server context."}), 404

@app.errorhandler(500)
def structural_server_fault(error):
    return jsonify({"error": "Internal analytical engine thread structural fault exception execution layers."}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5000)
