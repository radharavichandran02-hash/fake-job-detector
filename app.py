import streamlit as st
import pandas as pd
import os
import json
import re
import smtplib
import hashlib
import urllib.parse
import io
import base64
from datetime import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from deep_translator import GoogleTranslator, MyMemoryTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from langdetect import detect

# ==================== NEW: OCR SETUP ====================
try:
    import pytesseract
    from PIL import Image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False

# ==================== NEW: MATPLOTLIB FOR ANALYTICS ====================
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False

# ==================== CONFIGURATION (unchanged) ====================
SENDER_EMAIL = "project192003@gmail.com"
SENDER_PASSWORD = "zppgvmmtergdvzgs"
ADMIN_EMAIL = "project192003@gmail.com"
USERS_FILE = "users.json"

# SMART PATH - WORKS ON LAPTOP & PHONE
if os.path.exists("fake_job.csv"):
    DATASET_PATH = "fake_job.csv"
    print("✅ Using local file: fake_job.csv")
elif os.path.exists(r"C:\Users\Lenovo\Desktop\AI fake job\fake_job.csv"):
    DATASET_PATH = r"C:\Users\Lenovo\Desktop\AI fake job\fake_job.csv"
    print("✅ Using laptop path")
else:
    DATASET_PATH = "fake_job.csv"
    print("❌ Dataset not found! Please check location")

st.set_page_config(
    page_title="JobShield AI - Premium Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== NEW: SESSION STATE FOR HISTORY ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'history' not in st.session_state:
    st.session_state.history = []  # for scan history
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = True

# ==================== PREMIUM CSS (Light Purple Background) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    
    * { font-family: 'Inter', sans-serif !important; }
    
    /* Light Purple Background */
    .stApp {
        background: linear-gradient(145deg, #f3e8ff, #e9d9ff, #f3e8ff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    p, span, label, div, h1, h2, h3, h4, h5, li {
        color: #1e1e3f !important;
    }
    .hero-sub {
        color: #4a4a6a !important;
    }
    
    .hero-premium {
        text-align: center;
        padding: 2rem 0;
        animation: fadeInDown 1s ease;
    }
    
    .hero-title-premium {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6b21a5, #9333ea, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 300% 300%;
        animation: gradientShift 5s ease infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-sub-premium {
        color: #6b21a5 !important;
        font-size: 1.2rem;
        animation: fadeInUp 1s ease 0.3s both;
    }
    
    /* Glass Card - Login/Register Box */
    .glass-card-premium {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(155, 77, 202, 0.3);
        border-radius: 30px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 20px 50px rgba(106, 27, 154, 0.3);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease;
    }
    
    .glass-card-premium:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(106, 27, 154, 0.4);
        border-color: rgba(155, 77, 202, 0.6);
    }
    
    .fake-banner-premium {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        animation: pulse 2s infinite, slideIn 0.5s ease;
        box-shadow: 0 0 50px rgba(255, 65, 108, 0.5);
        margin: 1rem 0;
    }
    
    .genuine-banner-premium {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        animation: slideIn 0.5s ease;
        box-shadow: 0 0 50px rgba(56, 239, 125, 0.4);
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fake-banner-premium h2,
    .fake-banner-premium p,
    .genuine-banner-premium h2,
    .genuine-banner-premium p {
        color: white !important;
    }
    
    .stats-card-premium {
        background: linear-gradient(135deg, #8b5cf6, #a78bfa);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        animation: float 3s ease infinite;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .stats-card-premium h3,
    .stats-card-premium p {
        color: white !important;
    }
    
    .risk-badge-premium {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #fca5a5 !important;
        border-radius: 30px;
        padding: 0.4rem 1.2rem;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
        animation: badgePop 0.3s ease;
    }
    
    @keyframes badgePop {
        0% { transform: scale(0); }
        80% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #8b5cf6, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(139, 92, 246, 0.4) !important;
        border-radius: 15px !important;
        color: #1a1a2e !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3) !important;
        transform: scale(1.02);
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(106, 27, 154, 0.2) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(155, 77, 202, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1e1e3f !important;
    }
    
    .sidebar-user-premium {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        animation: slideInRight 0.5s ease;
    }
    
    .sidebar-user-premium p {
        color: white !important;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .email-alert-premium {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(168, 85, 247, 0.2));
        border-left: 5px solid #8b5cf6;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .site-card-premium {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInScale 0.5s ease;
    }
    
    .site-card-premium:hover {
        transform: scale(1.05) rotateY(5deg);
        border-color: #8b5cf6;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .site-card-premium a {
        color: #8b5cf6 !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        display: block;
        margin-top: 0.5rem;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6, #a855f7) !important;
        border-radius: 10px !important;
        transition: width 1s ease !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        border-radius: 50px;
        padding: 0.3rem;
        gap: 0.5rem;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #1e1e3f !important;
        font-weight: 600;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #8b5cf6, #a855f7) !important;
        color: white !important;
        transform: scale(1.05);
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #8b5cf6, #a855f7, transparent);
        margin: 2rem 0;
    }
    
    .footer-premium {
        text-align: center;
        color: #6b21a5 !important;
        padding: 2rem;
        font-size: 0.85rem;
        position: relative;
        overflow: hidden;
    }
    
    .footer-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #8b5cf6, #a855f7, transparent);
        animation: slide 3s infinite;
    }
    
    @keyframes slide {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .loading-premium {
        text-align: center;
        padding: 2rem;
    }
    
    .loading-premium::after {
        content: '🔍';
        font-size: 3rem;
        animation: spin 1s linear infinite;
        display: inline-block;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .admin-badge {
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        z-index: 999;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* ===== Share button styles ===== */
    .share-button {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        color: white !important;
        border: none;
        border-radius: 40px;
        padding: 0.6rem 1.2rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin: 0.2rem;
        transition: all 0.3s ease;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
    }
    
    .share-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
    }
    
    /* ===== Light Purple File Uploader ===== */
    div[data-testid="stFileUploader"] {
        background: #f3e8ff !important;
        border: 2px dashed #8b5cf6 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
    }
    
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
        background: #f3e8ff !important;
    }
    
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] div {
        color: #4a1d6d !important;
    }
    
    /* ===== Site Card for Trusted Sites ===== */
    .site-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .site-card:hover {
        transform: translateY(-5px);
        border-color: #8b5cf6;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
    }
    
    .site-card img {
        border-radius: 8px;
        margin-bottom: 8px;
    }
    
    .site-card a {
        color: #8b5cf6 !important;
        text-decoration: none;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== OCR CLEANING FUNCTION ====================
def clean_ocr_text(text):
    """Remove common OCR artifacts like keyboard_arrowright, arrows, etc."""
    artifacts = [
        'keyboard_arrowright', 'keyboard_arrowleft', 'arrow_forward',
        'arrow_back', 'arrow_upward', 'arrow_downward', 'chevron_right',
        'chevron_left', '➡️', '⬅️', '⬆️', '⬇️', '▶️', '◀️',
        'keyboard_arrow_right', 'keyboard_arrow_left',
        'keyToaid', 'Entroweight', 'keyToaid Entroweight'
    ]
    cleaned = text
    for artifact in artifacts:
        cleaned = cleaned.replace(artifact, '')
    # Remove extra blank lines
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    return '\n'.join(lines)

# ==================== ADMIN ALERT FUNCTION ====================
def send_admin_alert(user_email, user_name, action="login"):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"👤 User {action.capitalize()} Alert - JobShield AI"
        msg['From'] = SENDER_EMAIL
        msg['To'] = ADMIN_EMAIL
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#1a1a2e;font-family:'Inter',sans-serif;">
            <div style="max-width:600px;margin:30px auto;padding:20px;">
                <div style="background:linear-gradient(135deg,#8b5cf6,#a855f7);border-radius:20px;padding:2rem;text-align:center;margin-bottom:20px;">
                    <h1 style="color:white;margin:0;">🛡️ JobShield AI</h1>
                    <p style="color:rgba(255,255,255,0.9);margin:5px 0 0;">User Activity Alert</p>
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;">
                    <h2 style="color:#a855f7;margin:0 0 20px;">🔔 New User {action.capitalize()}</h2>
                    
                    <div style="background:rgba(139,92,246,0.1);border-radius:15px;padding:1.5rem;margin:10px 0;">
                        <p style="color:#e2e8f0;margin:10px 0;"><strong>👤 User:</strong> {user_name}</p>
                        <p style="color:#e2e8f0;margin:10px 0;"><strong>📧 Email:</strong> {user_email}</p>
                        <p style="color:#e2e8f0;margin:10px 0;"><strong>⏰ Time:</strong> {current_time}</p>
                        <p style="color:#e2e8f0;margin:10px 0;"><strong>📍 Action:</strong> {action}</p>
                    </div>
                    
                    <div style="background:rgba(255,215,0,0.1);border-left:4px solid #ffd700;border-radius:10px;padding:1rem;margin:20px 0;">
                        <p style="color:#ffd700;margin:0;">⚠️ User has accessed the JobShield AI platform</p>
                    </div>
                </div>
                
                <div style="text-align:center;margin-top:20px;">
                    <p style="color:#475569;font-size:0.8rem;">🛡️ JobShield AI v2.0 - Security Monitoring System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, ADMIN_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Admin alert failed: {e}")
        return False

# ==================== USER MANAGEMENT ====================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password):
    users = load_users()
    if email in users:
        return False, "Email already registered!"
    users[email] = {"name": name, "password": hash_password(password), "email": email}
    save_users(users)
    return True, "Registration successful!"

def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "Email not found!"
    if users[email]['password'] != hash_password(password):
        return False, "Wrong password!"
    return True, users[email]['name']

# ==================== ENHANCED EMAIL FUNCTION ====================
def send_email_alert(to_email, user_name, job_text, result, score, suggestions,
                     trigger_hits, detected_lang="en", translated_text=""):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🛡️ JobShield AI - {'⚠️ FAKE JOB DETECTED' if result == 'FAKE' else '✅ Genuine Job Verified'}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        is_fake = (result == "FAKE")
        banner_grad = "linear-gradient(135deg,#ff416c,#ff4b2b)" if is_fake else "linear-gradient(135deg,#11998e,#38ef7d)"
        status_label = "⚠️ FAKE JOB DETECTED" if is_fake else "✅ LIKELY GENUINE JOB"
        score_label = f"Fraud Probability: {score:.1f}%" if is_fake else f"Safety Score: {100-score:.1f}%"
        warning_line = "⛔ Do NOT apply or pay any money for this job!" if is_fake else "Still verify company details before applying."
        
        lang_map = {
            'ta':'Tamil','hi':'Hindi','en':'English','ar':'Arabic','zh-cn':'Chinese',
            'es':'Spanish','fr':'French','de':'German','ja':'Japanese','ko':'Korean',
            'ru':'Russian','pt':'Portuguese','id':'Indonesian','tr':'Turkish',
            'bn':'Bengali','vi':'Vietnamese','th':'Thai','ur':'Urdu',
        }
        lang_display = lang_map.get(detected_lang, detected_lang.upper())
        
        sugg_rows = "".join([
            f"<tr><td style='padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.07);color:#e2e8f0;'>{s}</td></tr>"
            for s in suggestions
        ])
        
        badge_html = ""
        if trigger_hits:
            for t in trigger_hits:
                badge_html += f"<span style='display:inline-block;background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.5);color:#fca5a5;border-radius:30px;padding:5px 15px;margin:3px;font-size:0.85rem;'>{t}</span>"
        else:
            badge_html = "<span style='color:#94a3b8;'>✅ No major risk keywords found</span>"
        
        translation_block = ""
        if detected_lang != 'en' and translated_text:
            translation_block = f"""
            <div style="background:rgba(139,92,246,0.1);border-radius:15px;padding:1rem;margin:15px 0;border-left:4px solid #8b5cf6;">
                <p style="color:#8b5cf6;font-weight:600;margin:0 0 5px;">📝 English Translation</p>
                <p style="color:#94a3b8;margin:0;">{translated_text[:400]}{'...' if len(translated_text)>400 else ''}</p>
            </div>"""
        
        job_preview = job_text[:300] + ("..." if len(job_text) > 300 else "")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#1a1a2e;font-family:'Inter',sans-serif;">
            <div style="max-width:600px;margin:30px auto;padding:20px;">
                <div style="text-align:center;margin-bottom:30px;">
                    <h1 style="background:linear-gradient(90deg,#8b5cf6,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5rem;margin:0;">🛡️ JobShield AI</h1>
                    <p style="color:#94a3b8;">Fake Job Detection Report</p>
                </div>
                
                <p style="color:#e2e8f0;">Hello <strong style="color:#8b5cf6;">{user_name}</strong>,</p>
                
                <div style="background:{banner_grad};border-radius:24px;padding:2rem;text-align:center;margin:20px 0;box-shadow:0 0 30px {'#ff416c' if is_fake else '#11998e'}80;">
                    <h2 style="color:white;margin:0;">{status_label}</h2>
                    <p style="color:white;font-size:1.2rem;margin:10px 0;"><strong>{score_label}</strong></p>
                    <p style="color:rgba(255,255,255,0.9);">{warning_line}</p>
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:1.5rem;margin:15px 0;">
                    <p style="color:#8b5cf6;font-weight:700;">🌍 Language Analysis</p>
                    <p style="color:#e2e8f0;">Detected Language: <strong style="color:#a855f7;">{lang_display}</strong></p>
                    {translation_block}
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:1.5rem;margin:15px 0;">
                    <p style="color:#f87171;font-weight:700;">⚠️ Risk Indicators</p>
                    <div>{badge_html}</div>
                </div>
                
                <div style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);border-radius:20px;padding:1.5rem;margin:15px 0;">
                    <p style="color:#a78bfa;font-weight:700;">💡 Recommendations</p>
                    <table style="width:100%;border-collapse:collapse;">{sugg_rows}</table>
                </div>
                
                <div style="background:rgba(255,255,255,0.03);border-radius:15px;padding:1rem;margin:15px 0;">
                    <p style="color:#64748b;font-size:0.85rem;">📋 ANALYZED JOB PREVIEW</p>
                    <p style="color:#94a3b8;">{job_preview}</p>
                </div>
                
                <div style="text-align:center;margin-top:30px;">
                    <p style="color:#475569;font-size:0.8rem;">🛡️ JobShield AI v2.0 · Protecting Job Seekers Worldwide</p>
                </div>
            </div>
        </body>
        </html>"""
        
        msg.attach(MIMEText(html, 'html'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False

# ==================== MODEL TRAINING ====================
@st.cache_resource
def train_model():
    try:
        try:
            df = pd.read_excel(DATASET_PATH, engine='openpyxl')
        except Exception:
            df = None
            
        if df is None or df.shape[0] < 10:
            for enc in ['utf-8', 'latin1', 'cp1252']:
                try:
                    df = pd.read_csv(DATASET_PATH, encoding=enc, engine='python', on_bad_lines='skip')
                    if df.shape[0] > 10:
                        break
                except Exception:
                    continue
        
        text_cols = [c for c in ['description','company_profile','requirements','benefits','title'] if c in df.columns]
        if not text_cols:
            return None, None
            
        df['_text'] = df[text_cols].fillna('').astype(str).agg(' '.join, axis=1).str.strip()
        df = df[df['_text'].str.len() > 10]
        
        label_col = next((c for c in ['fraudulent','label','fake','fraud'] if c in df.columns), df.columns[-1])
        df = df[['_text', label_col]].copy()
        df.columns = ['description', 'fraudulent']
        
        df['fraudulent'] = df['fraudulent'].astype(str).str.lower().str.strip()
        df['fraudulent'] = df['fraudulent'].replace(
            {'fake':1,'real':0,'genuine':0,'1':1,'0':0,'1.0':1,'0.0':0,'true':1,'false':0}
        )
        df = df[df['fraudulent'].isin([0,1])].dropna()
        df['fraudulent'] = df['fraudulent'].astype(int)
        
        fake = df[df['fraudulent']==1]
        real = df[df['fraudulent']==0]
        n = min(len(fake), len(real))
        df_bal = pd.concat([fake.sample(n, random_state=42), real.sample(n, random_state=42)])
        
        vec = TfidfVectorizer(stop_words='english', max_features=5000, min_df=1)
        X = vec.fit_transform(df_bal['description'].astype(str))
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X, df_bal['fraudulent'])
        
        return model, vec
    except Exception:
        return None, None

model, vectorizer = train_model()

# ==================== TRANSLATION FUNCTION ====================
def translate_to_english(text):
    try:
        detected_lang = detect(text)
    except Exception:
        detected_lang = "unknown"
        
    if detected_lang == 'en':
        return text, 'en'
        
    for Translator in [GoogleTranslator, MyMemoryTranslator]:
        try:
            r = Translator(source='auto', target='en').translate(text)
            if r and len(r.strip()) > 5 and r.strip() != text.strip():
                return r, detected_lang
        except Exception:
            pass
    return text, detected_lang

# ==================== JOB ANALYSIS FUNCTION ====================
def analyze_job(job_text):
    if not job_text or model is None:
        return None
        
    try:
        translated, detected_lang = translate_to_english(job_text)
        
        trigger_keywords = {
            'urgent': '🚨 Urgent Hiring',
            'immediate': '⚡ Immediate Joining',
            'work from home': '🏠 Work From Home',
            'part time': '⏰ Part Time',
            'registration fee': '💰 Registration Fee',
            'processing fee': '💳 Processing Fee',
            'advance payment': '💸 Advance Payment',
            'lottery': '🎲 Lottery',
            'prize': '🏆 Prize',
            'selected': '✅ You Are Selected',
            'congratulations': '🎉 Congratulations',
            'western union': '💱 Western Union',
            'money gram': '💵 Money Gram',
            'bitcoin': '₿ Bitcoin',
            'cryptocurrency': '🔷 Cryptocurrency',
            'no experience': '🌟 No Experience Needed',
            'fresher': '🎓 Fresher Friendly',
            'high salary': '💰 High Salary',
            'lakhs per month': '📈 Lakhs/Month',
            'crore': '💎 Crore Package',
            'foreign': '🌏 Foreign Job',
            'visa sponsorship': '🛂 Visa Sponsorship',
            'free visa': '🎫 Free Visa',
            'air ticketing': '✈️ Air Ticketing',
            'travel free': '🧳 Free Travel',
            'accommodation': '🏨 Free Accommodation',
            'food allowance': '🍛 Food Allowance',
            'medical insurance': '⚕️ Medical Insurance',
            'join today': '🔜 Join Today',
            'limited seats': '🎯 Limited Seats',
            'hurry up': '⏳ Hurry Up',
            'last chance': '⌛ Last Chance',
            'whatsapp': '📱 WhatsApp Contact',
            'telegram': '📲 Telegram Group',
            'personal email': '📧 Personal Email',
            'youtube': '▶️ YouTube Channel',
            'instagram': '📸 Instagram',
            'facebook': '👤 Facebook'
        }
        
        trigger_hits = []
        text_lower = translated.lower()
        for pattern, display in trigger_keywords.items():
            if pattern in text_lower:
                trigger_hits.append(display)
        
        trigger_hits = list(set(trigger_hits))[:8]
        
        X = vectorizer.transform([translated])
        proba = model.predict_proba(X)[0]
        score = proba[1] * 100
        result = "FAKE" if score >= 50 else "REAL"
        
        suggestions = [
            "📋 Verify company on LinkedIn and Glassdoor",
            "🔍 Check official website domain carefully",
            "📞 Call company directly using official number",
            "🚫 Never pay for job applications or training",
            "👥 Ask current/former employees on LinkedIn",
            "⚖️ Research legal complaints against company"
        ]
        
        if trigger_hits:
            suggestions.append(f"⚠️ Be careful: {', '.join(trigger_hits[:3])}")
        
        return {
            'result': result,
            'score': score,
            'suggestions': suggestions,
            'trigger_hits': trigger_hits,
            'detected_lang': detected_lang,
            'translated_text': translated
        }
    except Exception as e:
        print(f"Analysis error: {e}")
        return None

# ==================== TRUSTED SITES ====================
def get_trusted_sites():
    return [
        {'name': 'LinkedIn',  'url': 'https://www.linkedin.com/jobs', 'logo': 'https://www.google.com/s2/favicons?domain=linkedin.com&sz=64'},
        {'name': 'Naukri',    'url': 'https://www.naukri.com',        'logo': 'https://www.google.com/s2/favicons?domain=naukri.com&sz=64'},
        {'name': 'Indeed',    'url': 'https://www.indeed.com',        'logo': 'https://www.google.com/s2/favicons?domain=indeed.com&sz=64'},
        {'name': 'Glassdoor', 'url': 'https://www.glassdoor.com',     'logo': 'https://www.google.com/s2/favicons?domain=glassdoor.com&sz=64'},
        {'name': 'Monster',   'url': 'https://www.monster.com',       'logo': 'https://www.google.com/s2/favicons?domain=monster.com&sz=64'},
        {'name': 'Shine',     'url': 'https://www.shine.com',         'logo': 'https://www.google.com/s2/favicons?domain=shine.com&sz=64'},
    ]

# ==================== NEW: OCR FUNCTION ====================
import requests

def extract_text_from_image(uploaded_file):
    """Extract text from image using OCR.space API"""
    try:
        # OCR.space API endpoint
        url = "https://api.ocr.space/parse/image"
        
        # API key - CHANGE THIS!
        api_key = "YOUR_API_KEY_HERE"
        
        # File ah read pannu
        image_bytes = uploaded_file.read()
        
        # Multipart form data
        files = {
            'file': (uploaded_file.name, image_bytes, uploaded_file.type)
        }
        data = {
            'apikey': api_key,
            'language': 'eng',
            'isOverlayRequired': False,
            'detectOrientation': True,
            'scale': True
        }
        
        # API call
        response = requests.post(url, files=files, data=data)
        result = response.json()
        
        # Check success
        if not result.get('IsErroredOnProcessing'):
            parsed_results = result.get('ParsedResults', [])
            if parsed_results:
                text = parsed_results[0].get('ParsedText', '')
                return text, None
            else:
                return None, "No text found in image"
        else:
            error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
            return None, error_msg
            
    except Exception as e:
        return None, str(e)

# ==================== PAGE FUNCTIONS ====================
def show_history_page():
    st.markdown("## 📜 Scan History")
    if not st.session_state.history:
        st.info("No scans yet. Go to Scanner and analyze some jobs!")
        return
    
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

def show_analytics_page():
    st.markdown("## 📊 Analytics")
    history = st.session_state.history
    if not history:
        st.info("No data yet.")
        return
    
    total = len(history)
    fake = sum(1 for h in history if h['result'] == 'FAKE')
    real = total - fake
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", total)
    col2.metric("Fake Jobs", fake, delta=fake, delta_color="inverse")
    col3.metric("Safe Jobs", real)
    
    # Simple pie chart
    if MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots()
        ax.pie([fake, real], labels=['Fake', 'Safe'], autopct='%1.1f%%', colors=['#ff6b6b','#51cf66'])
        st.pyplot(fig)
    else:
        st.write("Install matplotlib to see charts.")

# ==================== AUTH PAGE ====================
def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="hero-premium">
            <h1 class="hero-title-premium">🛡️ JobShield AI</h1>
            <p class="hero-sub-premium">Premium Fake Job Detection System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs inside the same box
        tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
        
        with tab1:
            st.markdown("### 👋 Welcome Back!")
            email = st.text_input("📧 Email", placeholder="Enter your email", key="login_email")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🚀 LOGIN NOW", use_container_width=True):
                if email and password:
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result
                        
                        with st.spinner("📧 Sending security alert..."):
                            send_admin_alert(email, result, "login")
                        
                        st.success(f"✅ Welcome back, {result}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("⚠️ Fill all fields!")
        
        with tab2:
            st.markdown("### ✨ Create New Account")
            name = st.text_input("👤 Full Name", placeholder="Enter your name", key="reg_name")
            email = st.text_input("📧 Email", placeholder="Enter your email", key="reg_email")
            password = st.text_input("🔑 Password", type="password", placeholder="Create password", key="reg_pass")
            confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm password", key="reg_confirm")
            
            if st.button("📝 REGISTER NOW", use_container_width=True):
                if name and email and password and confirm:
                    if password != confirm:
                        st.error("❌ Passwords don't match!")
                    else:
                        success, msg = register_user(name, email, password)
                        if success:
                            st.success(f"✅ {msg} Please login!")
                        else:
                            st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ Fill all fields!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats below the box
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">20+</h3>
                <p style="color:rgba(255,255,255,0.9);">Languages</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">AI</h3>
                <p style="color:rgba(255,255,255,0.9);">Powered</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">100%</h3>
                <p style="color:rgba(255,255,255,0.9);">Free</p>
            </div>
            """, unsafe_allow_html=True)

# ==================== MAIN PAGE ====================
def show_main_page():
    # Admin Alert Badge
    st.markdown("""
    <div class="admin-badge">
        👮 Admin Monitoring Active
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h1 style="font-size:2rem; margin:0;">🛡️</h1>
            <h3 style="color:#8b5cf6; margin:0;">JobShield AI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="sidebar-user-premium">
            <p style="color:white; margin:0;">👤 {st.session_state.user_name}</p>
            <p style="color:rgba(255,255,255,0.9); font-size:0.8rem; margin:5px 0 0;">{st.session_state.user_email}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio("Navigation", ["🔍 Scanner", "📜 History", "📊 Analytics"])
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:rgba(139,92,246,0.15); border-radius:15px; padding:1rem; text-align:center;">
                <p style="color:#8b5cf6; font-size:1.5rem; margin:0;">20+</p>
                <p style="color:#4a4a6a; margin:0;">Languages</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:rgba(139,92,246,0.15); border-radius:15px; padding:1rem; text-align:center;">
                <p style="color:#8b5cf6; font-size:1.5rem; margin:0;">ML</p>
                <p style="color:#4a4a6a; margin:0;">Powered</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Page routing
    if page == "🔍 Scanner":
        # ===== Main Scanner UI =====
        st.markdown("""
        <div class="hero-premium">
            <h1 class="hero-title-premium">🔍 Job Fraud Detector</h1>
            <p class="hero-sub-premium">Paste any job posting or upload screenshot - we'll analyze it in 20+ languages</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card-premium">', unsafe_allow_html=True)
        
        # Input method
        input_method = st.radio(
            "Choose input method:",
            ["📝 Paste Text", "🔗 Job URL", "📸 Image Upload"],
            horizontal=True
        )
        
        job_text = ""
        
        if input_method == "📝 Paste Text":
            st.markdown("#### 📝 Paste Job Description")
            job_text = st.text_area(
                "Paste the job posting here:",
                height=200,
                placeholder="Copy and paste the suspicious job description here..."
            )
        elif input_method == "🔗 Job URL":
            st.markdown("#### 🔗 Enter Job URL")
            url = st.text_input("Paste the job URL:", placeholder="https://...")
            if url:
                domain = url.split('/')[2] if '//' in url else url
                trusted = [
                    'naukri.com', 'shine.com', 'monsterindia.com', 'timesjobs.com', 'freshersworld.com',
                    'careers360.com', 'indeed.co.in', 'linkedin.com', 'glassdoor.co.in', 'foundit.in',
                    'apna.co', 'quikrjobs.com', 'click.in', 'hireclap.com', 'workindia.in',
                    'internshala.com', 'hellotasks.com', 'urbanpro.com', 'babajob.com', 'hirect.in',
                    'indeed.com', 'monster.com', 'careerbuilder.com', 'ziprecruiter.com', 'simplyhired.com',
                    'dice.com', 'upwork.com', 'freelancer.com', 'fiverr.com', 'toptal.com',
                    'angel.co', 'wellfound.com', 'hired.com', 'landing.jobs', 'remoteok.com',
                    'weworkremotely.com', 'flexjobs.com', 'virtualvocations.com', 'jobspresso.co',
                    'tcs.com', 'infosys.com', 'wipro.com', 'hcl.com', 'techmahindra.com',
                    'lti.com', 'mindtree.com', 'cognizant.com', 'capgemini.com', 'accenture.com',
                    'ibm.com', 'microsoft.com', 'google.co.in', 'amazon.in', 'flipkart.com',
                    'paytm.com', 'phonepe.com', 'razorpay.com', 'zomato.com', 'swiggy.com',
                    'ola.com', 'uber.com', 'oyo.com', 'makemytrip.com', 'goibibo.com',
                    'byjus.com', 'unacademy.com', 'vedantu.com', 'upgrad.com', 'coursera.com',
                    'apple.com', 'meta.com', 'facebook.com', 'twitter.com', 'netflix.com',
                    'adobe.com', 'salesforce.com', 'oracle.com', 'sap.com', 'vmware.com',
                    'cisco.com', 'intel.com', 'nvidia.com', 'amd.com', 'qualcomm.com',
                    'dell.com', 'hp.com', 'lenovo.com', 'sony.com', 'samsung.com',
                    'lg.com', 'panasonic.com', 'toshiba.com', 'hitachi.com', 'philips.com',
                    'siemens.com', 'ge.com', '3m.com', 'bosch.com', 'honeywell.com',
                    'walmart.com', 'target.com', 'bestbuy.com', 'homedepot.com', 'lowes.com',
                    'ebay.com', 'etsy.com', 'shopify.com', 'alibaba.com', 'aliexpress.com',
                    'icicibank.com', 'hdfcbank.com', 'sbicard.com', 'axisbank.com', 'kotak.com',
                    'goldmansachs.com', 'jpmorgan.com', 'morganstanley.com', 'credit-suisse.com',
                    'paypal.com', 'stripe.com', 'square.com', 'robinhood.com',
                    'airtel.com', 'jio.com', 'vodafone.com', 'idea.com', 'bsnl.co.in',
                    'disney.com', 'netflix.com', 'spotify.com', 'youtube.com', 'hotstar.com',
                    'gov.in', 'nic.in', 'upsc.gov.in', 'ssc.nic.in', 'ugc.ac.in',
                    'iit.ac.in', 'nit.edu', 'annauniv.edu', 'vtu.ac.in', 'jntuh.ac.in',
                    'apollohospitals.com', 'fortishealthcare.com', 'maxhealthcare.com', 'medanta.org',
                    'pfizer.com', 'novartis.com', 'roche.com', 'merck.com', 'johnsonandjohnson.com',
                    'toyota.com', 'honda.com', 'hyundai.com', 'marutisuzuki.com', 'tata.com',
                    'mahindra.com', 'bmw.com', 'mercedes-benz.com', 'audi.com', 'ford.com',
                    'airindia.com', 'indigo.in', 'spicejet.com', 'goair.in', 'emirates.com',
                    'qatarairways.com', 'singaporeair.com', 'britishairways.com', 'lufthansa.com',
                    'zoom.us', 'slack.com', 'dropbox.com', 'box.com', 'github.com',
                    'gitlab.com', 'bitbucket.org', 'atlassian.com', 'jira.com', 'trello.com'
                ]
                if any(t in domain for t in trusted):
                    st.success(f"✅ {domain} is a trusted portal!")
                    job_text = f"Job from trusted portal {domain}"
                else:
                    st.warning(f"⚠️ {domain} is not a known trusted portal!")
                    job_text = f"suspicious unknown domain {domain} unverified link job posting fee deposit urgent"
        else:  # Image Upload
            st.markdown("#### 📸 Upload Job Screenshot")
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=['png', 'jpg', 'jpeg', 'bmp'],
                help="Upload screenshot of job posting"
            )
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Screenshot", width=300)
                
                with st.spinner("🔍 Extracting text from image..."):
                    extracted_text, error = extract_text_from_image(uploaded_file)
                    if extracted_text:
                        st.success("✅ Text extracted successfully!")
                        job_text = extracted_text
                    else:
                        st.error(f"❌ {error}")
                        job_text = ""
        
        st.markdown('</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_clicked = st.button("🔍 ANALYZE JOB - DETECT FRAUD", use_container_width=True)
        
        if analyze_clicked:
            if not job_text.strip():
                st.warning("⚠️ Please enter job content first!")
            elif model is None:
                st.error("❌ AI Model not loaded - check dataset path!")
            else:
                with st.spinner("🔍 Analyzing with AI Engine..."):
                    analysis = analyze_job(job_text)
                
                # SAFETY CHECK
                if analysis and isinstance(analysis, dict):
                    st.markdown("---")
                    
                    if analysis.get('result') == "FAKE":
                        st.markdown(f"""
                        <div class="fake-banner-premium">
                            <h2>🚩 WARNING: FAKE JOB DETECTED!</h2>
                            <p style="font-size:1.5rem;"><strong>Fraud Probability: {analysis.get('score', 0):.1f}%</strong></p>
                            <p style="font-size:1.1rem;">⛔ Do NOT apply or pay any money for this job!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="genuine-banner-premium">
                            <h2>✅ LIKELY GENUINE JOB</h2>
                            <p style="font-size:1.5rem;"><strong>Safety Score: {100 - analysis.get('score', 0):.1f}%</strong></p>
                            <p style="font-size:1.1rem;">Still verify company details before applying.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Share buttons
                    st.markdown("### 📤 Share Result")
                    if analysis.get('result') == "FAKE":
                        share_text = f"🚨 FAKE JOB ALERT! Fraud Probability: {analysis.get('score', 0):.1f}%"
                    else:
                        share_text = f"✅ Job seems genuine! Safety Score: {100 - analysis.get('score', 0):.1f}%"
                    
                    whatsapp_link = f"https://wa.me/?text={urllib.parse.quote(share_text)}"
                    mailto_link = f"mailto:?subject=JobShield AI Result&body={urllib.parse.quote(share_text)}"
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<a href="{whatsapp_link}" target="_blank" class="share-button">📱 WhatsApp</a>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<a href="#" onclick="navigator.clipboard.writeText(`{share_text}`);alert(\'Copied!\');" class="share-button">📋 Copy</a>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<a href="{mailto_link}" class="share-button">📧 Email</a>', unsafe_allow_html=True)
                    
                    # Auto Email
                    with st.spinner("📧 Sending analysis report to your email..."):
                        auto_sent = send_email_alert(
                            to_email=st.session_state.user_email,
                            user_name=st.session_state.user_name,
                            job_text=job_text,
                            result=analysis.get('result'),
                            score=analysis.get('score', 0),
                            suggestions=analysis.get('suggestions', []),
                            trigger_hits=analysis.get('trigger_hits', []),
                            detected_lang=analysis.get('detected_lang', 'en'),
                            translated_text=analysis.get('translated_text', ''),
                        )
                    
                    if auto_sent:
                        st.markdown(f"""
                        <div class="email-alert-premium">
                            📧 Analysis report sent to <strong>{st.session_state.user_email}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Auto email failed - check SMTP settings.")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🌍 Language Analysis")
                        lang_map = {
                            'ta':'Tamil','hi':'Hindi','en':'English','ar':'Arabic','zh-cn':'Chinese',
                            'es':'Spanish','fr':'French','de':'German','ja':'Japanese','ko':'Korean',
                            'ru':'Russian','pt':'Portuguese','id':'Indonesian','tr':'Turkish',
                            'bn':'Bengali','vi':'Vietnamese','th':'Thai','ur':'Urdu',
                        }
                        lang_display = lang_map.get(analysis.get('detected_lang'), analysis.get('detected_lang', 'unknown').upper())
                        st.info(f"**Detected Language:** {lang_display}")
                        
                        if analysis.get('detected_lang') != 'en':
                            st.markdown("#### 📝 English Translation")
                            st.info(analysis.get('translated_text', '')[:400])
                        
                        if analysis.get('trigger_hits'):
                            st.markdown("#### ⚠️ Risk Indicators")
                            for hit in analysis.get('trigger_hits', []):
                                st.markdown(f'<span class="risk-badge-premium">{hit}</span>', unsafe_allow_html=True)
                        else:
                            st.success("✅ No major risk keywords found")
                    
                    with col2:
                        st.markdown("#### 💡 Recommendations")
                        for s in analysis.get('suggestions', []):
                            st.markdown(f"- {s}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    heading = "### 🚨 Apply on These TRUSTED Platforms Instead!" if analysis.get('result') == "FAKE" else "### 🏆 Top Trusted Job Platforms"
                    st.markdown(heading)
                    cols = st.columns(6)
                    for i, site in enumerate(get_trusted_sites()):
                        with cols[i]:
                            st.markdown(f"""<div class="site-card">
                                <img src="{site['logo']}" width="40" height="40" 
                                     style="border-radius:8px;margin-bottom:8px;">
                                <br>
                                <a href="{site['url']}" target="_blank">{site['name']}</a>
                            </div>""", unsafe_allow_html=True)
                
                else:
                    st.error("❌ Analysis failed. Invalid result.")
        
        # ===== End Scanner UI =====
    elif page == "📜 History":
        show_history_page()
    elif page == "📊 Analytics":
        show_analytics_page()

# ==================== ROUTER ====================
if st.session_state.logged_in:
    show_main_page()
else:
    show_auth_page()

# Premium Footer
st.markdown("""
<div class="footer-premium">
    🛡️ JobShield AI v3.0 | ML + AI + 20+ Languages | Premium Security System
</div>
""", unsafe_allow_html=True)
