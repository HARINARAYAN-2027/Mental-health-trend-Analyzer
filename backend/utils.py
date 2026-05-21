import os
import hashlib
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

def hash_password(password):
    """Simple SHA256 hashing for password safety"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(provided_password, stored_hash):
    """Password logging checking mechanism"""
    return hash_password(provided_password) == stored_hash

def save_uploaded_file(file):
    """CSV files directory validation mapping"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    if not file.filename.endswith('.csv'):
        return None
        
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return filepath

def read_csv_file(filepath):
    """Pandas CSV read handler module"""
    try:
        df = pd.read_csv(filepath)
        if 'text' not in df.columns:
            return None
        return df
    except Exception:
        return None

def generate_pdf_report(user, analyses):
    """ReportLab framework based static PDF generator module pipeline"""
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    filepath = os.path.join(reports_dir, f"Mental_Health_Trend_Analyzer_Report_{user['id']}.pdf")
    
    # Creating Canvas Layer Layout Configuration
    pdf = canvas.Canvas(filepath, pagesize=letter)
    pdf.setTitle("Mental Health Trend Analyzer Analytics Assessment Report")
    
    # Content Mapping Parameters
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(100, 740, "Mental Health Trend Analyzer Executive Analysis Summary")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 715, f"Profile Identity Subject: {user['username']} | Account Code: {user['id']}")
    pdf.drawString(100, 700, "Generation Protocol Standard: Local Pipeline Analytics Sandbox Engine")
    
    pdf.line(100, 685, 520, 685)
    
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 650, "Extracted Historical Sequence Data (Recent Logs)")
    
    y_position = 620
    pdf.setFont("Helvetica", 10)
    for idx, item in enumerate(analyses[:10]): # Limit logs overview up to 10 indices
        text_preview = item['text_content'][:45] + "..." if len(item['text_content']) > 45 else item['text_content']
        pdf.drawString(100, y_position, f"- {text_preview} | Sentiment: {item['sentiment']} | Risk: {item['risk_level']}")
        y_position -= 22
        if y_position < 100:
            pdf.showPage()
            y_position = 700
            
    pdf.save()
    return filepath

def get_random_quote():
    return "Mental health is not a destination, but a process. It's about how you drive, not where you're going."

def get_trending_topics():
    return [{"topic": "Exam Stress Relief Techniques", "volume": "High Trending"}]