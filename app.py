import streamlit as s
import pandas as pd
import os
import json
import re
import smtplib
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from deep_translator import GoogleTranslator, MyMemoryTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from langdetect import detect
from datetime import datetime
import time

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
SENDER_EMAIL = "project192003@gmail.com"
SENDER_PASSWORD = "zppgvmmtergdvzgs"
ADMIN_EMAIL = "project192003@gmail.com"
USERS_FILE = "users.json"

# SMART PATH - WORKS ON LAPTOP & PHONE
import os

# Method 1: First try same folder (for phone & cloud)
if os.path.exists("fake_job.csv"):
    DATASET_PATH = "fake_job.csv"
    print("✅ Using local file: fake_job.csv")
    
# Method 2: If not found, try laptop specific path
elif os.path.exists(r"C:\Users\Lenovo\Desktop\AI fake job\fake_job.csv"):
    DATASET_PATH = r"C:\Users\Lenovo\Desktop\AI fake job\fake_job.csv"
    print("✅ Using laptop path: C:\\Users\\Lenovo\\Desktop\\AI fake job\\fake_job.csv")
    
# Method 3: If both not found, show error
else:
    DATASET_PATH = "fake_job.csv"  # default
    print("❌ Dataset not found! Please check location")


st.set_page_config(page_title="JobShield AI - Premium Security", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────
# PREMIUM CSS WITH ANIMATIONS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    
    * { font-family: 'Inter', sans-serif !important; }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(145deg,#f8faff,#f0f3fd);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Premium Text Colors */
    p, span, label, div, h1, h2, h3, h4, h5, li {
        color: #1e293b !important;
    }
    .hero-sub {
    color: #475569 !important;
    }
    
    /* Animated Hero Section */
    .hero-premium {
        text-align: center;
        padding: 2rem 0;
        animation: fadeInDown 1s ease;
    }
    
    .hero-title-premium {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
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
        color: #94a3b8 !important;
        font-size: 1.2rem;
        animation: fadeInUp 1s ease 0.3s both;
    }
    
    /* Premium Glass Card */
    .glass-card-premium {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease;
    }
    
    .glass-card-premium:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(123, 47, 247, 0.3);
        border-color: rgba(123, 47, 247, 0.3);
    }
    
    /* Animated Result Banners */
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
    
    /* Premium Stats Card */
    .stats-card-premium {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        animation: float 3s ease infinite;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Premium Badges */
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
    
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(90deg, #7b2ff7, #00d2ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.4) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(123, 47, 247, 0.6) !important;
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
    
    /* Premium Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(123, 47, 247, 0.3) !important;
        border-radius: 15px !important;
        color: #1a1a2e !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7b2ff7 !important;
        box-shadow: 0 0 0 3px rgba(123, 47, 247, 0.2) !important;
        transform: scale(1.02);
    }
    
    /* Premium Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 8, 30, 0.98) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    .sidebar-user-premium {
        background: linear-gradient(135deg, #7b2ff7, #00d2ff);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        animation: slideInRight 0.5s ease;
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
    
    /* Premium Email Alert Box */
    .email-alert-premium {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1));
        border-left: 5px solid #ffd700;
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
    
    /* Premium Trusted Site Cards */
    .site-card-premium {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInScale 0.5s ease;
    }
    
    .site-card-premium:hover {
        transform: scale(1.05) rotateY(5deg);
        border-color: #7b2ff7;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.3);
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
        color: #00d2ff !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        display: block;
        margin-top: 0.5rem;
    }
    
    /* Premium Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7b2ff7, #00d2ff) !important;
        border-radius: 10px !important;
        transition: width 1s ease !important;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50px;
        padding: 0.3rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #7b2ff7, #00d2ff) !important;
        color: white !important;
        transform: scale(1.05);
    }
    
    /* Premium Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #7b2ff7, #00d2ff, transparent);
        margin: 2rem 0;
    }
    
    /* Premium Footer */
    .footer-premium {
        text-align: center;
        color: #475569 !important;
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
        background: linear-gradient(90deg, transparent, #7b2ff7, #00d2ff, transparent);
        animation: slide 3s infinite;
    }
    
    @keyframes slide {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Loading Animation */
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
    
    /* Admin Alert Badge */
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ADMIN ALERT FUNCTION
# ─────────────────────────────────────────────
def send_admin_alert(user_email, user_name, action="login"):
    """Send alert to admin when user logs in"""
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
                <div style="background:linear-gradient(135deg,#7b2ff7,#00d2ff);border-radius:20px;padding:2rem;text-align:center;margin-bottom:20px;">
                    <h1 style="color:white;margin:0;">🛡️ JobShield AI</h1>
                    <p style="color:rgba(255,255,255,0.9);margin:5px 0 0;">User Activity Alert</p>
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;">
                    <h2 style="color:#00d2ff;margin:0 0 20px;">🔔 New User {action.capitalize()}</h2>
                    
                    <div style="background:rgba(123,47,247,0.1);border-radius:15px;padding:1.5rem;margin:10px 0;">
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

# ─────────────────────────────────────────────
# USER MANAGEMENT
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# ENHANCED EMAIL FUNCTION
# ─────────────────────────────────────────────
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
            <div style="background:rgba(0,210,255,0.1);border-radius:15px;padding:1rem;margin:15px 0;border-left:4px solid #00d2ff;">
                <p style="color:#00d2ff;font-weight:600;margin:0 0 5px;">📝 English Translation</p>
                <p style="color:#94a3b8;margin:0;">{translated_text[:400]}{'...' if len(translated_text)>400 else ''}</p>
            </div>"""
        
        job_preview = job_text[:300] + ("..." if len(job_text) > 300 else "")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#1a1a2e;font-family:'Inter',sans-serif;">
            <div style="max-width:600px;margin:30px auto;padding:20px;">
                <div style="text-align:center;margin-bottom:30px;">
                    <h1 style="background:linear-gradient(90deg,#00d2ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5rem;margin:0;">🛡️ JobShield AI</h1>
                    <p style="color:#94a3b8;">Fake Job Detection Report</p>
                </div>
                
                <p style="color:#e2e8f0;">Hello <strong style="color:#00d2ff;">{user_name}</strong>,</p>
                
                <div style="background:{banner_grad};border-radius:24px;padding:2rem;text-align:center;margin:20px 0;box-shadow:0 0 30px {'#ff416c' if is_fake else '#11998e'}80;">
                    <h2 style="color:white;margin:0;">{status_label}</h2>
                    <p style="color:white;font-size:1.2rem;margin:10px 0;"><strong>{score_label}</strong></p>
                    <p style="color:rgba(255,255,255,0.9);">{warning_line}</p>
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:1.5rem;margin:15px 0;">
                    <p style="color:#00d2ff;font-weight:700;">🌍 Language Analysis</p>
                    <p style="color:#e2e8f0;">Detected Language: <strong style="color:#7dd3fc;">{lang_display}</strong></p>
                    {translation_block}
                </div>
                
                <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:1.5rem;margin:15px 0;">
                    <p style="color:#f87171;font-weight:700;">⚠️ Risk Indicators</p>
                    <div>{badge_html}</div>
                </div>
                
                <div style="background:rgba(123,47,247,0.15);border:1px solid rgba(123,47,247,0.4);border-radius:20px;padding:1.5rem;margin:15px 0;">
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

# ─────────────────────────────────────────────
# MODEL TRAINING
# ─────────────────────────────────────────────
@st.cache_resource
def train_model():
    try:
        # Try Excel first
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
        
        # Combine text columns
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

# ─────────────────────────────────────────────
# TRANSLATION FUNCTION
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# JOB ANALYSIS FUNCTION
# ─────────────────────────────────────────────
def analyze_job(job_text):
    if not job_text or model is None:
        return None
        
    try:
        translated, detected_lang = translate_to_english(job_text)
        
        # Risk keywords
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
        
        # ML prediction
        X = vectorizer.transform([translated])
        proba = model.predict_proba(X)[0]
        score = proba[1] * 100
        result = "FAKE" if score >= 50 else "REAL"
        
        # Suggestions
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
    except Exception:
        return None

# ─────────────────────────────────────────────
# TRUSTED SITES
# ─────────────────────────────────────────────
def get_trusted_sites():
    return [
        {'name': 'LinkedIn', 'url': 'https://www.linkedin.com/jobs', 'icon': '🔵'},
        {'name': 'Naukri', 'url': 'https://www.naukri.com', 'icon': '🟠'},
        {'name': 'Indeed', 'url': 'https://www.indeed.com', 'icon': '🔷'},
        {'name': 'Glassdoor', 'url': 'https://www.glassdoor.com', 'icon': '🟢'},
        {'name': 'Monster', 'url': 'https://www.monster.com', 'icon': '🟣'},
        {'name': 'Shine', 'url': 'https://www.shine.com', 'icon': '⭐'},
    ]

# ─────────────────────────────────────────────
# AUTH PAGE - PREMIUM DESIGN
# ─────────────────────────────────────────────
def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Premium Hero
        st.markdown("""
        <div class="hero-premium">
            <h1 class="hero-title-premium">🛡️ JobShield AI</h1>
            <p class="hero-sub-premium">Premium Fake Job Detection System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium Auth Card
        st.markdown('<div class="glass-card-premium">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### 👋 Welcome Back!")
            email = st.text_input("📧 Email", placeholder="Enter your email", key="login_email")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🚀 Login Now", use_container_width=True):
                if email and password:
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result
                        
                        # Send admin alert on login
                        with st.spinner("📧 Sending security alert..."):
                            send_admin_alert(email, result, "login")
                        
                        st.success(f"✅ Welcome back, {result}!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("⚠️ Fill all fields!")
        
        with tab2:
            st.markdown("### ✨ Create Account")
            name = st.text_input("👤 Full Name", placeholder="Enter your name", key="reg_name")
            email = st.text_input("📧 Email", placeholder="Enter your email", key="reg_email")
            password = st.text_input("🔑 Password", type="password", placeholder="Create password", key="reg_pass")
            confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm password", key="reg_confirm")
            
            if st.button("📝 Register Now", use_container_width=True):
                if name and email and password and confirm:
                    if password != confirm:
                        st.error("❌ Passwords don't match!")
                    else:
                        success, msg = register_user(name, email, password)
                        if success:
                            st.success(f"✅ {msg} Please login!")
                            st.snow()
                        else:
                            st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ Fill all fields!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">20+</h3>
                <p style="color:rgba(255,255,255,0.8);">Languages</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">AI</h3>
                <p style="color:rgba(255,255,255,0.8);">Powered</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
            <div class="stats-card-premium">
                <h3 style="color:white;">100%</h3>
                <p style="color:rgba(255,255,255,0.8);">Free</p>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN PAGE - PREMIUM DESIGN
# ─────────────────────────────────────────────
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
            <h3 style="color:#00d2ff; margin:0;">JobShield AI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="sidebar-user-premium">
            <p style="color:white; margin:0;">👤 {st.session_state.user_name}</p>
            <p style="color:rgba(255,255,255,0.8); font-size:0.8rem; margin:5px 0 0;">{st.session_state.user_email}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:rgba(123,47,247,0.1); border-radius:15px; padding:1rem; text-align:center;">
                <p style="color:#00d2ff; font-size:1.5rem; margin:0;">20+</p>
                <p style="color:#94a3b8; margin:0;">Languages</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:rgba(123,47,247,0.1); border-radius:15px; padding:1rem; text-align:center;">
                <p style="color:#00d2ff; font-size:1.5rem; margin:0;">ML</p>
                <p style="color:#94a3b8; margin:0;">Powered</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Main Content
    st.markdown("""
    <div class="hero-premium">
        <h1 class="hero-title-premium">🔍 Job Fraud Detector</h1>
        <p class="hero-sub-premium">Paste any job posting - we'll analyze it in 20+ languages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="glass-card-premium">', unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choose input method:",
        ["📝 Paste Text", "🔗 Job URL", "📧 Email Content"],
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
            trusted = ['linkedin.com', 'naukri.com', 'indeed.com', 'glassdoor.com', 
                      'monster.com', 'shine.com', 'freshersworld.com', 'timesjobs.com']
            if any(t in domain for t in trusted):
                st.success(f"✅ {domain} is a trusted portal!")
                job_text = f"Job from trusted portal {domain}"
            else:
                st.warning(f"⚠️ {domain} is not a known trusted portal!")
                job_text = f"suspicious unknown domain {domain} unverified link job posting fee deposit urgent"
    else:
        st.markdown("#### 📧 Paste Job Email")
        job_text = st.text_area(
            "Paste the job-related email:",
            height=200,
            placeholder="Copy and paste the suspicious job email here..."
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("🔍 ANALYZE JOB - DETECT FRAUD", use_container_width=True)
    
    # Results Section
    if analyze_clicked:
        if not job_text.strip():
            st.warning("⚠️ Please enter job content first!")
        elif model is None:
            st.error("❌ AI Model not loaded - check dataset path!")
        else:
            with st.spinner("🔍 Analyzing with AI Engine..."):
                analysis = analyze_job(job_text)
            
            if not analysis:
                st.error("❌ Analysis failed. Please try again.")
            else:
                st.markdown("---")
                
                # Result Banner
                if analysis['result'] == "FAKE":
                    st.markdown(f"""
                    <div class="fake-banner-premium">
                        <h2>🚩 WARNING: FAKE JOB DETECTED!</h2>
                        <p style="font-size:1.5rem;"><strong>Fraud Probability: {analysis['score']:.1f}%</strong></p>
                        <p style="font-size:1.1rem;">⛔ Do NOT apply or pay any money for this job!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="genuine-banner-premium">
                        <h2>✅ LIKELY GENUINE JOB</h2>
                        <p style="font-size:1.5rem;"><strong>Safety Score: {100 - analysis['score']:.1f}%</strong></p>
                        <p style="font-size:1.1rem;">Still verify company details before applying.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Auto Email
                with st.spinner("📧 Sending analysis report to your email..."):
                    auto_sent = send_email_alert(
                        to_email=st.session_state.user_email,
                        user_name=st.session_state.user_name,
                        job_text=job_text,
                        result=analysis['result'],
                        score=analysis['score'],
                        suggestions=analysis['suggestions'],
                        trigger_hits=analysis['trigger_hits'],
                        detected_lang=analysis['detected_lang'],
                        translated_text=analysis['translated_text'],
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
                
                # Two Column Analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="glass-card-premium">', unsafe_allow_html=True)
                    st.markdown("#### 🌍 Language Analysis")
                    
                    lang_map = {
                        'ta':'Tamil','hi':'Hindi','en':'English','ar':'Arabic','zh-cn':'Chinese',
                        'es':'Spanish','fr':'French','de':'German','ja':'Japanese','ko':'Korean',
                        'ru':'Russian','pt':'Portuguese','id':'Indonesian','tr':'Turkish',
                        'bn':'Bengali','vi':'Vietnamese','th':'Thai','ur':'Urdu',
                    }
                    lang_display = lang_map.get(analysis['detected_lang'], analysis['detected_lang'].upper())
                    
                    st.info(f"**Detected Language:** {lang_display}")
                    
                    if analysis['detected_lang'] != 'en':
                        st.markdown("#### 📝 English Translation")
                        st.info(analysis['translated_text'][:400])
                    
                    if analysis['trigger_hits']:
                        st.markdown("#### ⚠️ Risk Indicators")
                        for hit in analysis['trigger_hits']:
                            st.markdown(f'<span class="risk-badge-premium">{hit}</span>', unsafe_allow_html=True)
                    else:
                        st.success("✅ No major risk keywords found")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="glass-card-premium">', unsafe_allow_html=True)
                    st.markdown("#### 💡 Recommendations")
                    
                    for s in analysis['suggestions']:
                        st.markdown(f"- {s}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Trusted Sites
                st.markdown("<br>", unsafe_allow_html=True)
                heading = "### 🚨 Apply on These TRUSTED Platforms Instead!" if analysis['result'] == "FAKE" else "### 🏆 Top Trusted Job Platforms"
                st.markdown(heading)
                
                cols = st.columns(6)
                for i, site in enumerate(get_trusted_sites()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="site-card-premium">
                            <div style="font-size:2rem;">{site['icon']}</div>
                            <a href="{site['url']}" target="_blank">{site['name']}</a>
                        </div>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    show_main_page()
else:
    show_auth_page()

# Premium Footer
st.markdown("""
<div class="footer-premium">
    🛡️ JobShield AI v2.0 | ML + AI + 20+ Languages | Premium Security System
</div>
""", unsafe_allow_html=True)



