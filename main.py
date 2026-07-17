from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import os
import uuid
from starlette.middleware.sessions import SessionMiddleware

# =====================
# KONFIGIRASYON APP AVEC LIFESPAN
# =====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    total = db.query(Plan).count()
    if total == 0:
        plans = [
            Plan(name="Starter Basic", price=10, duration=30, daily_return=0.5, description="Plan Starter debaz - 30 jou"),
            Plan(name="Starter Plus", price=25, duration=30, daily_return=0.8, description="Plan Starter Plus - 30 jou"),
            Plan(name="Standard Basic", price=50, duration=60, daily_return=1.0, description="Plan Standard debaz - 60 jou"),
            Plan(name="Standard Plus", price=100, duration=60, daily_return=1.3, description="Plan Standard Plus - 60 jou"),
            Plan(name="Premium Basic", price=200, duration=90, daily_return=1.6, description="Plan Premium debaz - 90 jou"),
            Plan(name="Premium Plus", price=350, duration=90, daily_return=2.0, description="Plan Premium Plus - 90 jou"),
            Plan(name="Premium Pro", price=500, duration=90, daily_return=2.4, description="Plan Premium Pro - 90 jou"),
            Plan(name="VIP Basic", price=750, duration=120, daily_return=2.8, description="Plan VIP debaz - 120 jou"),
            Plan(name="VIP Plus", price=1000, duration=120, daily_return=3.3, description="Plan VIP Plus - 120 jou"),
            Plan(name="VIP Pro", price=2000, duration=120, daily_return=4.0, description="Plan VIP Pro - 120 jou")
        ]
        db.add_all(plans)
        db.commit()
    db.close()
    yield

app = FastAPI(
    title="VestiCore",
    description="Platfòm VestiCore",
    version="3.0",
    lifespan=lifespan
)

# =====================
# SESSION MIDDLEWARE
# =====================

SECRET_KEY = os.getenv("SECRET_KEY", "vesticore-secret-key-change-later")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
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
    deprecated="auto",
    bcrypt__rounds=12
)

# =====================
# VARIYAB ANVIWÒNMAN
# =====================

USDT_TRON_ADDRESS = "TUNtoPGB3sBwbbX81t6ca4fK2exJNFLRiu"
USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
DEPOSIT_FEE = int(os.getenv("DEPOSIT_FEE", "3"))
WITHDRAW_FEE = int(os.getenv("WITHDRAW_FEE", "5"))
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")
REFERRAL_BONUS = 2
REFERRAL_MIN_INVESTORS = 10

# =====================
# STIL CSS AVEC LOGO DIAMANT
# =====================

STYLE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
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
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 24px;
        padding: 40px 35px;
        max-width: 600px;
        width: 100%;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 40px rgba(255,215,0,0.05);
    }
    
    /* ===== LOGO DIAMANT ===== */
    .logo { text-align: center; margin-bottom: 20px; }
    .logo-diamond {
        width: 75px;
        height: 75px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
        box-shadow: 0 0 40px rgba(255,215,0,0.3);
        position: relative;
        transition: transform 0.3s ease;
    }
    .logo-diamond:hover {
        transform: scale(1.05);
    }
    .logo-diamond::after {
        content: '';
        position: absolute;
        top: -6px;
        left: -6px;
        right: -6px;
        bottom: -6px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
        z-index: -1;
        opacity: 0.25;
        filter: blur(15px);
        animation: pulseGlow 2s ease-in-out infinite;
    }
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.25; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
    }
    .logo-diamond span {
        font-size: 34px;
        font-weight: 900;
        color: #0a0e27;
        text-shadow: 0 2px 15px rgba(255,215,0,0.4);
        margin-top: 2px;
        letter-spacing: -1px;
    }
    .logo h1 {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .logo h1 span {
        color: #ffd700;
        text-shadow: 0 0 20px rgba(255,215,0,0.2);
    }
    .logo p {
        color: rgba(255,255,255,0.4);
        font-size: 10px;
        margin-top: 2px;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    .lang-selector {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        margin-bottom: 15px;
    }
    .lang-selector a {
        color: rgba(255,255,255,0.3);
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        transition: all 0.3s;
    }
    .lang-selector a:hover { color: #ffd700; background: rgba(255,215,0,0.1); }
    .lang-selector a.active { color: #ffd700; background: rgba(255,215,0,0.15); }
    
    .title { color: #ffffff; font-size: 22px; font-weight: 600; margin-bottom: 6px; text-align: center; }
    .subtitle { color: rgba(255,255,255,0.4); font-size: 13px; text-align: center; margin-bottom: 22px; }
    
    .form-group { margin-bottom: 16px; }
    .form-group label {
        display: block;
        color: rgba(255,255,255,0.6);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    .form-group input {
        width: 100%;
        padding: 13px 16px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        color: #ffffff;
        font-size: 14px;
        transition: all 0.3s ease;
        outline: none;
    }
    .form-group input:focus {
        border-color: #ffd700;
        background: rgba(255,215,0,0.05);
        box-shadow: 0 0 25px rgba(255,215,0,0.08);
    }
    .form-group input::placeholder { color: rgba(255,255,255,0.2); }
    
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
        box-shadow: 0 10px 30px rgba(255,215,0,0.3);
    }
    .btn-secondary {
        background: rgba(255,255,255,0.06);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .btn-secondary:hover {
        background: rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(255,255,255,0.05);
    }
    .btn-sm {
        padding: 8px 16px;
        font-size: 12px;
        width: auto;
        display: inline-block;
        margin: 0;
    }
    .btn-danger {
        background: linear-gradient(135deg, #ff6b6b, #ee4444);
        color: #fff;
    }
    .btn-danger:hover {
        box-shadow: 0 10px 30px rgba(255,107,107,0.3);
    }
    .btn-success {
        background: linear-gradient(135deg, #4ade80, #22c55e);
        color: #0a0e27;
    }
    .btn-success:hover {
        box-shadow: 0 10px 30px rgba(74,222,128,0.3);
    }
    
    .link {
        text-align: center;
        margin-top: 18px;
        color: rgba(255,255,255,0.35);
        font-size: 13px;
    }
    .link a { color: #ffd700; text-decoration: none; font-weight: 600; transition: color 0.3s; }
    .link a:hover { color: #f0a500; text-decoration: underline; }
    
    .footer-text {
        text-align: center;
        margin-top: 20px;
        color: rgba(255,255,255,0.15);
        font-size: 11px;
        letter-spacing: 1px;
    }
    
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .dashboard-user h2 {
        color: #ffffff;
        font-size: 18px;
    }
    .dashboard-user p {
        color: rgba(255,255,255,0.3);
        font-size: 11px;
    }
    
    .balance-card {
        background: rgba(255,215,0,0.04);
        border-radius: 14px;
        padding: 18px;
        border: 1px solid rgba(255,215,0,0.08);
        margin-bottom: 15px;
        text-align: center;
    }
    .balance-card .label {
        color: rgba(255,255,255,0.4);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .balance-card .amount {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        margin: 5px 0;
    }
    .balance-card .amount span {
        color: #ffd700;
        font-size: 18px;
    }
    
    .quick-actions {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        margin-bottom: 15px;
    }
    .quick-actions a {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 12px 8px;
        text-align: center;
        color: #ffffff;
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
        transition: all 0.3s;
        cursor: pointer;
    }
    .quick-actions a:hover {
        background: rgba(255,215,0,0.05);
        border-color: rgba(255,215,0,0.15);
    }
    .quick-actions a .icon {
        display: block;
        font-size: 20px;
        margin-bottom: 4px;
    }
    
    .plan-card {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 14px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .plan-card .plan-info h4 {
        color: #ffd700;
        font-size: 14px;
    }
    .plan-card .plan-info p {
        color: rgba(255,255,255,0.4);
        font-size: 11px;
        margin: 2px 0;
    }
    .plan-card .plan-info .return {
        color: #4ade80;
        font-weight: 600;
    }
    .plan-card .plan-price {
        color: #ffffff;
        font-size: 16px;
        font-weight: 700;
        text-align: right;
    }
    .plan-card .plan-price small {
        color: rgba(255,255,255,0.3);
        font-size: 10px;
        font-weight: 400;
    }
    
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 600;
    }
    .badge-gold { background: rgba(255,215,0,0.15); color: #ffd700; }
    .badge-green { background: rgba(74,222,128,0.15); color: #4ade80; }
    .badge-red { background: rgba(255,107,107,0.15); color: #ff6b6b; }
    
    /* ===== MODAL ===== */
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        backdrop-filter: blur(10px);
        z-index: 1000;
        justify-content: center;
        align-items: center;
    }
    .modal.active {
        display: flex;
    }
    .modal-content {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 20px;
        padding: 30px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
    }
    .modal-content h3 {
        color: #ffffff;
        font-size: 20px;
        margin-bottom: 10px;
    }
    .modal-content p {
        color: rgba(255,255,255,0.6);
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .modal-content .btn {
        width: auto;
        display: inline-block;
        padding: 10px 30px;
    }
    .modal-content .icon-big {
        font-size: 48px;
        margin-bottom: 15px;
        display: block;
    }
    
    .history-item {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    .history-item .left {
        color: rgba(255,255,255,0.5);
        font-size: 11px;
    }
    .history-item .right {
        font-size: 11px;
        font-weight: 600;
    }
    .history-item .right.positive { color: #4ade80; }
    .history-item .right.negative { color: #ff6b6b; }
    
    .withdraw-section {
        margin-top: 15px;
        padding: 15px;
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .withdraw-section h4 {
        color: #ffffff;
        font-size: 14px;
        margin-bottom: 10px;
    }
    
    @media (max-width: 480px) {
        .container { padding: 20px 15px; }
        .logo h1 { font-size: 22px; }
        .logo-diamond { width: 55px; height: 55px; }
        .logo-diamond span { font-size: 26px; }
        .quick-actions { grid-template-columns: 1fr 1fr 1fr; }
        .plan-card { flex-direction: column; text-align: center; }
        .plan-card .plan-price { text-align: center; margin-top: 8px; }
    }
</style>
"""

# =====================
# JAVASCRIPT POU MODAL + ACHTE PLAN
# =====================

MODAL_JS = """
<script>
function showModal(message, title, type) {
    const modal = document.getElementById('customModal');
    const icon = document.getElementById('modalIcon');
    const titleEl = document.getElementById('modalTitle');
    const msgEl = document.getElementById('modalMessage');
    
    if (type === 'error') {
        icon.textContent = '❌';
        titleEl.textContent = title || 'Erreur';
    } else if (type === 'success') {
        icon.textContent = '✅';
        titleEl.textContent = title || 'Succès';
    } else {
        icon.textContent = 'ℹ️';
        titleEl.textContent = title || 'Information';
    }
    
    msgEl.textContent = message;
    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('customModal').classList.remove('active');
}

function acheterPlan(planId) {
    fetch('/buy-plan/' + planId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showModal(data.message, '✅ Succès', 'success');
            setTimeout(() => location.reload(), 2000);
        } else {
            showModal(data.message, '❌ Erreur', 'error');
        }
    })
    .catch(err => {
        showModal('Erreur de connexion au serveur', '❌ Erreur', 'error');
    });
}

function faireRetrait() {
    const amount = document.getElementById('withdrawAmount').value;
    const wallet = document.getElementById('withdrawWallet').value;
    
    if (!amount || amount <= 0) {
        showModal('Veuillez entrer un montant valide.', '❌ Erreur', 'error');
        return;
    }
    if (!wallet || wallet.length < 10) {
        showModal('Veuillez entrer une adresse TRC20 valide.', '❌ Erreur', 'error');
        return;
    }
    
    fetch('/withdraw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'amount=' + amount + '&wallet=' + encodeURIComponent(wallet)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showModal(data.message, '✅ Succès', 'success');
            setTimeout(() => location.reload(), 2000);
        } else {
            showModal(data.message, '❌ Erreur', 'error');
        }
    })
    .catch(err => {
        showModal('Erreur de connexion au serveur', '❌ Erreur', 'error');
    });
}
</script>
"""

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
        "dashboard_balance_label": "Solde disponible",
        "dashboard_deposit": "Dépôt",
        "dashboard_withdraw": "Retrait",
        "dashboard_referral": "Parrainage",
        "dashboard_history": "Historique",
        "dashboard_profile": "Profil",
        "dashboard_logout": "Déconnexion",
        "dashboard_plans": "Plans d'investissement",
        "dashboard_buy": "Acheter",
        "dashboard_no_plan": "⚠️ Vous n'avez pas de plan actif.",
        "dashboard_plan_active": "✅ Plan actif",
        "deposit_title": "💰 Dépôt USDT",
        "deposit_warning": "⚠️ Envoyer UNIQUEMENT USDT sur TRC20 (Tron)",
        "deposit_network": "🌐 RÉSEAU",
        "deposit_address": "🏦 ADRESSE",
        "deposit_contract": "📄 CONTRAT",
        "deposit_fee": "💸 FRAIS",
        "deposit_time": "⏱️ TEMPS",
        "deposit_verify": "Vérifier votre dépôt",
        "deposit_amount": "Montant USDT",
        "deposit_txid": "ID de transaction (txid)",
        "deposit_btn": "Envoyer le dépôt",
        "deposit_back": "← Retour",
        "referral_title": "👥 Parrainage",
        "referral_code": "VOTRE CODE",
        "referral_link": "LIEN D'INVITATION",
        "referral_count": "Personnes invitées",
        "referral_investors": "Investisseurs qualifiés",
        "referral_needed": "Encore {needed} investisseurs pour 2%",
        "referral_bonus": "Bonus reçu",
        "referral_back": "← Retour",
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
        "insufficient_balance": "❌ Solde insuffisant. Veuillez effectuer un dépôt.",
        "plan_bought": "✅ Plan acheté avec succès!",
        "already_has_plan": "❌ Vous avez déjà un plan actif.",
        "plan_not_found": "❌ Plan introuvable.",
        "withdraw_success": "✅ Demande de retrait envoyée avec succès!",
        "withdraw_error": "❌ Erreur lors de la demande de retrait.",
        "no_active_plan": "❌ Vous devez avoir un plan actif pour faire un retrait.",
        "insufficient_balance_withdraw": "❌ Solde insuffisant pour ce retrait."
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
        "dashboard_balance_label": "Available balance",
        "dashboard_deposit": "Deposit",
        "dashboard_withdraw": "Withdraw",
        "dashboard_referral": "Referral",
        "dashboard_history": "History",
        "dashboard_profile": "Profile",
        "dashboard_logout": "Logout",
        "dashboard_plans": "Investment Plans",
        "dashboard_buy": "Buy",
        "dashboard_no_plan": "⚠️ You don't have an active plan.",
        "dashboard_plan_active": "✅ Active plan",
        "deposit_title": "💰 USDT Deposit",
        "deposit_warning": "⚠️ Send ONLY USDT on TRC20 (Tron)",
        "deposit_network": "🌐 NETWORK",
        "deposit_address": "🏦 ADDRESS",
        "deposit_contract": "📄 CONTRACT",
        "deposit_fee": "💸 FEE",
        "deposit_time": "⏱️ TIME",
        "deposit_verify": "Verify your deposit",
        "deposit_amount": "USDT Amount",
        "deposit_txid": "Transaction ID (txid)",
        "deposit_btn": "Submit deposit",
        "deposit_back": "← Back",
        "referral_title": "👥 Referral",
        "referral_code": "YOUR CODE",
        "referral_link": "INVITATION LINK",
        "referral_count": "People invited",
        "referral_investors": "Qualified investors",
        "referral_needed": "{needed} more investors for 2%",
        "referral_bonus": "Bonus received",
        "referral_back": "← Back",
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
        "insufficient_balance": "❌ Insufficient balance. Please make a deposit.",
        "plan_bought": "✅ Plan purchased successfully!",
        "already_has_plan": "❌ You already have an active plan.",
        "plan_not_found": "❌ Plan not found.",
        "withdraw_success": "✅ Withdrawal request sent successfully!",
        "withdraw_error": "❌ Error processing withdrawal request.",
        "no_active_plan": "❌ You must have an active plan to withdraw.",
        "insufficient_balance_withdraw": "❌ Insufficient balance for this withdrawal."
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
        "dashboard_balance_label": "Saldo disponible",
        "dashboard_deposit": "Depósito",
        "dashboard_withdraw": "Retiro",
        "dashboard_referral": "Referidos",
        "dashboard_history": "Historial",
        "dashboard_profile": "Perfil",
        "dashboard_logout": "Cerrar sesión",
        "dashboard_plans": "Planes de inversión",
        "dashboard_buy": "Comprar",
        "dashboard_no_plan": "⚠️ No tienes un plan activo.",
        "dashboard_plan_active": "✅ Plan activo",
        "deposit_title": "💰 Depósito USDT",
        "deposit_warning": "⚠️ Enviar SOLAMENTE USDT en TRC20 (Tron)",
        "deposit_network": "🌐 RED",
        "deposit_address": "🏦 DIRECCIÓN",
        "deposit_contract": "📄 CONTRATO",
        "deposit_fee": "💸 COMISIÓN",
        "deposit_time": "⏱️ TIEMPO",
        "deposit_verify": "Verifica tu depósito",
        "deposit_amount": "Monto USDT",
        "deposit_txid": "ID de transacción (txid)",
        "deposit_btn": "Enviar depósito",
        "deposit_back": "← Volver",
        "referral_title": "👥 Referidos",
        "referral_code": "TU CÓDIGO",
        "referral_link": "ENLACE DE INVITACIÓN",
        "referral_count": "Personas invitadas",
        "referral_investors": "Inversores calificados",
        "referral_needed": "Se necesitan {needed} inversores para 2%",
        "referral_bonus": "Bonificación recibida",
        "referral_back": "← Volver",
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
        "insufficient_balance": "❌ Saldo insuficiente. Por favor, haz un depósito.",
        "plan_bought": "✅ Plan comprado con éxito!",
        "already_has_plan": "❌ Ya tienes un plan activo.",
        "plan_not_found": "❌ Plan no encontrado.",
        "withdraw_success": "✅ Solicitud de retiro enviada con éxito!",
        "withdraw_error": "❌ Error al procesar la solicitud de retiro.",
        "no_active_plan": "❌ Debes tener un plan activo para retirar.",
        "insufficient_balance_withdraw": "❌ Saldo insuficiente para este retiro."
    }
}

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
    referral_bonus = Column(Float, default=0)
    referral_qualified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float, default=0)
    duration = Column(Integer)
    daily_return = Column(Float, default=0)
    description = Column(String)

class UserPlan(Base):
    __tablename__ = "user_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    plan_id = Column(Integer)
    amount = Column(Float)
    status = Column(String, default="active")
    start_date = Column(DateTime, default=datetime.now)
    last_return_date = Column(DateTime, default=datetime.now)
    total_returned = Column(Float, default=0)

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    fee = Column(Float, default=0)
    net_amount = Column(Float, default=0)
    txid = Column(String, unique=True)
    status = Column(String, default="pending")
    date = Column(DateTime, default=datetime.now)

class Withdraw(Base):
    __tablename__ = "withdraws"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    fee = Column(Float, default=0)
    net_amount = Column(Float, default=0)
    wallet = Column(String)
    status = Column(String, default="pending")
    date = Column(DateTime, default=datetime.now)

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    referrer = Column(String)
    invited_user = Column(String)
    has_invested = Column(Boolean, default=False)
    bonus_amount = Column(Float, default=0)
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
    return code + str(uuid.uuid4())[:5]

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
# PAYE BENEFIS PLAN
# =====================

def process_plan_returns(db: Session):
    user_plans = db.query(UserPlan).filter(UserPlan.status == "active").all()
    
    for up in user_plans:
        plan = db.query(Plan).filter(Plan.id == up.plan_id).first()
        if not plan:
            continue
        
        expiration_date = up.start_date + timedelta(days=plan.duration)
        if datetime.now() > expiration_date:
            up.status = "expired"
            db.commit()
            continue
        
        days_passed = (datetime.now() - up.last_return_date).days
        
        if days_passed >= 1:
            daily_profit = up.amount * (plan.daily_return / 100)
            max_return = up.amount * (plan.daily_return / 100) * plan.duration
            remaining = max_return - up.total_returned
            
            if remaining <= 0:
                up.status = "completed"
                db.commit()
                continue
            
            to_pay = min(daily_profit * days_passed, remaining)
            
            user = db.query(User).filter(User.id == up.user_id).first()
            if user:
                user.balance += to_pay
                up.total_returned += to_pay
                up.last_return_date = datetime.now()
                add_log(db, user.username, f"Benefis plan {plan.name}: {to_pay:.2f} USDT")
    
    db.commit()

# =====================
# FUNCTIONS
# =====================

def get_lang(request: Request):
    lang = request.cookies.get("lang", "fr")
    if lang not in LANG:
        lang = "fr"
    return lang

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
        <div class="logo-diamond">
            <span>V</span>
        </div>
        <h1>Vesti<span>Core</span></h1>
        <p>{LANG[lang_key].get('logo_sub', 'INVEST • GROW • PROSPER')}</p>
    </div>
    """

# =====================
# MODAL HTML
# =====================

def get_modal_html():
    return f"""
    <div id="customModal" class="modal">
        <div class="modal-content">
            <span class="icon-big" id="modalIcon">ℹ️</span>
            <h3 id="modalTitle">Information</h3>
            <p id="modalMessage">Message</p>
            <button onclick="closeModal()" class="btn">Fermer</button>
        </div>
    </div>
    {MODAL_JS}
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
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# REGISTER PAGE
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, ref: str = None):
    lang = get_lang(request)
    ref_value = f'value="{ref}"' if ref else ''
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
                    <input type="text" name="ref" placeholder="{LANG[lang].get('register_ref', 'Referral code (optional)')}" {ref_value}>
                </div>
                <button type="submit" class="btn">{LANG[lang].get('register_btn', 'Create account')}</button>
            </form>
            <div class="link">
                {LANG[lang].get('register_link', 'Already have an account?')} <a href="/login">{LANG[lang].get('register_link_btn', 'Login')}</a>
            </div>
        </div>
        {get_modal_html()}
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
    
    is_admin = 0
    if ADMIN_SECRET_KEY and ref and ref.strip() == ADMIN_SECRET_KEY.strip():
        is_admin = 1
        ref = None
    
    new_user = User(
        username=username,
        password=hash_password(password),
        referral_code=create_referral_code(username),
        referred_by=ref,
        is_admin=is_admin
    )
    db.add(new_user)
    db.flush()
    
    if ref:
        referrer = db.query(User).filter(User.referral_code == ref).first()
        if referrer:
            referral = Referral(
                referrer=referrer.username,
                invited_user=username,
                has_invested=False,
                bonus_amount=0,
                status="pending"
            )
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
        {get_modal_html()}
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
    process_plan_returns(db)
    
    lang = get_lang(request)
    user = current_user(request, db)
    plans = db.query(Plan).all()
    active_plan_info = get_user_active_plan(db, user.id)
    
    referrals = db.query(Referral).filter(Referral.referrer == user.username).all()
    qualified_investors = sum(1 for r in referrals if r.has_invested)
    total_bonus = sum(r.bonus_amount for r in referrals)
    
    # History
    logs = db.query(ActivityLog).filter(ActivityLog.username == user.username).order_by(ActivityLog.date.desc()).limit(10).all()
    
    plan_html = ""
    for plan in plans:
        plan_html += f"""
        <div class="plan-card">
            <div class="plan-info">
                <h4>{plan.name}</h4>
                <p>{plan.description}</p>
                <p>⏳ {plan.duration} jours • <span class="return">📈 {plan.daily_return}% / jour</span></p>
            </div>
            <div class="plan-price">
                {plan.price} <small>USDT</small>
                <br>
                <button onclick="acheterPlan({plan.id})" class="btn btn-sm" style="margin-top:4px;">{LANG[lang].get('dashboard_buy', 'Buy')}</button>
            </div>
        </div>
        """
    
    plan_info_html = ""
    if active_plan_info:
        plan = active_plan_info["plan"]
        exp_date = active_plan_info["expiration_date"]
        plan_info_html = f"""
        <div style="background:rgba(74,222,128,0.05);border:1px solid rgba(74,222,128,0.15);border-radius:10px;padding:12px;margin-bottom:12px;text-align:center;">
            <span class="badge badge-green">✅ {LANG[lang].get('dashboard_plan_active', 'Active plan')}</span>
            <p style="color:#ffffff;font-size:14px;margin-top:6px;">{plan.name}</p>
            <p style="color:rgba(255,255,255,0.3);font-size:11px;">Expire: {exp_date.strftime('%d/%m/%Y')}</p>
        </div>
        """
    else:
        plan_info_html = f"""
        <div style="background:rgba(255,150,0,0.05);border:1px solid rgba(255,150,0,0.12);border-radius:10px;padding:12px;margin-bottom:12px;text-align:center;">
            <p style="color:#fbbf24;font-size:12px;">{LANG[lang].get('dashboard_no_plan', '⚠️ You don\'t have an active plan.')}</p>
        </div>
        """
    
    history_html = ""
    for log in logs[:5]:
        if "Benefis" in log.action:
            history_html += f"""
            <div class="history-item">
                <span class="left">{log.date.strftime('%d/%m %H:%M')} - {log.action[:30]}...</span>
                <span class="right positive">+{log.action.split(':')[-1].strip() if ':' in log.action else ''}</span>
            </div>
            """
        elif "Depo" in log.action or "retrè" in log.action:
            history_html += f"""
            <div class="history-item">
                <span class="left">{log.date.strftime('%d/%m %H:%M')} - {log.action[:30]}...</span>
                <span class="right">💰</span>
            </div>
            """
    
    admin_link = f'<a href="/admin" style="color:rgba(255,255,255,0.15);text-decoration:none;font-size:10px;">Admin</a>' if user.is_admin == 1 else ''
    
    return f"""
    <html>
    <head>
        <title>Dashboard - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:600px;">
            {get_logo_html(lang, request)}
            
            <div class="dashboard-header">
                <div class="dashboard-user">
                    <h2>👋 {user.username}</h2>
                    <p>{LANG[lang].get('dashboard_balance_label', 'Available balance')}</p>
                </div>
                <div>
                    <a href="/logout" class="btn btn-sm btn-danger">{LANG[lang].get('dashboard_logout', 'Logout')}</a>
                </div>
            </div>
            
            <div class="balance-card">
                <div class="label">{LANG[lang].get('dashboard_balance', 'BALANCE')}</div>
                <div class="amount">{user.balance:.2f} <span>USDT</span></div>
            </div>
            
            {plan_info_html}
            
            <div class="quick-actions">
                <a href="/deposit-page">
                    <span class="icon">💰</span>
                    {LANG[lang].get('dashboard_deposit', 'Deposit')}
                </a>
                <a href="#" onclick="document.getElementById('withdrawSection').scrollIntoView(); return false;">
                    <span class="icon">📤</span>
                    {LANG[lang].get('dashboard_withdraw', 'Withdraw')}
                </a>
                <a href="/referral">
                    <span class="icon">🎁</span>
                    {LANG[lang].get('dashboard_referral', 'Referral')}
                </a>
            </div>
            
            <div id="withdrawSection" class="withdraw-section">
                <h4>📤 {LANG[lang].get('dashboard_withdraw', 'Withdraw')}</h4>
                <div class="form-group">
                    <input type="number" id="withdrawAmount" placeholder="{LANG[lang].get('dashboard_withdraw_placeholder', 'USDT Amount')}" step="0.01" min="1">
                </div>
                <div class="form-group">
                    <input type="text" id="withdrawWallet" placeholder="{LANG[lang].get('dashboard_withdraw_wallet', 'Your TRC20 address')}">
                </div>
                <button onclick="faireRetrait()" class="btn btn-secondary" style="margin-top:0;">{LANG[lang].get('dashboard_withdraw_btn', 'Submit request')}</button>
                <p style="color:rgba(255,255,255,0.2);font-size:10px;text-align:center;margin-top:6px;">{LANG[lang].get('dashboard_withdraw_warning', '⚠️ Withdrawals are subject to admin approval')}</p>
            </div>
            
            <h4 style="color:#ffffff;font-size:14px;margin:15px 0 10px;">{LANG[lang].get('dashboard_plans', 'Investment Plans')}</h4>
            {plan_html}
            
            {f'<div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">{admin_link}</div>' if user.is_admin == 1 else ''}
            
            <div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">
                <p style="color:rgba(255,255,255,0.15);font-size:9px;">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</p>
            </div>
        </div>
        
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# BUY PLAN - AVEC JSON RESPONSE
# =====================

@app.post("/buy-plan/{plan_id}")
def buy_plan(
    plan_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Ou dwe konekte"}
        )
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Itilizatè pa jwenn"}
        )
    
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": LANG[get_lang(request)].get('plan_not_found', 'Plan not found')}
        )
    
    existing = db.query(UserPlan).filter(
        UserPlan.user_id == user.id,
        UserPlan.status == "active"
    ).first()
    if existing:
        return JSONResponse(
            content={"success": False, "message": LANG[get_lang(request)].get('already_has_plan', 'You already have an active plan')}
        )
    
    if user.balance < plan.price:
        return JSONResponse(
            content={"success": False, "message": LANG[get_lang(request)].get('insufficient_balance', 'Insufficient balance')}
        )
    
    user.balance -= plan.price
    
    user_plan = UserPlan(
        user_id=user.id,
        plan_id=plan.id,
        amount=plan.price,
        status="active",
        start_date=datetime.now(),
        last_return_date=datetime.now(),
        total_returned=0
    )
    db.add(user_plan)
    add_log(db, user.username, f"Achte plan {plan.name} pou {plan.price} USDT")
    db.commit()
    
    return JSONResponse(
        content={"success": True, "message": LANG[get_lang(request)].get('plan_bought', 'Plan purchased successfully!')}
    )

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
            
            <div style="background:rgba(255,0,0,0.06);border:1px solid rgba(255,0,0,0.12);border-radius:10px;padding:12px;margin-bottom:15px;">
                <p style="color:#ff6b6b;font-weight:600;font-size:12px;text-align:center;">{LANG[lang].get('deposit_warning', '⚠️ Send ONLY USDT on TRC20 (Tron)')}</p>
            </div>
            
            <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:15px;border:1px solid rgba(255,255,255,0.04);margin-bottom:15px;">
                <p style="color:rgba(255,255,255,0.4);font-size:10px;">{LANG[lang].get('deposit_network', '🌐 NETWORK')}</p>
                <p style="color:#4ade80;font-weight:700;font-size:15px;">TRC20 (Tron)</p>
                
                <p style="color:rgba(255,255,255,0.4);font-size:10px;margin-top:8px;">{LANG[lang].get('deposit_address', '🏦 ADDRESS')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:10px;border-radius:6px;color:#ffd700;font-size:12px;word-break:break-all;font-family:monospace;">{USDT_TRON_ADDRESS}</p>
                
                <p style="color:rgba(255,255,255,0.4);font-size:10px;margin-top:8px;">{LANG[lang].get('deposit_contract', '📄 CONTRACT')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px;color:rgba(255,255,255,0.4);font-size:11px;word-break:break-all;font-family:monospace;">{USDT_CONTRACT_ADDRESS}</p>
                
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px;">
                    <div><p style="color:rgba(255,255,255,0.3);font-size:9px;">{LANG[lang].get('deposit_fee', '💸 FEE')}</p><p style="color:#ffffff;font-size:14px;">{DEPOSIT_FEE}%</p></div>
                    <div><p style="color:rgba(255,255,255,0.3);font-size:9px;">{LANG[lang].get('deposit_time', '⏱️ TIME')}</p><p style="color:#ffffff;font-size:14px;">~1-2 min</p></div>
                </div>
            </div>
            
            <h3 style="color:#ffffff;font-size:14px;margin-bottom:10px;">{LANG[lang].get('deposit_verify', 'Verify your deposit')}</h3>
            <form method="post" action="/deposit">
                <div class="form-group">
                    <input type="number" name="amount" placeholder="{LANG[lang].get('deposit_amount', 'USDT Amount')}" step="0.01" required>
                </div>
                <div class="form-group">
                    <input type="text" name="txid" placeholder="{LANG[lang].get('deposit_txid', 'Transaction ID (txid)')}" required>
                </div>
                <button type="submit" class="btn">{LANG[lang].get('deposit_btn', 'Submit deposit')}</button>
            </form>
            
            <div class="link" style="margin-top:15px;">
                <a href="/dashboard">{LANG[lang].get('deposit_back', '← Back')}</a>
            </div>
        </div>
        {get_modal_html()}
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
    
    existing = db.query(Deposit).filter(Deposit.txid == txid).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID tranzaksyon sa deja itilize")
    
    fee = amount * DEPOSIT_FEE / 100
    net_amount = amount - fee
    
    deposit = Deposit(
        username=user.username,
        amount=amount,
        fee=fee,
        net_amount=net_amount,
        txid=txid,
        status="pending"
    )
    db.add(deposit)
    add_log(db, user.username, f"Depo {amount} USDT voye (frè: {fee} USDT)")
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

# =====================
# WITHDRAW - AVEC JSON RESPONSE
# =====================

@app.post("/withdraw")
def withdraw(
    request: Request,
    amount: float = Form(...),
    wallet: str = Form(...),
    db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Ou dwe konekte"}
        )
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Itilizatè pa jwenn"}
        )
    
    active_plan_info = get_user_active_plan(db, user.id)
    if not active_plan_info:
        return JSONResponse(
            content={"success": False, "message": LANG[get_lang(request)].get('no_active_plan', 'You must have an active plan to withdraw')}
        )
    
    if amount <= 0:
        return JSONResponse(
            content={"success": False, "message": "Montan pa valab"}
        )
    
    if user.balance < amount:
        return JSONResponse(
            content={"success": False, "message": LANG[get_lang(request)].get('insufficient_balance_withdraw', 'Insufficient balance for this withdrawal')}
        )
    
    fee = amount * WITHDRAW_FEE / 100
    net_amount = amount - fee
    
    user.balance -= amount
    
    withdraw = Withdraw(
        username=user.username,
        amount=amount,
        fee=fee,
        net_amount=net_amount,
        wallet=wallet,
        status="pending"
    )
    db.add(withdraw)
    add_log(db, user.username, f"Demann retrè {amount} USDT voye")
    db.commit()
    
    return JSONResponse(
        content={"success": True, "message": LANG[get_lang(request)].get('withdraw_success', 'Withdrawal request sent successfully!')}
    )

# =====================
# REFERRAL
# =====================

@app.get("/referral", response_class=HTMLResponse)
def referral_page(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request)
    user = current_user(request, db)
    referrals = db.query(Referral).filter(Referral.referrer == user.username).all()
    
    qualified_investors = sum(1 for r in referrals if r.has_invested)
    total_bonus = sum(r.bonus_amount for r in referrals)
    needed = max(0, REFERRAL_MIN_INVESTORS - qualified_investors)
    
    status_text = LANG[lang].get('referral_needed', '{needed} more investors for 2%').format(needed=needed)
    if qualified_investors >= REFERRAL_MIN_INVESTORS:
        status_text = "✅ Bonus 2% débloqué!"
    
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
            
            <div style="background:rgba(255,215,0,0.04);border-radius:10px;padding:15px;border:1px solid rgba(255,215,0,0.06);">
                <p style="color:rgba(255,255,255,0.4);font-size:10px;">{LANG[lang].get('referral_code', 'YOUR CODE')}</p>
                <p style="color:#ffd700;font-size:22px;font-weight:700;font-family:monospace;">{user.referral_code}</p>
            </div>
            
            <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;margin-top:12px;">
                <p style="color:rgba(255,255,255,0.4);font-size:10px;">{LANG[lang].get('referral_link', 'INVITATION LINK')}</p>
                <p style="background:rgba(0,0,0,0.3);padding:8px;border-radius:6px;color:rgba(255,255,255,0.5);font-size:11px;word-break:break-all;">
                    <a href="/register?ref={user.referral_code}" style="color:#ffd700;">/register?ref={user.referral_code}</a>
                </p>
            </div>
            
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;">
                <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.4);font-size:10px;">{LANG[lang].get('referral_count', 'People invited')}</p>
                    <p style="color:#ffffff;font-size:22px;font-weight:700;">{len(referrals)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.4);font-size:10px;">{LANG[lang].get('referral_investors', 'Qualified investors')}</p>
                    <p style="color:#4ade80;font-size:22px;font-weight:700;">{qualified_investors}/{REFERRAL_MIN_INVESTORS}</p>
                </div>
            </div>
            
            <div style="background:rgba(255,215,0,0.04);border-radius:8px;padding:12px;margin-top:12px;text-align:center;border:1px solid rgba(255,215,0,0.1);">
                <p style="color:rgba(255,255,255,0.6);font-size:12px;">{status_text}</p>
                <p style="color:rgba(255,255,255,0.4);font-size:11px;margin-top:4px;">{LANG[lang].get('referral_bonus', 'Bonus received')}: <span style="color:#ffd700;font-weight:700;">{total_bonus:.2f} USDT</span></p>
            </div>
            
            <div class="link" style="margin-top:15px;">
                <a href="/dashboard">{LANG[lang].get('referral_back', '← Back')}</a>
            </div>
        </div>
        {get_modal_html()}
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
    pending_deposits = db.query(Deposit).filter(Deposit.status == "pending").all()
    pending_withdraws = db.query(Withdraw).filter(Withdraw.status == "pending").all()
    
    deposit_html = ""
    for d in pending_deposits:
        deposit_html += f"""
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;margin:6px 0;border:1px solid rgba(255,255,255,0.03);">
            <p style="color:#ffffff;font-size:13px;"><strong>{d.username}</strong> - {d.amount} USDT</p>
            <p style="color:rgba(255,255,255,0.3);font-size:10px;">TXID: {d.txid}</p>
            <p style="color:rgba(255,255,255,0.2);font-size:10px;">Frè: {d.fee} USDT | Net: {d.net_amount} USDT</p>
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
            <p style="color:rgba(255,255,255,0.3);font-size:10px;">Frè: {w.fee} USDT | Net: {w.net_amount} USDT</p>
            <p style="color:rgba(255,255,255,0.3);font-size:10px;">Wallet: {w.wallet}</p>
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
            
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:15px;">
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
        {get_modal_html()}
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
        user.balance += deposit.net_amount
        add_log(db, user.username, f"Depo {deposit.amount} USDT apwouve (net: {deposit.net_amount} USDT)")
        
        if user.referred_by:
            referral = db.query(Referral).filter(
                Referral.invited_user == user.username
            ).first()
            if referral:
                referral.has_invested = True
                
                referrer = db.query(User).filter(User.username == referral.referrer).first()
                if referrer:
                    qualified = db.query(Referral).filter(
                        Referral.referrer == referrer.username,
                        Referral.has_invested == True
                    ).count()
                    
                    if qualified >= REFERRAL_MIN_INVESTORS and not referrer.referral_qualified:
                        referrer.referral_qualified = True
                        
                        invited_users = db.query(Referral).filter(
                            Referral.referrer == referrer.username,
                            Referral.has_invested == True
                        ).all()
                        
                        total_invested = 0
                        for inv in invited_users:
                            user_deposits = db.query(Deposit).filter(
                                Deposit.username == inv.invited_user,
                                Deposit.status == "approved"
                            ).all()
                            total_invested += sum(d.net_amount for d in user_deposits)
                        
                        bonus = total_invested * REFERRAL_BONUS / 100
                        referrer.balance += bonus
                        referrer.referral_bonus += bonus
                        
                        for inv in invited_users:
                            ref = db.query(Referral).filter(
                                Referral.invited_user == inv.invited_user
                            ).first()
                            if ref:
                                ref.bonus_amount = bonus / len(invited_users)
                                ref.status = "completed"
                        
                        add_log(db, referrer.username, f"Bonus referral {bonus:.2f} USDT - 10 investisseurs")
    
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
    add_log(db, withdraw.username, f"Retrè {withdraw.amount} USDT apwouve (net: {withdraw.net_amount} USDT)")
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
    user = db.query(User).filter(User.username == withdraw.username).first()
    if user:
        user.balance += withdraw.amount
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
# RUN
# =====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
