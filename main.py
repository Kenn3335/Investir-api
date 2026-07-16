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
# KLE SEKRE POU ADMIN
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

# =====================
# REGISTER ACTION (KORIJE)
# =====================

@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    ref: str = Form(None),
    db: Session = Depends(get_db)
):
    # Verifye si kont deja egziste
    user_exist = db.query(User).filter(User.username == username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Kont sa deja egziste")
    
    # Tcheke si ref la se kle admin an
    admin_key = os.getenv("ADMIN_SECRET_KEY", "vesticore-admin-2026")
    
    # Si ref la egal ak kle admin an, li vin admin
    if ref and ref.strip() == admin_key.strip():
        is_admin = 1
        referred_by = ""  # Pa gen referral
    else:
        is_admin = 0
        referred_by = ref if ref else ""  # Referral normal oswa vid
    
    # Kreye nouvo itilizatè
    new_user = User(
        username=username,
        password=hash_password(password),
        referral_code=create_referral_code(username),
        referred_by=referred_by,
        is_admin=is_admin
    )
    db.add(new_user)
    
    # Si se yon referral normal (pa kle admin an)
    if ref and ref.strip() != admin_key.strip():
        referral = Referral(referrer=ref, invited_user=username)
        db.add(referral)
    
    add_log(db, username, "Kreye nouvo kont")
    db.commit()
    
    return RedirectResponse(url="/login", status_code=303)

# =====================
# LOGIN PAGE
# =====================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
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
            <div class="title">{LANG[lang].get('login_title', 'Welcome back')}</div>
            <div class="subtitle">{LANG[lang].get('login_sub', 'Login to access your space')}</div>
            <form method="post">
                <div class="form-group">
                    <label>{LANG[lang].get('register_username', 'Username')}</label>
                    <input type="text" name="username" placeholder="{LANG[lang].get('register_username', 'Username')}" required>
                </div>
                <div class="form-group">
                    <label>{LANG[lang].get('register_password', 'Password')}</label>
                    <input type="password" name="password" placeholder="{LANG[lang].get('register_password', 'Password')}" required>
                </div>
                <button type="submit" class="btn">{LANG[lang].get('login_btn', 'Login')}</button>
            </form>
            <div class="link">
                {LANG[lang].get('login_link', 'No account?')} <a href="/register">{LANG[lang].get('login_link_btn', 'Create account')}</a>
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
    lang = get_lang(request)
    user = current_user(request, db)
    plans = db.query(Plan).all()
    active_plan_info = get_user_active_plan(db, user.id)
    
    plan_html = ""
    for plan in plans:
        plan_html += f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:16px;margin:8px 0;border:1px solid rgba(255,215,0,0.06);">
            <h3 style="color:#ffd700;font-size:16px;">{plan.name}</h3>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;">{plan.description}</p>
            <p style="color:rgba(255,255,255,0.3);font-size:12px;">⏳ {plan.duration} {LANG[lang].get('days', 'days') if lang == 'en' else 'jou' if lang == 'fr' else 'días'}</p>
            <p style="color:#ffffff;font-size:18px;font-weight:700;margin:6px 0;">{plan.price} USDT</p>
            <form method="post" action="/buy-plan">
                <input type="hidden" name="plan_id" value="{plan.id}">
                <button style="width:100%;padding:10px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:8px;color:#0a0e27;font-weight:700;cursor:pointer;font-size:13px;">{LANG[lang].get('dashboard_buy', 'Buy this plan')}</button>
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
        <div style="background:rgba(0,255,100,0.06);border:1px solid rgba(0,255,100,0.15);border-radius:10px;padding:14px;margin:12px 0;">
            <h3 style="color:#4ade80;font-size:15px;">{LANG[lang].get('dashboard_plan_active', '✅ Your plan:')} {plan.name}</h3>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;">{LANG[lang].get('dashboard_plan_start', '📅 Start:')} {active_plan_info['user_plan'].start_date.strftime('%d/%m/%Y')}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;">{LANG[lang].get('dashboard_plan_expire', '⏳ Expires:')} {exp_date.strftime('%d/%m/%Y')}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:12px;">{LANG[lang].get('dashboard_plan_min', '💰 Min withdraw:')} {min_wd} USDT | {LANG[lang].get('dashboard_plan_max', '📈 Max withdraw:')} {max_wd} USDT</p>
        </div>
        """
    else:
        plan_info_html = f"""
        <div style="background:rgba(255,150,0,0.06);border:1px solid rgba(255,150,0,0.15);border-radius:10px;padding:14px;margin:12px 0;">
            <p style="color:#fbbf24;font-size:13px;">{LANG[lang].get('dashboard_no_plan', '⚠️ You don\'t have an active plan. Buy a plan to start withdrawing.')}</p>
        </div>
        """
    
    admin_link = f'<a href="/admin" style="color:rgba(255,255,255,0.12);text-decoration:none;font-size:11px;">Admin</a>' if user.is_admin == 1 else ''
    
    return f"""
    <html>
    <head>
        <title>Dashboard - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:560px;">
            {get_logo_html(lang, request)}
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
                <div>
                    <h1 style="color:#ffffff;font-size:20px;">👋 {user.username}</h1>
                    <p style="color:rgba(255,255,255,0.3);font-size:11px;">Dashboard</p>
                </div>
                <a href="/logout" style="color:#ff6b6b;text-decoration:none;font-size:13px;">{LANG[lang].get('logout', 'Logout')}</a>
            </div>
            <div style="background:rgba(255,215,0,0.04);border-radius:14px;padding:18px;border:1px solid rgba(255,215,0,0.08);">
                <p style="color:rgba(255,255,255,0.4);font-size:11px;">{LANG[lang].get('dashboard_balance', 'BALANCE')}</p>
                <p style="color:#ffffff;font-size:28px;font-weight:700;">{user.balance} <span style="color:#ffd700;font-size:16px;">USDT</span></p>
            </div>
            {plan_info_html}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">
                <a href="/deposit-page" style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.1);border-radius:10px;padding:12px;text-align:center;color:#ffffff;text-decoration:none;font-weight:600;font-size:13px;">💰 {LANG[lang].get('deposit_title', 'Deposit')}</a>
                <a href="/referral" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px;text-align:center;color:#ffffff;text-decoration:none;font-weight:600;font-size:13px;">👥 {LANG[lang].get('referral_title', 'Referral')}</a>
            </div>
            <h3 style="color:#ffffff;font-size:15px;margin-top:15px;">{LANG[lang].get('dashboard_withdraw', 'Make a Withdrawal')}</h3>
            <form method="post" action="/withdraw">
                <div class="form-group">
                    <input type="number" name="amount" placeholder="{LANG[lang].get('dashboard_withdraw_placeholder', 'USDT Amount')}" step="0.01" required>
                </div>
                <div class="form-group">
                    <input type="text" name="wallet" placeholder="{LANG[lang].get('dashboard_withdraw_wallet', 'Your TRC20 address')}" required>
                </div>
                <button type="submit" class="btn btn-secondary">{LANG[lang].get('dashboard_withdraw_btn', 'Submit request')}</button>
            </form>
            <p style="color:rgba(255,255,255,0.2);font-size:11px;text-align:center;margin-top:8px;">{LANG[lang].get('dashboard_withdraw_warning', '⚠️ Withdrawals are subject to admin approval')}</p>
            <h3 style="color:#ffffff;font-size:15px;margin-top:20px;">{LANG[lang].get('dashboard_plans', 'VestiCore Plans')}</h3>
            {plan_html}
            <div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">
                {admin_link}
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
    lang = get_lang(request)
    user = current_user(request, db)
    return f"""
    <html>
    <head>
        <title>Deposit - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            {get_logo_html(lang, request)}
            <div class="title">{LANG[lang].get('deposit_title', '💰 USDT Deposit')}</div>
            <div style="background:rgba(255,0,0,0.06);border:1px solid rgba(255,0,0,0.12);border-radius:10px;padding:14px;margin-bottom:16px;">
                <p style="color:#ff6b6b;font-weight:600;font-size:13px;text-align:center;">{LANG[lang].get('deposit_warning', '⚠️ Send ONLY USDT on TRC20 (Tron)')}</p>
            </div>
            <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:16px;border:1px solid rgba(255,255,255,0.04);">
                <p style="color:rgba(255,255,255,0.4);font-size:11px;">{LANG[lang].get('deposit_network', '🌐 NETWORK')}</p>
                <p style="color:#4ade80;font-weight:700;font-size:16px;">TRC20 (Tron)</p>
                <p style="color:rgba(255,255,255,0.4);font-size:11px;margin-top:10px;">{LANG[lang].get('deposit_address', '🏦 WALLET ADDRESS')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:10px;border-radius:6px;color:#ffd700;font-size:13px;word-break:break-all;font-family:monospace;">{USDT_TRON_ADDRESS}</p>
                <p style="color:rgba(255,255,255,0.4);font-size:11px;margin-top:10px;">{LANG[lang].get('deposit_contract', '📄 CONTRACT ADDRESS')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:10px;border-radius:6px;color:rgba(255,255,255,0.5);font-size:12px;word-break:break-all;font-family:monospace;">{USDT_CONTRACT_ADDRESS}</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px;">
                    <div><p style="color:rgba(255,255,255,0.3);font-size:10px;">{LANG[lang].get('deposit_fee', '💸 FEE')}</p><p style="color:#ffffff;font-size:14px;">{DEPOSIT_FEE}%</p></div>
                    <div><p style="color:rgba(255,255,255,0.3);font-size:10px;">{LANG[lang].get('deposit_time', '⏱️ TIME')}</p><p style="color:#ffffff;font-size:14px;">~1-2 {LANG[lang].get('minutes', 'min') if lang == 'en' else 'min'}</p></div>
                </div>
            </div>
            <h3 style="color:#ffffff;font-size:15px;margin:18px 0 12px;">{LANG[lang].get('deposit_verify', 'Verify your deposit')}</h3>
            <form method="post" action="/deposit">
                <div class="form-group">
                    <input type="number" name="amount" placeholder="{LANG[lang].get('deposit_amount', 'USDT Amount')}" step="0.01" required>
                </div>
                <div class="form-group">
                    <input type="text" name="txid" placeholder="{LANG[lang].get('deposit_txid', 'Transaction ID (txid)')}" required>
                </div>
                <button type="submit" class="btn">{LANG[lang].get('deposit_btn', 'Submit deposit')}</button>
            </form>
            <div class="link" style="margin-top:16px;">
                <a href="/dashboard">{LANG[lang].get('deposit_back', '← Back to Dashboard')}</a>
            </div>
        </div>
    </body>
    </html>
    """

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
        raise HTTPException(status_code=403, detail="Ou dwe achte yon plan anvan ou ka fè retrè")
    plan = active_plan_info["plan"]
    min_withdraw_map = {"Starter": 10, "Standard": 25, "Premium": 50, "VIP": 100}
    max_withdraw_map = {"Starter": 200, "Standard": 500, "Premium": 1000, "VIP": 5000}
    plan_name = plan.name.split()[0]
    min_withdraw = min_withdraw_map.get(plan_name, 10)
    max_withdraw = max_withdraw_map.get(plan_name, 200)
    if amount < min_withdraw:
        raise HTTPException(status_code=400, detail=f"Minimum retrè pou plan {plan_name} se {min_withdraw} USDT")
    if amount > max_withdraw:
        raise HTTPException(status_code=400, detail=f"Maksimòm retrè pou plan {plan_name} se {max_withdraw} USDT")
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Balans pa ase")
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
    lang = get_lang(request)
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
            {get_logo_html(lang, request)}
            <div class="title">{LANG[lang].get('referral_title', '👥 Referral')}</div>
            <div style="background:rgba(255,215,0,0.04);border-radius:10px;padding:16px;border:1px solid rgba(255,215,0,0.06);">
                <p style="color:rgba(255,255,255,0.4);font-size:11px;">{LANG[lang].get('referral_code', 'YOUR REFERRAL CODE')}</p>
                <p style="color:#ffd700;font-size:22px;font-weight:700;font-family:monospace;">{user.referral_code}</p>
            </div>
            <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;margin-top:12px;">
                <p style="color:rgba(255,255,255,0.4);font-size:11px;">{LANG[lang].get('referral_link', 'INVITATION LINK')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px;color:rgba(255,255,255,0.5);font-size:11px;word-break:break-all;">/register?ref={user.referral_code}</p>
            </div>
            <div style="text-align:center;margin-top:16px;">
                <p style="color:rgba(255,255,255,0.4);font-size:13px;">{LANG[lang].get('referral_count', 'People you invited:')} <span style="color:#ffd700;font-weight:700;font-size:18px;">{len(referrals)}</span></p>
            </div>
            <div class="link" style="margin-top:16px;">
                <a href="/dashboard">{LANG[lang].get('referral_back', '← Back to Dashboard')}</a>
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
    lang = get_lang(request)
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
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;margin:6px 0;border:1px solid rgba(255,255,255,0.03);">
            <p style="color:#ffffff;font-size:13px;"><strong>{d.username}</strong> - {d.amount} USDT</p>
            <p style="color:rgba(255,255,255,0.3);font-size:10px;">TXID: {d.txid}</p>
            <p style="color:rgba(255,255,255,0.2);font-size:10px;">{d.date.strftime('%d/%m/%Y %H:%M')}</p>
            <div style="display:flex;gap:6px;margin-top:6px;">
                <form method="post" action="/admin/approve-deposit/{d.id}" style="display:inline;">
                    <button style="background:#4ade80;border:none;padding:6px 14px;border-radius:6px;color:#0a0e27;font-weight:700;cursor:pointer;font-size:12px;">{LANG[lang].get('admin_approve', 'Approve')}</button>
                </form>
                <form method="post" action="/admin/reject-deposit/{d.id}" style="display:inline;">
                    <button style="background:#ff6b6b;border:none;padding:6px 14px;border-radius:6px;color:#ffffff;font-weight:700;cursor:pointer;font-size:12px;">{LANG[lang].get('admin_reject', 'Reject')}</button>
                </form>
            </div>
        </div>
        """
    
    withdraw_html = ""
    for w in pending_withdraws:
        withdraw_html += f"""
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;margin:6px 0;border:1px solid rgba(255,255,255,0.03);">
            <p style="color:#ffffff;font-size:13px;"><strong>{w.username}</strong> - {w.amount} USDT</p>
            <p style="color:rgba(255,255,255,0.3);font-size:10px;">Wallet: {w.wallet}</p>
            <p style="color:rgba(255,255,255,0.2);font-size:10px;">{w.date.strftime('%d/%m/%Y %H:%M')}</p>
            <div style="display:flex;gap:6px;margin-top:6px;">
                <form method="post" action="/admin/approve-withdraw/{w.id}" style="display:inline;">
                    <button style="background:#4ade80;border:none;padding:6px 14px;border-radius:6px;color:#0a0e27;font-weight:700;cursor:pointer;font-size:12px;">{LANG[lang].get('admin_approve', 'Approve')}</button>
                </form>
                <form method="post" action="/admin/reject-withdraw/{w.id}" style="display:inline;">
                    <button style="background:#ff6b6b;border:none;padding:6px 14px;border-radius:6px;color:#ffffff;font-weight:700;cursor:pointer;font-size:12px;">{LANG[lang].get('admin_reject', 'Reject')}</button>
                </form>
            </div>
        </div>
        """
    
    no_pending = LANG[lang].get('admin_no_pending', 'No pending requests')
    return f"""
    <html>
    <head>
        <title>Admin - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:560px;">
            {get_logo_html(lang, request)}
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div>
                    <h1 style="color:#ffffff;font-size:20px;">🛡️ {LANG[lang].get('admin_title', 'Admin')}</h1>
                    <p style="color:rgba(255,255,255,0.3);font-size:11px;">{LANG[lang].get('admin_sub', 'Admin Dashboard')}</p>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:12px;">{LANG[lang].get('admin_back', '← Back')}</a>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:16px;">
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">{LANG[lang].get('admin_users', 'USERS')}</p>
                    <p style="color:#ffffff;font-size:20px;font-weight:700;">{len(users)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">{LANG[lang].get('admin_deposits', 'DEPOSITS')}</p>
                    <p style="color:#4ade80;font-size:20px;font-weight:700;">{len(deposits)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">{LANG[lang].get('admin_withdraws', 'WITHDRAWALS')}</p>
                    <p style="color:#fbbf24;font-size:20px;font-weight:700;">{len(withdraws)}</p>
                </div>
            </div>
            <h3 style="color:#ffd700;font-size:14px;">{LANG[lang].get('admin_pending_deposits', '⏳ Pending deposits')}</h3>
            {deposit_html if deposit_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>{no_pending}</p>"}
            <h3 style="color:#ffd700;font-size:14px;margin-top:12px;">{LANG[lang].get('admin_pending_withdraws', '⏳ Pending withdrawals')}</h3>
            {withdraw_html if withdraw_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>{no_pending}</p>"}
            <div style="margin-top:14px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">
                <p style="color:rgba(255,255,255,0.15);font-size:10px;">{LANG[lang].get('admin_recent', 'Recent activities')}</p>
                <ul style="list-style:none;padding:0;max-height:120px;overflow-y:auto;">
                {''.join([f"<li style='color:rgba(255,255,255,0.2);font-size:10px;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.01);'>{log.date.strftime('%d/%m %H:%M')} - {log.username}: {log.action}</li>" for log in logs[-12:]])}
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
