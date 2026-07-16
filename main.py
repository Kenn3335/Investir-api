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
# KLE SEKRE POU ADMIN (SOLISYON 3)
# =====================

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "vesticore-admin-2026")

# =====================
# TEXTE POU CHAK LANG
# =====================

LANG = {
    "fr": {
        "title": "VestiCore - Plateforme d'investissement",
        "logo_sub": "INVEST • CROISSANCE • PROSPÉRITÉ",
        "home_title": "Plateforme d'investissement numérique",
        "home_desc": "Faites fructifier votre argent",
        "home_btn_register": "Créer un compte",
        "home_btn_login": "Se connecter",
        "register_title": "Créer votre compte",
        "register_sub": "Commencez votre voyage d'investissement",
        "register_username": "Nom d'utilisateur",
        "register_password": "Mot de passe",
        "register_ref": "Code de parrainage (optionnel)",
        "register_btn": "Créer un compte",
        "register_link": "Vous avez déjà un compte?",
        "register_link_btn": "Se connecter",
        "login_title": "Bienvenue de retour",
        "login_sub": "Connectez-vous pour accéder à votre espace",
        "login_btn": "Se connecter",
        "login_link": "Pas de compte?",
        "login_link_btn": "Créer un compte",
        "dashboard_balance": "SOLDE",
        "dashboard_withdraw": "Faire un retrait",
        "dashboard_withdraw_placeholder": "Montant USDT",
        "dashboard_withdraw_wallet": "Votre adresse TRC20",
        "dashboard_withdraw_btn": "Envoyer la demande",
        "dashboard_withdraw_warning": "⚠️ Les retraits sont soumis à l'approbation de l'administrateur",
        "dashboard_plans": "Plans VestiCore",
        "dashboard_buy": "Acheter ce plan",
        "dashboard_no_plan": "⚠️ Vous n'avez pas de plan actif. Achetez un plan pour commencer à faire des retraits.",
        "dashboard_plan_active": "✅ Votre plan:",
        "dashboard_plan_start": "📅 Début:",
        "dashboard_plan_expire": "⏳ Expire:",
        "dashboard_plan_min": "💰 Retrait min:",
        "dashboard_plan_max": "📈 Retrait max:",
        "deposit_title": "💰 Dépôt USDT",
        "deposit_warning": "⚠️ Envoyer UNIQUEMENT USDT sur TRC20 (Tron)",
        "deposit_network": "🌐 RÉSEAU",
        "deposit_address": "🏦 ADRESSE PORTEFEUILLE",
        "deposit_contract": "📄 ADRESSE CONTRAT",
        "deposit_fee": "💸 FRAIS",
        "deposit_time": "⏱️ TEMPS",
        "deposit_verify": "Vérifier votre dépôt",
        "deposit_amount": "Montant USDT",
        "deposit_txid": "ID de transaction (txid)",
        "deposit_btn": "Envoyer le dépôt",
        "deposit_back": "← Retour au Dashboard",
        "referral_title": "👥 Parrainage",
        "referral_code": "VOTRE CODE DE PARRAINAGE",
        "referral_link": "LIEN D'INVITATION",
        "referral_count": "Personnes que vous avez invitées:",
        "referral_back": "← Retour au Dashboard",
        "logout": "Déconnexion",
        "admin_title": "🛡️ Administration",
        "admin_sub": "Tableau de bord administrateur",
        "admin_users": "UTILISATEURS",
        "admin_deposits": "DÉPÔTS",
        "admin_withdraws": "RETRAITS",
        "admin_pending_deposits": "⏳ Dépôts en attente",
        "admin_pending_withdraws": "⏳ Retraits en attente",
        "admin_no_pending": "Aucune demande en attente",
        "admin_approve": "Approuver",
        "admin_reject": "Rejeter",
        "admin_recent": "Activités récentes",
        "admin_back": "← Retour",
        "footer": "© 2026 VestiCore. Tous droits réservés.",
        "select_lang": "🌐 Langue"
    },
    "en": {
        "title": "VestiCore - Investment Platform",
        "logo_sub": "INVEST • GROW • PROSPER",
        "home_title": "Digital Investment Platform",
        "home_desc": "Make your money grow",
        "home_btn_register": "Create account",
        "home_btn_login": "Login",
        "register_title": "Create your account",
        "register_sub": "Start your investment journey",
        "register_username": "Username",
        "register_password": "Password",
        "register_ref": "Referral code (optional)",
        "register_btn": "Create account",
        "register_link": "Already have an account?",
        "register_link_btn": "Login",
        "login_title": "Welcome back",
        "login_sub": "Login to access your space",
        "login_btn": "Login",
        "login_link": "No account?",
        "login_link_btn": "Create account",
        "dashboard_balance": "BALANCE",
        "dashboard_withdraw": "Make a Withdrawal",
        "dashboard_withdraw_placeholder": "USDT Amount",
        "dashboard_withdraw_wallet": "Your TRC20 address",
        "dashboard_withdraw_btn": "Submit request",
        "dashboard_withdraw_warning": "⚠️ Withdrawals are subject to admin approval",
        "dashboard_plans": "VestiCore Plans",
        "dashboard_buy": "Buy this plan",
        "dashboard_no_plan": "⚠️ You don't have an active plan. Buy a plan to start withdrawing.",
        "dashboard_plan_active": "✅ Your plan:",
        "dashboard_plan_start": "📅 Start:",
        "dashboard_plan_expire": "⏳ Expires:",
        "dashboard_plan_min": "💰 Min withdraw:",
        "dashboard_plan_max": "📈 Max withdraw:",
        "deposit_title": "💰 USDT Deposit",
        "deposit_warning": "⚠️ Send ONLY USDT on TRC20 (Tron)",
        "deposit_network": "🌐 NETWORK",
        "deposit_address": "🏦 WALLET ADDRESS",
        "deposit_contract": "📄 CONTRACT ADDRESS",
        "deposit_fee": "💸 FEE",
        "deposit_time": "⏱️ TIME",
        "deposit_verify": "Verify your deposit",
        "deposit_amount": "USDT Amount",
        "deposit_txid": "Transaction ID (txid)",
        "deposit_btn": "Submit deposit",
        "deposit_back": "← Back to Dashboard",
        "referral_title": "👥 Referral",
        "referral_code": "YOUR REFERRAL CODE",
        "referral_link": "INVITATION LINK",
        "referral_count": "People you invited:",
        "referral_back": "← Back to Dashboard",
        "logout": "Logout",
        "admin_title": "🛡️ Admin",
        "admin_sub": "Admin Dashboard",
        "admin_users": "USERS",
        "admin_deposits": "DEPOSITS",
        "admin_withdraws": "WITHDRAWALS",
        "admin_pending_deposits": "⏳ Pending deposits",
        "admin_pending_withdraws": "⏳ Pending withdrawals",
        "admin_no_pending": "No pending requests",
        "admin_approve": "Approve",
        "admin_reject": "Reject",
        "admin_recent": "Recent activities",
        "admin_back": "← Back",
        "footer": "© 2026 VestiCore. All rights reserved.",
        "select_lang": "🌐 Language"
    },
    "es": {
        "title": "VestiCore - Plataforma de Inversión",
        "logo_sub": "INVIERTE • CRECE • PROSPERA",
        "home_title": "Plataforma de Inversión Digital",
        "home_desc": "Haz crecer tu dinero",
        "home_btn_register": "Crear cuenta",
        "home_btn_login": "Iniciar sesión",
        "register_title": "Crea tu cuenta",
        "register_sub": "Comienza tu viaje de inversión",
        "register_username": "Nombre de usuario",
        "register_password": "Contraseña",
        "register_ref": "Código de referencia (opcional)",
        "register_btn": "Crear cuenta",
        "register_link": "¿Ya tienes una cuenta?",
        "register_link_btn": "Iniciar sesión",
        "login_title": "Bienvenido de nuevo",
        "login_sub": "Inicia sesión para acceder a tu espacio",
        "login_btn": "Iniciar sesión",
        "login_link": "¿No tienes cuenta?",
        "login_link_btn": "Crear cuenta",
        "dashboard_balance": "SALDO",
        "dashboard_withdraw": "Hacer un retiro",
        "dashboard_withdraw_placeholder": "Monto USDT",
        "dashboard_withdraw_wallet": "Tu dirección TRC20",
        "dashboard_withdraw_btn": "Enviar solicitud",
        "dashboard_withdraw_warning": "⚠️ Los retiros están sujetos a aprobación del administrador",
        "dashboard_plans": "Planes VestiCore",
        "dashboard_buy": "Comprar este plan",
        "dashboard_no_plan": "⚠️ No tienes un plan activo. Compra un plan para comenzar a retirar.",
        "dashboard_plan_active": "✅ Tu plan:",
        "dashboard_plan_start": "📅 Inicio:",
        "dashboard_plan_expire": "⏳ Expira:",
        "dashboard_plan_min": "💰 Retiro mínimo:",
        "dashboard_plan_max": "📈 Retiro máximo:",
        "deposit_title": "💰 Depósito USDT",
        "deposit_warning": "⚠️ Enviar SOLAMENTE USDT en TRC20 (Tron)",
        "deposit_network": "🌐 RED",
        "deposit_address": "🏦 DIRECCIÓN DE BILLETERA",
        "deposit_contract": "📄 DIRECCIÓN DEL CONTRATO",
        "deposit_fee": "💸 COMISIÓN",
        "deposit_time": "⏱️ TIEMPO",
        "deposit_verify": "Verifica tu depósito",
        "deposit_amount": "Monto USDT",
        "deposit_txid": "ID de transacción (txid)",
        "deposit_btn": "Enviar depósito",
        "deposit_back": "← Volver al Dashboard",
        "referral_title": "👥 Referidos",
        "referral_code": "TU CÓDIGO DE REFERIDO",
        "referral_link": "ENLACE DE INVITACIÓN",
        "referral_count": "Personas que invitaste:",
        "referral_back": "← Volver al Dashboard",
        "logout": "Cerrar sesión",
        "admin_title": "🛡️ Administración",
        "admin_sub": "Panel de administración",
        "admin_users": "USUARIOS",
        "admin_deposits": "DEPÓSITOS",
        "admin_withdraws": "RETIROS",
        "admin_pending_deposits": "⏳ Depósitos pendientes",
        "admin_pending_withdraws": "⏳ Retiros pendientes",
        "admin_no_pending": "No hay solicitudes pendientes",
        "admin_approve": "Aprobar",
        "admin_reject": "Rechazar",
        "admin_recent": "Actividades recientes",
        "admin_back": "← Volver",
        "footer": "© 2026 VestiCore. Todos los derechos reservados.",
        "select_lang": "🌐 Idioma"
    }
}

# =====================
# FONKSYON POU JWENN LANG
# =====================

def get_lang(request: Request):
    lang = request.cookies.get("lang", "fr")
    if lang not in LANG:
        lang = "fr"
    return lang

def t(request: Request, key: str):
    lang = get_lang(request)
    return LANG[lang].get(key, key)

# =====================
# STIL CSS
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
        max-width: 520px;
        width: 100%;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(255, 215, 0, 0.05);
    }
    .logo {
        text-align: center;
        margin-bottom: 25px;
    }
    .logo-icon {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border-radius: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        font-weight: 900;
        color: #0a0e27;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 12px;
    }
    .logo h1 {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .logo h1 span {
        color: #ffd700;
    }
    .logo p {
        color: rgba(255, 255, 255, 0.4);
        font-size: 11px;
        margin-top: 4px;
        letter-spacing: 3px;
    }
    .lang-selector {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        margin-bottom: 15px;
    }
    .lang-selector a {
        color: rgba(255, 255, 255, 0.3);
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        transition: all 0.3s;
    }
    .lang-selector a:hover {
        color: #ffd700;
        background: rgba(255, 215, 0, 0.1);
    }
    .lang-selector a.active {
        color: #ffd700;
        background: rgba(255, 215, 0, 0.15);
    }
    .title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 6px;
        text-align: center;
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.4);
        font-size: 13px;
        text-align: center;
        margin-bottom: 22px;
    }
    .form-group {
        margin-bottom: 16px;
    }
    .form-group label {
        display: block;
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    .form-group input {
        width: 100%;
        padding: 13px 16px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        color: #ffffff;
        font-size: 14px;
        transition: all 0.3s ease;
        outline: none;
    }
    .form-group input:focus {
        border-color: #ffd700;
        background: rgba(255, 215, 0, 0.05);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.08);
    }
    .form-group input::placeholder {
        color: rgba(255, 255, 255, 0.2);
    }
    .btn {
        width: 100%;
        padding: 15px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border: none;
        border-radius: 10px;
        color: #0a0e27;
        font-size: 15px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
        margin-top: 6px;
        text-align: center;
        text-decoration: none;
        display: block;
    }
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    .btn-secondary {
        background: rgba(255, 255, 255, 0.06);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.12);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.05);
    }
    .link {
        text-align: center;
        margin-top: 18px;
        color: rgba(255, 255, 255, 0.35);
        font-size: 13px;
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
    .footer-text {
        text-align: center;
        margin-top: 20px;
        color: rgba(255, 255, 255, 0.15);
        font-size: 11px;
        letter-spacing: 1px;
    }
    @media (max-width: 480px) {
        .container { padding: 25px 18px; }
        .logo h1 { font-size: 24px; }
        .logo-icon { width: 55px; height: 55px; font-size: 28px; }
        .lang-selector a { font-size: 10px; padding: 3px 8px; }
    }
</style>
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
# SELÈKSYON LANG
# =====================

@app.get("/set-lang/{lang}")
def set_lang(lang: str, request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="lang", value=lang, max_age=365*24*60*60)
    return response

# =====================
# LOGO AVEC LANG
# =====================

def get_logo_html(lang_key, request):
    return f"""
    <div class="lang-selector">
        <a href="/set-lang/fr" class="{'active' if lang_key == 'fr' else ''}">FR</a>
        <a href="/set-lang/en" class="{'active' if lang_key == 'en' else ''}">EN</a>
        <a href="/set-lang/es" class="{'active' if lang_key == 'es' else ''}">ES</a>
    </div>
    <div class="logo">
        <div class="logo-icon">V</div>
        <h1>Vesti<span>Core</span></h1>
        <p>{LANG[lang_key].get('logo_sub', 'INVEST • GROW • PROSPER')}</p>
    </div>
    """

# =====================
# HOME PAGE
# =====================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    lang = get_lang(request)
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('title', 'VestiCore')}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo_html(lang, request)}
            <div style="text-align:center;margin:5px 0 25px;">
                <p style="color:rgba(255,255,255,0.6);font-size:14px;line-height:1.6;">
                    {LANG[lang].get('home_title', 'Digital Investment Platform')}<br>
                    <span style="color:#ffd700;">{LANG[lang].get('home_desc', 'Make your money grow')}</span>
                </p>
            </div>
            <a href="/register" class="btn">{LANG[lang].get('home_btn_register', 'Create account')}</a>
            <br><br>
            <a href="/login" class="btn btn-secondary">{LANG[lang].get('home_btn_login', 'Login')}</a>
            <div class="footer-text">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</div>
        </div>
    </body>
    </html>
    """

# =====================
# REGISTER PAGE
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    lang = get_lang(request)
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('title', 'VestiCore')}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo_html(lang, request)}
            <div class="title">{LANG[lang].get('register_title', 'Create your account')}</div>
            <div class="subtitle">{LANG[lang].get('register_sub', 'Start your investment journey')}</div>
            <form method="post">
                <div class="form-group">
                    <label>{LANG[lang].get('register_username', 'Username')}</label>
                    <input type="text" name="username" placeholder="{LANG[lang].get('register_username', 'Username')}" required>
                </div>
                <div class="form-group">
                    <label>{LANG[lang].get('register_password', 'Password')}</label>
                    <input type="password" name="password" placeholder="{LANG[lang].get('register_password', 'Password')}" required>
                </div>
                <div class="form-group">
                    <label>{LANG[lang].get('register_ref', 'Referral code (optional)')}</label>
                    <input type="text" name="ref" placeholder="{LANG[lang].get('register_ref', 'Referral code (optional)')}">
                </div>
                <button type="submit" class="btn">{LANG[lang].get('register_btn', 'Create account')}</button>
            </form>
            <div class="link">
                {LANG[lang].get('register_link', 'Already have an account?')} <a href="/login">{LANG[lang].get('register_link_btn', 'Login')}</a>
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
    
    # ========================================
    # SOLISYON 3: SÈLMAN KLE SEKRE A KA FÈ ADMIN
    # ========================================
    is_admin = 1 if ref == ADMIN_SECRET_KEY else 0
    
    new_user = User(
        username=username,
        password=hash_password(password),
        referral_code=create_referral_code(username),
        referred_by=ref,
        is_admin=is_admin
    )
    db.add(new_user)
    if ref:
        referral = Referral(referrer=ref, invited_user=username)
        db.add(referral)
    add_log(db, username, "Kreye nouvo kont")
    db.commit()
    return RedirectResponse(url="/login", status_code=303)
