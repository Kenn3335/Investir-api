from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from starlette.middleware.sessions import SessionMiddleware

# =====================
# KONFIGIRASYON APP
# =====================

app = FastAPI(
    title="VestiCore",
    description="Platfòm VestiCore",
    version="2.0"
)

# =====================
# SESSION MIDDLEWARE
# =====================

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "vesticore-secret-key-change-later")
)

# =====================
# DATABASE
# =====================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vesticore.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =====================
# VARIYAB ANVIWÒNMAN
# =====================

USDT_TRON_ADDRESS = "TUNtoPGB3sBwbbX81t6ca4fK2exJNFLRiu"
USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
DEPOSIT_FEE = int(os.getenv("DEPOSIT_FEE", "3"))
WITHDRAW_FEE = int(os.getenv("WITHDRAW_FEE", "5"))

# =====================
# STIL CSS (POU TOUT PAGES)
# =====================

STYLE = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a4e 50%, #0d1b3e 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 24px;
        padding: 50px 40px;
        max-width: 480px;
        width: 100%;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(255, 215, 0, 0.05);
    }
    .logo {
        text-align: center;
        margin-bottom: 30px;
    }
    .logo-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: 900;
        color: #0a0e27;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 15px;
    }
    .logo h1 {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .logo h1 span {
        color: #ffd700;
    }
    .logo p {
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        margin-top: 5px;
        letter-spacing: 4px;
    }
    .title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 8px;
        text-align: center;
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        text-align: center;
        margin-bottom: 25px;
    }
    .form-group {
        margin-bottom: 18px;
    }
    .form-group label {
        display: block;
        color: rgba(255, 255, 255, 0.7);
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }
    .form-group input {
        width: 100%;
        padding: 14px 18px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #ffffff;
        font-size: 15px;
        transition: all 0.3s ease;
        outline: none;
    }
    .form-group input:focus {
        border-color: #ffd700;
        background: rgba(255, 215, 0, 0.05);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.08);
    }
    .form-group input::placeholder {
        color: rgba(255, 255, 255, 0.25);
    }
    .btn {
        width: 100%;
        padding: 16px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border: none;
        border-radius: 12px;
        color: #0a0e27;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    .btn-secondary {
        background: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.05);
    }
    .link {
        text-align: center;
        margin-top: 20px;
        color: rgba(255, 255, 255, 0.4);
        font-size: 14px;
    }
    .link a {
        color: #ffd700;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s;
    }
    .link a:hover {
        color: #f0a500;
        text-decoration: underline;
    }
    .error {
        background: rgba(255, 0, 0, 0.15);
        border: 1px solid rgba(255, 0, 0, 0.2);
        color: #ff6b6b;
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 14px;
        margin-bottom: 18px;
        text-align: center;
    }
    @media (max-width: 480px) {
        .container { padding: 30px 20px; }
        .logo h1 { font-size: 26px; }
        .logo-icon { width: 60px; height: 60px; font-size: 30px; }
    }
</style>
"""

# =====================
# LOGO HTML (REKIPERAB)
# =====================

def get_logo():
    return """
    <div class="logo">
        <div class="logo-icon">V</div>
        <h1>Vesti<span>Core</span></h1>
        <p>INVEST • GROW • PROSPER</p>
    </div>
    """

# =====================
# DATABASE MODELS
# =====================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0)
    is_admin = Column(Integer, default=0)
    referral_code = Column(String, unique=True)
    referred_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float, default=0)
    duration = Column(Integer)
    description = Column(String)

class UserPlan(Base):
    __tablename__ = "user_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    plan_id = Column(Integer)
    amount = Column(Float)
    status = Column(String, default="active")
    start_date = Column(DateTime, default=datetime.now)

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    txid = Column(String)
    status = Column(String, default="pending")
    date = Column(DateTime, default=datetime.now)

class Withdraw(Base):
    __tablename__ = "withdraws"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    wallet = Column(String)
    status = Column(String, default="pending")
    date = Column(DateTime, default=datetime.now)

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    referrer = Column(String)
    invited_user = Column(String)
    status = Column(String, default="pending")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    action = Column(String)
    date = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

# =====================
# DATABASE SESSION
# =====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================
# PASSWORD SECURITY
# =====================

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# =====================
# REFERRAL CODE
# =====================

def create_referral_code(username):
    code = username.upper()[:5]
    return code + str(datetime.now().timestamp())[-5:]

# =====================
# ACTIVITY LOG
# =====================

def add_log(db, username, action):
    log = ActivityLog(username=username, action=action)
    db.add(log)
    db.commit()

# =====================
# CHECK LOGIN
# =====================

def current_user(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Ou dwe konekte")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kont pa jwenn")
    return user

# =====================
# ADMIN CHECK
# =====================

def admin_user(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if user.is_admin != 1:
        raise HTTPException(status_code=403, detail="Aksè admin sèlman")
    return user

# =====================
# TCHÈKE PLAN AKTIF
# =====================

def get_user_active_plan(db: Session, user_id: int):
    user_plan = db.query(UserPlan).filter(
        UserPlan.user_id == user_id,
        UserPlan.status == "active"
    ).first()
    if not user_plan:
        return None
    plan = db.query(Plan).filter(Plan.id == user_plan.plan_id).first()
    if not plan:
        return None
    expiration_date = user_plan.start_date + timedelta(days=plan.duration)
    if datetime.now() > expiration_date:
        user_plan.status = "expired"
        db.commit()
        return None
    return {"user_plan": user_plan, "plan": plan, "expiration_date": expiration_date}

# =====================
# HOME PAGE (AK LOGO)
# =====================

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
    <head>
        <title>VestiCore - Platfòm Envestisman</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo()}
            <div style="text-align:center;margin:10px 0 30px;">
                <p style="color:rgba(255,255,255,0.7);font-size:15px;line-height:1.6;">
                    Platfòm envestisman dijital ou<br>
                    <span style="color:#ffd700;">Fè kòb ou grandi</span>
                </p>
            </div>
            <a href="/register" class="btn" style="display:block;text-align:center;text-decoration:none;">
                Kreye kont
            </a>
            <br>
            <a href="/login" class="btn btn-secondary" style="display:block;text-align:center;text-decoration:none;">
                Konekte
            </a>
            <div class="link" style="margin-top:25px;">
                <span style="color:rgba(255,255,255,0.3);font-size:12px;">© 2026 VestiCore. Tout dwa rezève.</span>
            </div>
        </div>
    </body>
    </html>
    """

# =====================
# REGISTER PAGE
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return f"""
    <html>
    <head>
        <title>Kreye kont - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo()}
            <div class="title">Kreye kont ou</div>
            <div class="subtitle">Kòmanse vwayaj envestisman w</div>
            <form method="post">
                <div class="form-group">
                    <label>Non itilizatè</label>
                    <input type="text" name="username" placeholder="Antre non ou" required>
                </div>
                <div class="form-group">
                    <label>Modpas</label>
                    <input type="password" name="password" placeholder="Antre modpas ou" required>
                </div>
                <div class="form-group">
                    <label>Kòd referral (opsyonèl)</label>
                    <input type="text" name="ref" placeholder="Antre kòd referral si ou genyen">
                </div>
                <button type="submit" class="btn">Kreye kont</button>
            </form>
            <div class="link">
                Ou deja gen kont? <a href="/login">Konekte</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    ref: str = Form(None),
    db: Session = Depends(get_db)
):
    user_exist = db.query(User).filter(User.username == username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Kont sa deja egziste")
    
    new_user = User(
        username=username,
        password=hash_password(password),
        referral_code=create_referral_code(username),
        referred_by=ref
    )
    db.add(new_user)
    
    if ref:
        referral = Referral(referrer=ref, invited_user=username)
        db.add(referral)
    
    add_log(db, username, "Kreye nouvo kont")
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

# =====================
# LOGIN PAGE
# =====================

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return f"""
    <html>
    <head>
        <title>Konekte - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo()}
            <div class="title">Byenveni tounen</div>
            <div class="subtitle">Konekte pou jwenn espas ou</div>
            <form method="post">
                <div class="form-group">
                    <label>Non itilizatè</label>
                    <input type="text" name="username" placeholder="Antre non ou" required>
                </div>
                <div class="form-group">
                    <label>Modpas</label>
                    <input type="password" name="password" placeholder="Antre modpas ou" required>
                </div>
                <button type="submit" class="btn">Konekte</button>
            </form>
            <div class="link">
                Pa gen kont? <a href="/register">Kreye yon kont</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Itilizatè pa jwenn")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Modpas pa bon")
    
    request.session["username"] = username
    add_log(db, username, "Koneksyon fèt")
    return RedirectResponse(url="/dashboard", status_code=303)

# =====================
# DASHBOARD
# =====================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    plans = db.query(Plan).all()
    
    active_plan_info = get_user_active_plan(db, user.id)
    
    plan_html = ""
    for plan in plans:
        plan_html += f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:12px;padding:18px;margin:10px 0;border:1px solid rgba(255,215,0,0.1);">
            <h3 style="color:#ffd700;font-size:18px;">{plan.name}</h3>
            <p style="color:rgba(255,255,255,0.7);font-size:14px;">{plan.description}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:13px;">⏳ {plan.duration} jou</p>
            <p style="color:#ffffff;font-size:18px;font-weight:700;margin:8px 0;">{plan.price} USDT</p>
            <form method="post" action="/buy-plan">
                <input type="hidden" name="plan_id" value="{plan.id}">
                <button style="width:100%;padding:12px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:10px;color:#0a0e27;font-weight:700;cursor:pointer;font-size:14px;">Achte plan sa</button>
            </form>
        </div>
        """
    
    plan_info_html = ""
    if active_plan_info:
        plan = active_plan_info["plan"]
        exp_date = active_plan_info["expiration_date"]
        min_withdraw_map = {"Starter": 10, "Standard": 25, "Premium": 50, "VIP": 100}
        max_withdraw_map = {"Starter": 200, "Standard": 500, "Premium": 1000, "VIP": 5000}
        plan_name = plan.name.split()[0]
        min_wd = min_withdraw_map.get(plan_name, 10)
        max_wd = max_withdraw_map.get(plan_name, 200)
        
        plan_info_html = f"""
        <div style="background:rgba(0,255,100,0.08);border:1px solid rgba(0,255,100,0.2);border-radius:12px;padding:18px;margin:15px 0;">
            <h3 style="color:#4ade80;">✅ Plan ou: {plan.name}</h3>
            <p style="color:rgba(255,255,255,0.7);">📅 Kòmanse: {active_plan_info['user_plan'].start_date.strftime('%d/%m/%Y')}</p>
            <p style="color:rgba(255,255,255,0.7);">⏳ Ekspire: {exp_date.strftime('%d/%m/%Y')}</p>
            <p style="color:rgba(255,255,255,0.7);">💰 Min retrè: {min_wd} USDT | Maks: {max_wd} USDT</p>
        </div>
        """
    else:
        plan_info_html = """
        <div style="background:rgba(255,150,0,0.08);border:1px solid rgba(255,150,0,0.2);border-radius:12px;padding:18px;margin:15px 0;">
            <p style="color:#fbbf24;">⚠️ Ou pa gen plan aktif. Achte yon plan pou kòmanse fè retrè.</p>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <title>Dashboard - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:560px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div>
                    <h1 style="color:#ffffff;font-size:22px;">👋 {user.username}</h1>
                    <p style="color:rgba(255,255,255,0.4);font-size:12px;">Dashboard</p>
                </div>
                <a href="/logout" style="color:#ff6b6b;text-decoration:none;font-size:14px;">Dekonekte</a>
            </div>
            
            <div style="background:rgba(255,215,0,0.05);border-radius:16px;padding:20px;border:1px solid rgba(255,215,0,0.1);">
                <p style="color:rgba(255,255,255,0.5);font-size:13px;">BALANS</p>
                <p style="color:#ffffff;font-size:32px;font-weight:700;">{user.balance} <span style="color:#ffd700;font-size:18px;">USDT</span></p>
            </div>
            
            {plan_info_html}
            
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:15px 0;">
                <a href="/deposit-page" style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.2);border-radius:12px;padding:14px;text-align:center;color:#ffffff;text-decoration:none;font-weight:600;">💰 Depo</a>
                <a href="/referral" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:14px;text-align:center;color:#ffffff;text-decoration:none;font-weight:600;">👥 Referral</a>
            </div>
            
            <h3 style="color:#ffffff;font-size:18px;margin-top:20px;">Fè yon Retrè</h3>
            <form method="post" action="/withdraw">
                <div class="form-group">
                    <input type="number" name="amount" placeholder="Montan USDT" step="0.01" required>
                </div>
                <div class="form-group">
                    <input type="text" name="wallet" placeholder="Adrès TRC20 ou" required>
                </div>
                <button type="submit" class="btn btn-secondary">Voye demann retrè</button>
            </form>
            <p style="color:rgba(255,255,255,0.3);font-size:12px;text-align:center;margin-top:10px;">⚠️ Retrè ap tann apwobasyon admin</p>
            
            <h3 style="color:#ffffff;font-size:18px;margin-top:25px;">Plan VestiCore</h3>
            {plan_html}
            
            <div style="text-align:center;margin-top:20px;border-top:1px solid rgba(255,255,255,0.05);padding-top:20px;">
                <a href="/admin" style="color:rgba(255,255,255,0.2);text-decoration:none;font-size:12px;">Admin</a>
            </div>
        </div>
    </body>
    </html>
    """

# =====================
# DEPOSIT PAGE
# =====================

@app.get("/deposit-page", response_class=HTMLResponse)
def deposit_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    return f"""
    <html>
    <head>
        <title>Depo - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo()}
            <div class="title">💰 Depo USDT</div>
            
            <div style="background:rgba(255,0,0,0.08);border:1px solid rgba(255,0,0,0.2);border-radius:12px;padding:16px;margin-bottom:20px;">
                <p style="color:#ff6b6b;font-weight:700;text-align:center;">⚠️ Sèlman USDT sou TRC20 (Tron)</p>
            </div>
            
            <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:18px;border:1px solid rgba(255,255,255,0.05);">
                <p style="color:rgba(255,255,255,0.5);font-size:12px;">🌐 REZO</p>
                <p style="color:#4ade80;font-weight:700;font-size:18px;">TRC20 (Tron)</p>
                
                <p style="color:rgba(255,255,255,0.5);font-size:12px;margin-top:12px;">🏦 ADRÈS PORTEFEUILLE</p>
                <p style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;color:#ffd700;font-size:14px;word-break:break-all;font-family:monospace;">{USDT_TRON_ADDRESS}</p>
                
                <p style="color:rgba(255,255,255,0.5);font-size:12px;margin-top:12px;">📄 ADRÈS KONTRA</p>
                <p style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;color:rgba(255,255,255,0.6);font-size:12px;word-break:break-all;font-family:monospace;">{USDT_CONTRACT_ADDRESS}</p>
                
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;">
                    <div><p style="color:rgba(255,255,255,0.4);font-size:11px;">💸 FRÈ</p><p style="color:#ffffff;">{DEPOSIT_FEE}%</p></div>
                    <div><p style="color:rgba(255,255,255,0.4);font-size:11px;">⏱️ TAN</p><p style="color:#ffffff;">~1-2 min</p></div>
                </div>
            </div>
            
            <h3 style="color:#ffffff;font-size:16px;margin:20px 0 15px;">Vèrifye depo w</h3>
            <form method="post" action="/deposit">
                <div class="form-group">
                    <input type="number" name="amount" placeholder="Montan USDT" step="0.01" required>
                </div>
                <div class="form-group">
                    <input type="text" name="txid" placeholder="ID tranzaksyon (txid)" required>
                </div>
                <button type="submit" class="btn">Voye depo</button>
            </form>
            
            <div class="link" style="margin-top:20px;">
                <a href="/dashboard">← Retounen Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """

# =====================
# DEPOSIT POST
# =====================

@app.post("/deposit")
def deposit(
    request: Request,
    amount: float = Form(...),
    txid: str = Form(...),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Montan pa valab")
    
    deposit = Deposit(username=user.username, amount=amount, txid=txid, status="pending")
    db.add(deposit)
    add_log(db, user.username, f"Depo {amount} USDT voye pou verifikasyon")
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

# =====================
# BUY PLAN
# =====================

@app.post("/buy-plan")
def buy_plan(
    request: Request,
    plan_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)
    
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan pa jwenn")
    
    existing = db.query(UserPlan).filter(
        UserPlan.user_id == user.id,
        UserPlan.status == "active"
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Ou deja gen yon plan aktif")
    
    if user.balance < plan.price:
        raise HTTPException(status_code=400, detail="Balans pa ase pou achte plan sa")
    
    user.balance -= plan.price
    
    user_plan = UserPlan(
        user_id=user.id,
        plan_id=plan.id,
        amount=plan.price,
        status="active",
        start_date=datetime.now()
    )
    db.add(user_plan)
    
    add_log(db, user.username, f"Achte plan {plan.name} pou {plan.price} USDT")
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

# =====================
# WITHDRAW
# =====================

@app.post("/withdraw")
def withdraw(
    request: Request,
    amount: float = Form(...),
    wallet: str = Form(...),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)
    
    active_plan_info = get_user_active_plan(db, user.id)
    
    if not active_plan_info:
        raise HTTPException(
            status_code=403,
            detail="Ou dwe achte yon plan anvan ou ka fè retrè"
        )
    
    plan = active_plan_info["plan"]
    
    min_withdraw_map = {"Starter": 10, "Standard": 25, "Premium": 50, "VIP": 100}
    max_withdraw_map = {"Starter": 200, "Standard": 500, "Premium": 1000, "VIP": 5000}
    
    plan_name = plan.name.split()[0]
    min_withdraw = min_withdraw_map.get(plan_name, 10)
    max_withdraw = max_withdraw_map.get(plan_name, 200)
    
    if amount < min_withdraw:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum retrè pou plan {plan_name} se {min_withdraw} USDT"
        )
    
    if amount > max_withdraw:
        raise HTTPException(
            status_code=400,
            detail=f"Maksimòm retrè pou plan {plan_name} se {max_withdraw} USDT"
        )
    
    if user.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Balans pa ase"
        )
    
    fee = amount * WITHDRAW_FEE / 100
    net_amount = amount - fee
    
    withdraw = Withdraw(
        username=user.username,
        amount=net_amount,
        wallet=wallet,
        status="pending"
    )
    
    db.add(withdraw)
    add_log(db, user.username, f"Demann retrè {amount} USDT voye - Plan {plan_name}")
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

# =====================
# REFERRAL
# =====================

@app.get("/referral", response_class=HTMLResponse)
def referral_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    referrals = db.query(Referral).filter(Referral.referrer == user.referral_code).all()
    
    return f"""
    <html>
    <head>
        <title>Referral - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo()}
            <div class="title">👥 Referral</div>
            
            <div style="background:rgba(255,215,0,0.05);border-radius:12px;padding:18px;border:1px solid rgba(255,215,0,0.1);">
                <p style="color:rgba(255,255,255,0.5);font-size:12px;">KÒD REFERRAL OU</p>
                <p style="color:#ffd700;font-size:24px;font-weight:700;font-family:monospace;">{user.referral_code}</p>
            </div>
            
            <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:15px;margin-top:15px;">
                <p style="color:rgba(255,255,255,0.5);font-size:12px;">LYEN ENVITASYON</p>
                <p style="background:rgba(0,0,0,0.3);padding:10px;border-radius:8px;color:rgba(255,255,255,0.7);font-size:12px;word-break:break-all;">/register?ref={user.referral_code}</p>
            </div>
            
            <div style="text-align:center;margin-top:20px;">
                <p style="color:rgba(255,255,255,0.5);">Moun ou envite: <span style="color:#ffd700;font-weight:700;font-size:20px;">{len(referrals)}</span></p>
            </div>
            
            <div class="link" style="margin-top:20px;">
                <a href="/dashboard">← Retounen Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """

# =====================
# ADMIN DASHBOARD
# =====================

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    admin_user(request, db)
    users = db.query(User).all()
    deposits = db.query(Deposit).all()
    withdraws = db.query(Withdraw).all()
    logs = db.query(ActivityLog).all()
    user_plans = db.query(UserPlan).all()
    
    pending_deposits = db.query(Deposit).filter(Deposit.status == "pending").all()
    pending_withdraws = db.query(Withdraw).filter(Withdraw.status == "pending").all()
    
    deposit_html = ""
    for d in pending_deposits:
        deposit_html += f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px;margin:8px 0;border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#ffffff;"><strong>{d.username}</strong> - {d.amount} USDT</p>
            <p style="color:rgba(255,255,255,0.4);font-size:12px;">TXID: {d.txid}</p>
            <p style="color:rgba(255,255,255,0.3);font-size:11px;">{d.date.strftime('%d/%m/%Y %H:%M')}</p>
            <div style="display:flex;gap:8px;margin-top:8px;">
                <form method="post" action="/admin/approve-deposit/{d.id}" style="display:inline;">
                    <button style="background:#4ade80;border:none;padding:8px 18px;border-radius:8px;color:#0a0e27;font-weight:700;cursor:pointer;">Apwouve</button>
                </form>
                <form method="post" action="/admin/reject-deposit/{d.id}" style="display:inline;">
                    <button style="background:#ff6b6b;border:none;padding:8px 18px;border-radius:8px;color:#ffffff;font-weight:700;cursor:pointer;">Rejete</button>
                </form>
            </div>
        </div>
        """
    
    withdraw_html = ""
    for w in pending_withdraws:
        withdraw_html += f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px;margin:8px 0;border:1px solid rgba(255,255,255,0.05);">
            <p style="color:#ffffff;"><strong>{w.username}</strong> - {w.amount} USDT</p>
            <p style="color:rgba(255,255,255,0.4);font-size:12px;">Wallet: {w.wallet}</p>
            <p style="color:rgba(255,255,255,0.3);font-size:11px;">{w.date.strftime('%d/%m/%Y %H:%M')}</p>
            <div style="display:flex;gap:8px;margin-top:8px;">
                <form method="post" action="/admin/approve-withdraw/{w.id}" style="display:inline;">
                    <button style="background:#4ade80;border:none;padding:8px 18px;border-radius:8px;color:#0a0e27;font-weight:700;cursor:pointer;">Apwouve</button>
                </form>
                <form method="post" action="/admin/reject-withdraw/{w.id}" style="display:inline;">
                    <button style="background:#ff6b6b;border:none;padding:8px 18px;border-radius:8px;color:#ffffff;font-weight:700;cursor:pointer;">Rejete</button>
                </form>
            </div>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <title>Admin - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:560px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div>
                    <h1 style="color:#ffffff;font-size:22px;">🛡️ Admin</h1>
                    <p style="color:rgba(255,255,255,0.4);font-size:12px;">Dashboard administrasyon</p>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.4);text-decoration:none;font-size:13px;">← Retounen</a>
            </div>
            
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:20px;">
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.4);font-size:10px;">ITILIZATÈ</p>
                    <p style="color:#ffffff;font-size:24px;font-weight:700;">{len(users)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.4);font-size:10px;">DEPO</p>
                    <p style="color:#4ade80;font-size:24px;font-weight:700;">{len(deposits)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.4);font-size:10px;">RETRÈ</p>
                    <p style="color:#fbbf24;font-size:24px;font-weight:700;">{len(withdraws)}</p>
                </div>
            </div>
            
            <h3 style="color:#ffd700;font-size:16px;">⏳ Depo annatant</h3>
            {deposit_html if deposit_html else "<p style='color:rgba(255,255,255,0.3);font-size:14px;'>Pa gen depo annatant</p>"}
            
            <h3 style="color:#ffd700;font-size:16px;margin-top:15px;">⏳ Retrè annatant</h3>
            {withdraw_html if withdraw_html else "<p style='color:rgba(255,255,255,0.3);font-size:14px;'>Pa gen retrè annatant</p>"}
            
            <div style="margin-top:20px;border-top:1px solid rgba(255,255,255,0.05);padding-top:15px;">
                <p style="color:rgba(255,255,255,0.2);font-size:11px;">Dènye aktivite</p>
                <ul style="list-style:none;padding:0;max-height:150px;overflow-y:auto;">
                {''.join([f"<li style='color:rgba(255,255,255,0.3);font-size:11px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.02);'>{log.date.strftime('%d/%m %H:%M')} - {log.username}: {log.action}</li>" for log in logs[-15:]])}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

# =====================
# ADMIN APPROVE DEPOSIT
# =====================

@app.post("/admin/approve-deposit/{deposit_id}")
def approve_deposit(
    deposit_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    deposit = db.query(Deposit).filter(Deposit.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Depo pa jwenn")
    if deposit.status != "pending":
        raise HTTPException(status_code=400, detail="Depo sa deja trete")
    deposit.status = "approved"
    user = db.query(User).filter(User.username == deposit.username).first()
    if user:
        user.balance += deposit.amount
    add_log(db, deposit.username, f"Depo {deposit.amount} USDT apwouve")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# =====================
# ADMIN REJECT DEPOSIT
# =====================

@app.post("/admin/reject-deposit/{deposit_id}")
def reject_deposit(
    deposit_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    deposit = db.query(Deposit).filter(Deposit.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Depo pa jwenn")
    if deposit.status != "pending":
        raise HTTPException(status_code=400, detail="Depo sa deja trete")
    deposit.status = "rejected"
    add_log(db, deposit.username, f"Depo {deposit.amount} USDT rejete")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# =====================
# ADMIN APPROVE WITHDRAW
# =====================

@app.post("/admin/approve-withdraw/{withdraw_id}")
def approve_withdraw(
    withdraw_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    withdraw = db.query(Withdraw).filter(Withdraw.id == withdraw_id).first()
    if not withdraw:
        raise HTTPException(status_code=404, detail="Demann retrè pa jwenn")
    if withdraw.status != "pending":
        raise HTTPException(status_code=400, detail="Demann sa deja trete")
    withdraw.status = "approved"
    user = db.query(User).filter(User.username == withdraw.username).first()
    if user:
        user.balance -= withdraw.amount
    add_log(db, withdraw.username, f"Retrè {withdraw.amount} USDT apwouve")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# =====================
# ADMIN REJECT WITHDRAW
# =====================

@app.post("/admin/reject-withdraw/{withdraw_id}")
def reject_withdraw(
    withdraw_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    withdraw = db.query(Withdraw).filter(Withdraw.id == withdraw_id).first()
    if not withdraw:
        raise HTTPException(status_code=404, detail="Demann retrè pa jwenn")
    if withdraw.status != "pending":
        raise HTTPException(status_code=400, detail="Demann sa deja trete")
    withdraw.status = "rejected"
    add_log(db, withdraw.username, f"Retrè {withdraw.amount} USDT rejete")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# =====================
# LOGOUT
# =====================

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# =====================
# HEALTH CHECK
# =====================

@app.get("/status")
def status():
    return {"platform": "VestiCore", "status": "online"}

# =====================
# INITIAL PLANS
# =====================

@app.on_event("startup")
def startup_plans():
    db = next(get_db())
    total = db.query(Plan).count()
    if total == 0:
        plans = [
            Plan(name="Starter Basic", price=10, duration=30, description="Plan Starter debaz - 30 jou"),
            Plan(name="Starter Plus", price=25, duration=30, description="Plan Starter Plus - 30 jou"),
            Plan(name="Standard Basic", price=50, duration=60, description="Plan Standard debaz - 60 jou"),
            Plan(name="Standard Plus", price=100, duration=60, description="Plan Standard Plus - 60 jou"),
            Plan(name="Premium Basic", price=200, duration=90, description="Plan Premium debaz - 90 jou"),
            Plan(name="Premium Plus", price=350, duration=90, description="Plan Premium Plus - 90 jou"),
            Plan(name="Premium Pro", price=500, duration=90, description="Plan Premium Pro - 90 jou"),
            Plan(name="VIP Basic", price=750, duration=120, description="Plan VIP debaz - 120 jou"),
            Plan(name="VIP Plus", price=1000, duration=120, description="Plan VIP Plus - 120 jou"),
            Plan(name="VIP Pro", price=2000, duration=120, description="Plan VIP Pro - 120 jou")
        ]
        db.add_all(plans)
        db.commit()
    db.close()

# =====================
# RUN
# =====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
