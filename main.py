from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import os
import uuid
import json
import base64
from starlette.middleware.sessions import SessionMiddleware

# =====================
# SEKIRITE - SECRET_KEY OBLIGATWA
# =====================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY pa defini! Mete l nan Railway Variables.")

# =====================
# KONFIGIRASYON APP AVEC LIFESPAN
# =====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    total = db.query(Plan).count()
    if total == 0:
        plans = [
            Plan(name="Starter Basic", price=10, duration=30, daily_return=0.90, description="Plan Starter debaz - 30 jou"),
            Plan(name="Starter Plus", price=25, duration=30, daily_return=1.00, description="Plan Starter Plus - 30 jou"),
            Plan(name="Standard Basic", price=50, duration=60, daily_return=1.10, description="Plan Standard debaz - 60 jou"),
            Plan(name="Standard Plus", price=100, duration=60, daily_return=1.20, description="Plan Standard Plus - 60 jou"),
            Plan(name="Premium Basic", price=200, duration=90, daily_return=1.30, description="Plan Premium debaz - 90 jou"),
            Plan(name="Premium Plus", price=350, duration=90, daily_return=1.40, description="Plan Premium Plus - 90 jou"),
            Plan(name="Premium Pro", price=500, duration=90, daily_return=1.50, description="Plan Premium Pro - 90 jou"),
            Plan(name="VIP Basic", price=750, duration=120, daily_return=1.60, description="Plan VIP debaz - 120 jou"),
            Plan(name="VIP Plus", price=1000, duration=120, daily_return=1.70, description="Plan VIP Plus - 120 jou"),
            Plan(name="VIP Pro", price=2000, duration=120, daily_return=1.90, description="Plan VIP Pro - 120 jou")
        ]
        db.add_all(plans)
        db.commit()
    db.close()
    yield

app = FastAPI(
    title="VestiCore",
    description="Platfòm VestiCore - Finans Dijital & Rewards Platform",
    version="3.0",
    lifespan=lifespan
)

# =====================
# SESSION MIDDLEWARE
# =====================

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
# STIL CSS
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
        align-items: flex-start;
        padding: 20px;
    }
    .container {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,215,0,0.08);
        border-radius: 24px;
        padding: 25px 30px;
        max-width: 1100px;
        width: 100%;
        box-shadow: 0 25px 60px rgba(0,0,0,0.4);
        margin-top: 10px;
    }
    .logo { text-align: center; margin-bottom: 15px; }
    .logo-diamond {
        display: inline-block;
        width: 70px;
        height: 70px;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 30px rgba(255,215,0,0.3));
        animation: floatGlow 3s ease-in-out infinite;
    }
    .logo-diamond svg { width: 100%; height: 100%; }
    @keyframes floatGlow {
        0%, 100% { transform: translateY(0px); filter: drop-shadow(0 0 30px rgba(255,215,0,0.3)); }
        50% { transform: translateY(-5px); filter: drop-shadow(0 0 50px rgba(255,215,0,0.5)); }
    }
    .logo h1 { color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: 2px; }
    .logo h1 span { color: #ffd700; text-shadow: 0 0 30px rgba(255,215,0,0.2); }
    .logo p { color: rgba(255,255,255,0.4); font-size: 10px; margin-top: 2px; letter-spacing: 4px; text-transform: uppercase; }
    
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
    
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        flex-wrap: wrap;
        gap: 10px;
    }
    .header-left { display: flex; align-items: center; gap: 15px; }
    .header-right { display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }
    .header-user {
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        padding: 6px 12px 6px 6px;
        border-radius: 30px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s;
        position: relative;
    }
    .header-user:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,215,0,0.15);
    }
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0a0e27;
        font-weight: 700;
        font-size: 16px;
    }
    .user-info .name { color: #ffffff; font-size: 14px; font-weight: 600; }
    .user-info .id { color: rgba(255,255,255,0.3); font-size: 10px; }
    .user-plan-badge {
        background: rgba(255,215,0,0.12);
        color: #ffd700;
        font-size: 9px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 10px;
        border: 1px solid rgba(255,215,0,0.1);
    }
    .notif-bell { color: rgba(255,255,255,0.4); font-size: 18px; position: relative; cursor: pointer; }
    .notif-bell .badge {
        position: absolute;
        top: -6px;
        right: -6px;
        background: #ff6b6b;
        color: #fff;
        font-size: 9px;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
    }
    
    .nav {
        display: flex;
        gap: 5px;
        padding: 12px 0;
        flex-wrap: wrap;
        border-bottom: 1px solid rgba(255,255,255,0.03);
        margin-bottom: 20px;
    }
    .nav a {
        color: rgba(255,255,255,0.4);
        text-decoration: none;
        font-size: 13px;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: 8px;
        transition: all 0.3s;
        cursor: pointer;
    }
    .nav a:hover { color: #ffffff; background: rgba(255,255,255,0.05); }
    .nav a.active { color: #ffd700; background: rgba(255,215,0,0.08); }
    
    .user-dash-header {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 12px;
        margin-bottom: 20px;
    }
    .dash-stat {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .dash-stat .label { color: rgba(255,255,255,0.3); font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
    .dash-stat .value { color: #ffffff; font-size: 20px; font-weight: 700; margin-top: 4px; }
    .dash-stat .value span { color: #ffd700; font-size: 14px; }
    .dash-stat .sub { color: rgba(255,255,255,0.25); font-size: 11px; margin-top: 2px; }
    .dash-stat.gold { border-color: rgba(255,215,0,0.12); }
    .dash-stat.green { border-color: rgba(74,222,128,0.12); }
    .dash-stat.blue { border-color: rgba(59,130,246,0.12); }
    .dash-stat.purple { border-color: rgba(168,85,247,0.12); }
    .dash-stat.red { border-color: rgba(255,107,107,0.12); }
    
    .actions {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .actions .btn {
        padding: 10px 24px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border: none;
        border-radius: 10px;
        color: #0a0e27;
        font-weight: 700;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    .actions .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(255,215,0,0.2); }
    .actions .btn-secondary {
        background: rgba(255,255,255,0.06);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .actions .btn-secondary:hover {
        background: rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(255,255,255,0.05);
    }
    
    .cards {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }
    .card {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.04);
        text-align: center;
        transition: all 0.3s;
    }
    .card:hover { background: rgba(255,255,255,0.04); transform: translateY(-2px); }
    .card .icon { font-size: 24px; margin-bottom: 6px; }
    .card .label { color: rgba(255,255,255,0.3); font-size: 10px; text-transform: uppercase; }
    .card .value { color: #ffffff; font-size: 18px; font-weight: 700; margin-top: 4px; }
    .card .value.gold { color: #ffd700; }
    .card .value.green { color: #4ade80; }
    .card .value.blue { color: #3b82f6; }
    .card .value.purple { color: #a855f7; }
    .card .value.red { color: #ff6b6b; }
    
    .sections {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
    }
    .section {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .section h4 { color: #ffffff; font-size: 14px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .section h4 span { color: rgba(255,255,255,0.2); font-size: 12px; font-weight: 400; }
    
    .tx-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.02);
    }
    .tx-item .left { color: rgba(255,255,255,0.5); font-size: 12px; }
    .tx-item .right { font-size: 12px; font-weight: 600; }
    .tx-item .right.positive { color: #4ade80; }
    .tx-item .right.negative { color: #ff6b6b; }
    .tx-item .right.pending { color: #fbbf24; }
    
    .dropdown {
        display: none;
        position: absolute;
        top: 50px;
        right: 0;
        background: rgba(20,20,50,0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 8px 0;
        min-width: 200px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        z-index: 100;
    }
    .dropdown.active { display: block; }
    .dropdown a {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 18px;
        color: rgba(255,255,255,0.6);
        text-decoration: none;
        font-size: 13px;
        transition: all 0.3s;
    }
    .dropdown a:hover { background: rgba(255,255,255,0.05); color: #ffffff; }
    .dropdown a .icon { font-size: 16px; }
    .dropdown .divider { border-top: 1px solid rgba(255,255,255,0.05); margin: 6px 12px; }
    .dropdown .logout { color: #ff6b6b; }
    .dropdown .logout:hover { background: rgba(255,107,107,0.05); }
    
    .modal-overlay {
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
    .modal-overlay.active { display: flex; }
    .modal-content {
        background: rgba(20,20,50,0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 20px;
        padding: 30px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
    }
    .modal-content h3 { color: #ffffff; font-size: 20px; margin-bottom: 15px; text-align: center; }
    .modal-content .close-btn {
        float: right;
        color: rgba(255,255,255,0.3);
        font-size: 24px;
        cursor: pointer;
        background: none;
        border: none;
    }
    .modal-content .close-btn:hover { color: #ffffff; }
    
    .modal-plan-card {
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
    .modal-plan-card h4 { color: #ffd700; font-size: 14px; }
    .modal-plan-card p { color: rgba(255,255,255,0.4); font-size: 11px; margin: 2px 0; }
    .modal-plan-card .return { color: #4ade80; font-weight: 600; }
    .modal-plan-card .plan-price { color: #ffffff; font-size: 16px; font-weight: 700; text-align: right; }
    .modal-plan-card .plan-price small { color: rgba(255,255,255,0.3); font-size: 10px; font-weight: 400; }
    .modal-plan-card .btn-sm {
        padding: 6px 14px;
        font-size: 11px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        border: none;
        border-radius: 6px;
        color: #0a0e27;
        font-weight: 700;
        cursor: pointer;
        margin-top: 4px;
    }
    .modal-plan-card .btn-sm:hover { transform: scale(1.05); }
    
    .error-message {
        background: rgba(255,107,107,0.08);
        border: 1px solid rgba(255,107,107,0.12);
        color: #ff6b6b;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 15px;
        text-align: center;
    }
    .success-message {
        background: rgba(74,222,128,0.08);
        border: 1px solid rgba(74,222,128,0.12);
        color: #4ade80;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .withdraw-section {
        margin-top: 15px;
        padding: 15px;
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .withdraw-section h4 { color: #ffffff; font-size: 14px; margin-bottom: 10px; }
    .form-group { margin-bottom: 12px; }
    .form-group input {
        width: 100%;
        padding: 12px 14px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        color: #ffffff;
        font-size: 14px;
        outline: none;
    }
    .form-group input:focus {
        border-color: #ffd700;
        background: rgba(255,215,0,0.05);
    }
    .form-group input::placeholder { color: rgba(255,255,255,0.2); }
    
    .profile-info {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 15px 0;
    }
    .profile-item {
        background: rgba(255,255,255,0.02);
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .profile-item .label { color: rgba(255,255,255,0.3); font-size: 10px; text-transform: uppercase; }
    .profile-item .value { color: #ffffff; font-size: 15px; font-weight: 600; margin-top: 4px; }
    .profile-item .value.gold { color: #ffd700; }
    
    .simple-modal {
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
    .simple-modal.active { display: flex; }
    .simple-modal-content {
        background: rgba(20,20,50,0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 20px;
        padding: 30px;
        max-width: 400px;
        width: 90%;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
    }
    .simple-modal-content h3 { color: #ffffff; font-size: 20px; margin-bottom: 10px; }
    .simple-modal-content p { color: rgba(255,255,255,0.5); font-size: 14px; line-height: 1.6; margin-bottom: 20px; }
    .simple-modal-content .btn { width: auto; display: inline-block; padding: 10px 30px; }
    .simple-modal-content .icon-big { font-size: 48px; margin-bottom: 15px; display: block; }
    
    @media (max-width: 992px) {
        .user-dash-header { grid-template-columns: 1fr 1fr; }
        .cards { grid-template-columns: repeat(3, 1fr); }
        .sections { grid-template-columns: 1fr; }
        .profile-info { grid-template-columns: 1fr; }
    }
    @media (max-width: 600px) {
        .container { padding: 15px; }
        .header { flex-direction: column; align-items: stretch; }
        .header-right { justify-content: space-between; }
        .user-dash-header { grid-template-columns: 1fr; }
        .cards { grid-template-columns: 1fr 1fr; }
        .nav { gap: 3px; }
        .nav a { font-size: 11px; padding: 4px 10px; }
        .actions { flex-direction: column; }
        .actions .btn { text-align: center; }
        .modal-content { padding: 20px; }
        .modal-plan-card { flex-direction: column; text-align: center; }
        .modal-plan-card .plan-price { text-align: center; margin-top: 8px; }
        .logo-diamond { width: 50px; height: 50px; }
        .logo h1 { font-size: 22px; }
    }
</style>
"""

# =====================
# JAVASCRIPT
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

function closePlansModal() {
    document.getElementById('plansModal').classList.remove('active');
}

function toggleDropdown() {
    document.getElementById('userDropdown').classList.toggle('active');
}

function openPlansModal() {
    document.getElementById('plansModal').classList.add('active');
}

function acheterPlan(planId) {
    fetch('/buy-plan/' + planId, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
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
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
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
# LANG
# =====================

LANG = {
    "fr": {
        "title": "VestiCore - Finans Dijital & Rewards",
        "logo_sub": "INVEST • CROISSANCE • PROSPÉRITÉ",
        "home_title": "Platfòm Finans Dijital",
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
        "no_active_plan": "❌ Vous devez avoir un plan actif pour faire un retrait.",
        "insufficient_balance_withdraw": "❌ Solde insuffisant pour ce retrait.",
        "home": "Accueil",
        "investment": "Investissement",
        "wallet": "Portefeuille",
        "referral": "Parrainage",
        "academy": "Académie",
        "tools": "Outils",
        "market": "Marché",
        "analytics": "Analyses",
        "my_profile": "Mon profil",
        "security": "Sécurité",
        "settings": "Paramètres",
        "active_plan": "Plan actif",
        "total_investment": "Investissement total",
        "referral_bonus_label": "Bonus de parrainage",
        "pending_withdraw": "Retrait en attente",
        "recent_transactions": "Transactions récentes",
        "earnings_history": "Historique des gains",
        "news": "Actualités",
        "promotions": "Promotions",
        "info_title": "ℹ️ À propos de VestiCore",
        "info_subtitle": "Tout ce que vous devez savoir sur notre plateforme",
        "info_section1_title": "💎 Qu'est-ce que VestiCore ?",
        "info_section1_text": "VestiCore est une plateforme de finance digitale qui permet à ses utilisateurs d'investir dans des plans rémunérateurs et de gagner des bénéfices quotidiens en USDT.",
        "info_section2_title": "⚙️ Comment ça fonctionne ?",
        "info_section2_text": "1. Créez votre compte gratuitement\n2. Déposez des USDT sur votre portefeuille\n3. Choisissez un plan d'investissement\n4. Recevez des bénéfices chaque jour\n5. Retirez vos gains à tout moment",
        "info_section3_title": "🔒 Sécurité",
        "info_section3_text": "VestiCore utilise des technologies de pointe pour sécuriser vos données et vos transactions : cryptage SSL, authentification sécurisée, KYC, et approbation manuelle des retraits par l'administrateur.",
        "info_section4_title": "🎁 Programme de parrainage",
        "info_section4_text": "Invitez vos amis et gagnez 2% de bonus sur les dépôts de vos 10 premiers investisseurs qualifiés.",
        "info_section5_title": "📊 Plans d'investissement",
        "info_section5_text": "10 plans disponibles de 10 USDT à 2000 USDT, avec des rendements journaliers de 0.90% à 1.90%.",
        "info_back": "← Retour au Dashboard",
        "settings": "⚙️ Paramètres",
        "change_password": "🔐 Changer mot de passe",
        "current_password": "Mot de passe actuel",
        "new_password": "Nouveau mot de passe",
        "confirm_password": "Confirmer le mot de passe",
        "password_changed": "✅ Mot de passe changé avec succès!",
        "password_mismatch": "❌ Les mots de passe ne correspondent pas",
        "wrong_password": "❌ Mot de passe actuel incorrect",
        "transactions_history": "📊 Historique des transactions",
        "earnings_history": "📈 Historique des gains",
        "no_transactions": "Aucune transaction pour le moment",
        "no_earnings": "Aucun gain pour le moment",
        "amount": "Montant",
        "date": "Date",
        "status": "Statut",
        "type": "Type",
        "two_factor": "🔑 Authentification à deux facteurs (2FA)",
        "enable_2fa": "Activer 2FA",
        "disable_2fa": "Désactiver 2FA",
        "session_management": "🖥️ Gestion des sessions",
        "active_sessions": "Sessions actives",
        "logout_all": "Se déconnecter de tous les appareils",
        "current_session": "Session actuelle",
        "last_login": "Dernière connexion",
        "ip_address": "Adresse IP",
        "device": "Appareil"
    },
    "en": {
        "title": "VestiCore - Digital Finance & Rewards",
        "logo_sub": "INVEST • GROW • PROSPER",
        "home_title": "Digital Finance Platform",
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
        "no_active_plan": "❌ You must have an active plan to withdraw.",
        "insufficient_balance_withdraw": "❌ Insufficient balance for this withdrawal.",
        "home": "Home",
        "investment": "Investment",
        "wallet": "Wallet",
        "referral": "Referral",
        "academy": "Academy",
        "tools": "Tools",
        "market": "Market",
        "analytics": "Analytics",
        "my_profile": "My Profile",
        "security": "Security",
        "settings": "Settings",
        "active_plan": "Active Plan",
        "total_investment": "Total Investment",
        "referral_bonus_label": "Referral Bonus",
        "pending_withdraw": "Pending Withdraw",
        "recent_transactions": "Recent Transactions",
        "earnings_history": "Earnings History",
        "news": "News",
        "promotions": "Promotions",
        "info_title": "ℹ️ About VestiCore",
        "info_subtitle": "Everything you need to know about our platform",
        "info_section1_title": "💎 What is VestiCore?",
        "info_section1_text": "VestiCore is a digital finance platform that allows users to invest in rewarding plans and earn daily profits in USDT.",
        "info_section2_title": "⚙️ How does it work?",
        "info_section2_text": "1. Create your account for free\n2. Deposit USDT into your wallet\n3. Choose an investment plan\n4. Receive daily benefits\n5. Withdraw your earnings anytime",
        "info_section3_title": "🔒 Security",
        "info_section3_text": "VestiCore uses advanced technologies to secure your data and transactions: SSL encryption, secure authentication, KYC, and manual approval of withdrawals by the administrator.",
        "info_section4_title": "🎁 Referral Program",
        "info_section4_text": "Invite your friends and earn 2% bonus on the deposits of your first 10 qualified investors.",
        "info_section5_title": "📊 Investment Plans",
        "info_section5_text": "10 plans available from 10 USDT to 2000 USDT, with daily returns from 0.90% to 1.90%.",
        "info_back": "← Back to Dashboard",
        "settings": "⚙️ Settings",
        "change_password": "🔐 Change password",
        "current_password": "Current password",
        "new_password": "New password",
        "confirm_password": "Confirm password",
        "password_changed": "✅ Password changed successfully!",
        "password_mismatch": "❌ Passwords do not match",
        "wrong_password": "❌ Current password is incorrect",
        "transactions_history": "📊 Transaction History",
        "earnings_history": "📈 Earnings History",
        "no_transactions": "No transactions yet",
        "no_earnings": "No earnings yet",
        "amount": "Amount",
        "date": "Date",
        "status": "Status",
        "type": "Type",
        "two_factor": "🔑 Two-Factor Authentication (2FA)",
        "enable_2fa": "Enable 2FA",
        "disable_2fa": "Disable 2FA",
        "session_management": "🖥️ Session Management",
        "active_sessions": "Active sessions",
        "logout_all": "Logout all devices",
        "current_session": "Current session",
        "last_login": "Last login",
        "ip_address": "IP Address",
        "device": "Device"
    },
    "es": {
        "title": "VestiCore - Finanzas Digitales & Rewards",
        "logo_sub": "INVIERTE • CRECE • PROSPERA",
        "home_title": "Plataforma de Finanzas Digitales",
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
        "no_active_plan": "❌ Debes tener un plan activo para retirar.",
        "insufficient_balance_withdraw": "❌ Saldo insuficiente para este retiro.",
        "home": "Inicio",
        "investment": "Inversión",
        "wallet": "Billetera",
        "referral": "Referidos",
        "academy": "Academia",
        "tools": "Herramientas",
        "market": "Mercado",
        "analytics": "Análisis",
        "my_profile": "Mi Perfil",
        "security": "Seguridad",
        "settings": "Configuración",
        "active_plan": "Plan Activo",
        "total_investment": "Inversión Total",
        "referral_bonus_label": "Bonificación por Referidos",
        "pending_withdraw": "Retiro Pendiente",
        "recent_transactions": "Transacciones Recientes",
        "earnings_history": "Historial de Ganancias",
        "news": "Noticias",
        "promotions": "Promociones",
        "info_title": "ℹ️ Acerca de VestiCore",
        "info_subtitle": "Todo lo que necesitas saber sobre nuestra plataforma",
        "info_section1_title": "💎 ¿Qué es VestiCore?",
        "info_section1_text": "VestiCore es una plataforma de finanzas digitales que permite a los usuarios invertir en planes rentables y ganar beneficios diarios en USDT.",
        "info_section2_title": "⚙️ ¿Cómo funciona?",
        "info_section2_text": "1. Crea tu cuenta gratis\n2. Deposita USDT en tu billetera\n3. Elige un plan de inversión\n4. Recibe beneficios diarios\n5. Retira tus ganancias en cualquier momento",
        "info_section3_title": "🔒 Seguridad",
        "info_section3_text": "VestiCore utiliza tecnologías avanzadas para proteger tus datos y transacciones: cifrado SSL, autenticación segura, KYC y aprobación manual de retiros por el administrador.",
        "info_section4_title": "🎁 Programa de referidos",
        "info_section4_text": "Invita a tus amigos y gana 2% de bonificación sobre los depósitos de tus primeros 10 inversores calificados.",
        "info_section5_title": "📊 Planes de inversión",
        "info_section5_text": "10 planes disponibles desde 10 USDT hasta 2000 USDT, con rendimientos diarios del 0.90% al 1.90%.",
        "info_back": "← Volver al Dashboard",
        "settings": "⚙️ Configuración",
        "change_password": "🔐 Cambiar contraseña",
        "current_password": "Contraseña actual",
        "new_password": "Nueva contraseña",
        "confirm_password": "Confirmar contraseña",
        "password_changed": "✅ Contraseña cambiada con éxito!",
        "password_mismatch": "❌ Las contraseñas no coinciden",
        "wrong_password": "❌ Contraseña actual incorrecta",
        "transactions_history": "📊 Historial de transacciones",
        "earnings_history": "📈 Historial de ganancias",
        "no_transactions": "Sin transacciones por ahora",
        "no_earnings": "Sin ganancias por ahora",
        "amount": "Monto",
        "date": "Fecha",
        "status": "Estado",
        "type": "Tipo",
        "two_factor": "🔑 Autenticación de dos factores (2FA)",
        "enable_2fa": "Activar 2FA",
        "disable_2fa": "Desactivar 2FA",
        "session_management": "🖥️ Gestión de sesiones",
        "active_sessions": "Sesiones activas",
        "logout_all": "Cerrar sesión en todos los dispositivos",
        "current_session": "Sesión actual",
        "last_login": "Último inicio de sesión",
        "ip_address": "Dirección IP",
        "device": "Dispositivo"
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
    user_id_display = Column(String, unique=True, nullable=True)
    kyc_status = Column(String, default="unverified")
    kyc_document = Column(String, nullable=True)
    kyc_submitted_at = Column(DateTime, nullable=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)

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

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    message = Column(String)
    read = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.now)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    subject = Column(String)
    message = Column(Text)
    status = Column(String, default="open")
    admin_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

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

def generate_user_id():
    return "VC" + str(uuid.uuid4())[:6].upper()

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
# SVG LOGO DIAMANT
# =====================

LOGO_SVG = """
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="diamondGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffd700"/>
            <stop offset="40%" stop-color="#f5c800"/>
            <stop offset="70%" stop-color="#f0a500"/>
            <stop offset="100%" stop-color="#d48900"/>
        </linearGradient>
        <linearGradient id="shineGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#ffffff" stop-opacity="0.1"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="innerGlow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#fff8cc" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#f0a500" stop-opacity="0.3"/>
        </linearGradient>
    </defs>
    <polygon points="50,5 90,45 50,85 10,45" fill="rgba(0,0,0,0.2)" transform="translate(2,2)"/>
    <polygon points="50,5 90,45 50,85 10,45" fill="url(#goldGrad)" filter="url(#diamondGlow)"/>
    <polygon points="50,5 10,45 50,50" fill="url(#shineGrad)" opacity="0.6"/>
    <polygon points="50,5 90,45 50,50" fill="url(#shineGrad)" opacity="0.3"/>
    <polygon points="10,45 50,85 50,50" fill="url(#innerGlow)" opacity="0.4"/>
    <polygon points="90,45 50,85 50,50" fill="url(#innerGlow)" opacity="0.2"/>
    <circle cx="45" cy="30" r="4" fill="white" opacity="0.8"/>
    <circle cx="42" cy="27" r="2" fill="white" opacity="0.9"/>
    <circle cx="55" cy="65" r="2" fill="#f0a500" opacity="0.4"/>
    <text x="50" y="58" text-anchor="middle" font-size="36" font-weight="900" fill="#0a0e27" font-family="Arial, sans-serif" letter-spacing="-2">V</text>
</svg>
"""

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
            {LOGO_SVG}
        </div>
        <h1>Vesti<span>Core</span></h1>
        <p>{LANG[lang_key].get('logo_sub', 'INVEST • GROW • PROSPER')}</p>
    </div>
    """

# =====================
# SELÈKSYON LANG
# =====================

@app.get("/set-lang/{lang}")
def set_lang(lang: str, request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="lang", value=lang, max_age=365*24*60*60)
    return response

# =====================
# MODAL HTML
# =====================

def get_modal_html():
    return f"""
    <div id="customModal" class="simple-modal">
        <div class="simple-modal-content">
            <span class="icon-big" id="modalIcon">ℹ️</span>
            <h3 id="modalTitle">Information</h3>
            <p id="modalMessage">Message</p>
            <button onclick="closeModal()" class="btn" style="width:auto;display:inline-block;padding:10px 30px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:8px;color:#0a0e27;font-weight:700;cursor:pointer;">Fermer</button>
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
        <div class="container" style="max-width:600px;">
            {get_logo_html(lang, request)}
            
            <div style="text-align:center;margin:10px 0 25px;">
                <p style="color:rgba(255,255,255,0.6);font-size:16px;line-height:1.8;">
                    {LANG[lang].get('home_title', 'Digital Finance Platform')}<br>
                    <span style="color:#ffd700;font-size:20px;font-weight:600;">{LANG[lang].get('home_desc', 'Make your money grow')}</span>
                </p>
            </div>
            
            <a href="/register" class="btn" style="display:block;text-align:center;text-decoration:none;width:100%;padding:15px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:10px;color:#0a0e27;font-weight:700;font-size:16px;cursor:pointer;">{LANG[lang].get('home_btn_register', 'Create account')}</a>
            <br>
            <a href="/login" class="btn btn-secondary" style="display:block;text-align:center;text-decoration:none;width:100%;padding:15px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:10px;color:#ffffff;font-weight:700;font-size:16px;cursor:pointer;">{LANG[lang].get('home_btn_login', 'Login')}</a>
            
            <div style="text-align:center;margin-top:25px;color:rgba(255,255,255,0.1);font-size:11px;">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# REGISTER PAGE
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, ref: str = None, error: str = None):
    lang = get_lang(request)
    ref_value = f'value="{ref}"' if ref else ''
    error_html = f'<div class="error-message">❌ {error}</div>' if error else ''
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('register_title', 'Create account')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:500px;">
            {get_logo_html(lang, request)}
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('register_title', 'Create your account')}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:13px;text-align:center;margin-bottom:22px;">{LANG[lang].get('register_sub', 'Start your investment journey')}</div>
            
            {error_html}
            
            <form method="post" action="/register">
                <div class="form-group">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;font-weight:500;display:block;margin-bottom:5px;">{LANG[lang].get('register_username', 'Username')}</label>
                    <input type="text" name="username" placeholder="{LANG[lang].get('register_username', 'Username')}" required>
                </div>
                <div class="form-group">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;font-weight:500;display:block;margin-bottom:5px;">{LANG[lang].get('register_password', 'Password')}</label>
                    <input type="password" name="password" placeholder="{LANG[lang].get('register_password', 'Password')}" required>
                </div>
                <div class="form-group">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;font-weight:500;display:block;margin-bottom:5px;">{LANG[lang].get('register_ref', 'Referral code (optional)')}</label>
                    <input type="text" name="ref" placeholder="{LANG[lang].get('register_ref', 'Referral code (optional)')}" {ref_value}>
                </div>
                <button type="submit" class="btn" style="width:100%;padding:15px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:10px;color:#0a0e27;font-weight:700;font-size:15px;cursor:pointer;">{LANG[lang].get('register_btn', 'Create account')}</button>
            </form>
            
            <div style="text-align:center;margin-top:18px;color:rgba(255,255,255,0.35);font-size:13px;">
                {LANG[lang].get('register_link', 'Already have an account?')} <a href="/login" style="color:#ffd700;text-decoration:none;font-weight:600;">{LANG[lang].get('register_link_btn', 'Login')}</a>
            </div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# REGISTER ACTION
# =====================

@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    ref: str = Form(None),
    db: Session = Depends(get_db)
):
    user_exist = db.query(User).filter(User.username == username).first()
    if user_exist:
        return RedirectResponse(url="/register?error=Nom+d%27utilisateur+déjà+pris", status_code=303)
    
    admin_key = os.getenv("ADMIN_SECRET_KEY", "vesticore-admin-2026")
    
    if ref and ref.strip() == admin_key.strip():
        is_admin = 1
        ref = None
    else:
        is_admin = 0
    
    new_user = User(
        username=username,
        password=hash_password(password),
        referral_code=create_referral_code(username),
        referred_by=ref,
        is_admin=is_admin,
        user_id_display=generate_user_id()
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
    return RedirectResponse(url="/login?success=Compte+créé+avec+succès", status_code=303)

# =====================
# LOGIN PAGE
# =====================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None, success: str = None):
    lang = get_lang(request)
    error_html = f'<div class="error-message">❌ {error}</div>' if error else ''
    success_html = f'<div class="success-message">✅ {success}</div>' if success else ''
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('login_title', 'Login')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:500px;">
            {get_logo_html(lang, request)}
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('login_title', 'Welcome back')}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:13px;text-align:center;margin-bottom:22px;">{LANG[lang].get('login_sub', 'Login to access your space')}</div>
            
            {success_html}
            {error_html}
            
            <form method="post" action="/login">
                <div class="form-group">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;font-weight:500;display:block;margin-bottom:5px;">{LANG[lang].get('register_username', 'Username')}</label>
                    <input type="text" name="username" placeholder="{LANG[lang].get('register_username', 'Username')}" required>
                </div>
                <div class="form-group">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;font-weight:500;display:block;margin-bottom:5px;">{LANG[lang].get('register_password', 'Password')}</label>
                    <input type="password" name="password" placeholder="{LANG[lang].get('register_password', 'Password')}" required>
                </div>
                <button type="submit" class="btn" style="width:100%;padding:15px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:10px;color:#0a0e27;font-weight:700;font-size:15px;cursor:pointer;">{LANG[lang].get('login_btn', 'Login')}</button>
            </form>
            
            <div style="text-align:center;margin-top:18px;color:rgba(255,255,255,0.35);font-size:13px;">
                {LANG[lang].get('login_link', 'No account?')} <a href="/register" style="color:#ffd700;text-decoration:none;font-weight:600;">{LANG[lang].get('login_link_btn', 'Create account')}</a>
            </div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# LOGIN ACTION
# =====================

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return RedirectResponse(url="/login?error=Nom+d%27utilisateur+incorrect", status_code=303)
    if not verify_password(password, user.password):
        return RedirectResponse(url="/login?error=Mot+de+passe+incorrect", status_code=303)
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
    active_plan_info = get_user_active_plan(db, user.id)
    
    referrals = db.query(Referral).filter(Referral.referrer == user.username).all()
    qualified_investors = sum(1 for r in referrals if r.has_invested)
    total_bonus = sum(r.bonus_amount for r in referrals)
    
    notifications = db.query(Notification).filter(Notification.username == user.username, Notification.read == False).all()
    notif_count = len(notifications)
    
    logs = db.query(ActivityLog).filter(ActivityLog.username == user.username).order_by(ActivityLog.date.desc()).limit(10).all()
    
    total_investment = db.query(UserPlan).filter(UserPlan.user_id == user.id, UserPlan.status == "active").first()
    total_investment_amount = total_investment.amount if total_investment else 0
    
    pending_withdraw = db.query(Withdraw).filter(Withdraw.username == user.username, Withdraw.status == "pending").all()
    pending_withdraw_amount = sum(w.amount for w in pending_withdraw)
    
    active_plan_name = active_plan_info["plan"].name if active_plan_info else "Aucun"
    
    plans = db.query(Plan).all()
    plan_modal_html = ""
    for plan in plans:
        total_return = plan.price * (plan.daily_return / 100) * plan.duration
        daily_usdt = plan.price * (plan.daily_return / 100)
        plan_modal_html += f"""
        <div class="modal-plan-card">
            <div>
                <h4>{plan.name}</h4>
                <p>{plan.description}</p>
                <p>⏳ {plan.duration} jours • <span class="return">📈 {plan.daily_return}% / jour</span></p>
                <p style="color:rgba(255,255,255,0.3);font-size:10px;">💵 {daily_usdt:.2f} USDT/jour • 💎 Total: {total_return:.2f} USDT</p>
            </div>
            <div class="plan-price">
                {plan.price} <small>USDT</small>
                <br>
                <button onclick="acheterPlan({plan.id}); closePlansModal();" class="btn-sm">{LANG[lang].get('dashboard_buy', 'Buy')}</button>
            </div>
        </div>
        """
    
    history_html = ""
    for log in logs[:5]:
        if "Benefis" in log.action:
            history_html += f"""
            <div class="tx-item">
                <span class="left">{log.date.strftime('%d/%m %H:%M')} - {log.action[:30]}...</span>
                <span class="right positive">+{log.action.split(':')[-1].strip() if ':' in log.action else ''}</span>
            </div>
            """
        elif "Depo" in log.action:
            history_html += f"""
            <div class="tx-item">
                <span class="left">{log.date.strftime('%d/%m %H:%M')} - {log.action[:30]}...</span>
                <span class="right positive">💰</span>
            </div>
            """
        elif "retrè" in log.action:
            history_html += f"""
            <div class="tx-item">
                <span class="left">{log.date.strftime('%d/%m %H:%M')} - {log.action[:30]}...</span>
                <span class="right pending">⏳</span>
            </div>
            """
    
    profile_items = f"""
    <div class="profile-item"><div class="label">Nom d'utilisateur</div><div class="value">{user.username}</div></div>
    <div class="profile-item"><div class="label">ID</div><div class="value gold">{user.user_id_display or 'VC000001'}</div></div>
    <div class="profile-item"><div class="label">Plan actif</div><div class="value">{active_plan_name}</div></div>
    <div class="profile-item"><div class="label">Solde</div><div class="value gold">{user.balance:.2f} USDT</div></div>
    <div class="profile-item"><div class="label">Bonus de parrainage</div><div class="value">{total_bonus:.2f} USDT</div></div>
    <div class="profile-item"><div class="label">Membres depuis</div><div class="value">{user.created_at.strftime('%d/%m/%Y')}</div></div>
    """
    
    kyc_status_text = {
        "unverified": "Non vérifié",
        "pending": "En attente de vérification",
        "verified": "✅ Vérifié",
        "rejected": "❌ Rejeté"
    }.get(user.kyc_status, "Non vérifié")
    
    admin_link = f'<a href="/admin" style="color:rgba(255,255,255,0.08);text-decoration:none;font-size:10px;">Admin</a>' if user.is_admin == 1 else ''
    
    return f"""
    <html>
    <head>
        <title>Dashboard - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container">
            <!-- HEADER -->
            <div class="header">
                <div class="header-left">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div class="logo-diamond" style="width:45px;height:45px;margin:0;">
                            {LOGO_SVG}
                        </div>
                        <div class="logo-text" style="font-size:20px;">Vesti<span style="color:#ffd700;">Core</span></div>
                    </div>
                </div>
                <div class="header-right">
                    <div class="notif-bell">
                        🔔
                        {f'<span class="badge">{notif_count}</span>' if notif_count > 0 else ''}
                    </div>
                    <div class="header-user" onclick="toggleDropdown()">
                        <div class="avatar">{user.username[0].upper()}</div>
                        <div class="user-info">
                            <div class="name">{user.username}</div>
                            <div class="id">{user.user_id_display or 'VC000001'} • <span class="user-plan-badge">{active_plan_name}</span></div>
                        </div>
                        <span style="color:rgba(255,255,255,0.2);font-size:12px;">▼</span>
                    </div>
                    <div id="userDropdown" class="dropdown">
                        <a href="#" onclick="document.getElementById('profileSection').scrollIntoView(); toggleDropdown(); return false;"><span class="icon">👤</span> {LANG[lang].get('my_profile', 'My Profile')}</a>
                        <a href="/info"><span class="icon">ℹ️</span> À propos</a>
                        <a href="/settings"><span class="icon">⚙️</span> {LANG[lang].get('settings', 'Settings')}</a>
                        <a href="#" onclick="document.getElementById('profileSection').scrollIntoView(); toggleDropdown(); return false;"><span class="icon">🔐</span> {LANG[lang].get('security', 'Security')}</a>
                        <div class="divider"></div>
                        <a href="/logout" class="logout"><span class="icon">🚪</span> {LANG[lang].get('logout', 'Logout')}</a>
                    </div>
                </div>
            </div>
            
            <!-- NAV -->
            <div class="nav">
                <a href="/dashboard" class="active">🏠 {LANG[lang].get('home', 'Home')}</a>
                <a href="#" onclick="openPlansModal(); return false;">💼 {LANG[lang].get('investment', 'Investment')}</a>
                <a href="/deposit-page">💳 {LANG[lang].get('wallet', 'Wallet')}</a>
                <a href="/referral">👥 {LANG[lang].get('referral', 'Referral')}</a>
                <a href="#" onclick="document.getElementById('profileSection').scrollIntoView(); return false;">👤 {LANG[lang].get('my_profile', 'Profile')}</a>
                <a href="/kyc">🪪 KYC</a>
                <a href="/info">ℹ️ À propos</a>
                <a href="/settings">⚙️ {LANG[lang].get('settings', 'Settings')}</a>
            </div>
            
            <!-- USER DASHBOARD HEADER -->
            <div class="user-dash-header">
                <div class="dash-stat gold">
                    <div class="label">{LANG[lang].get('dashboard_balance', 'BALANCE')}</div>
                    <div class="value">{user.balance:.2f} <span>USDT</span></div>
                    <div class="sub">🎁 Rewards: {total_bonus:.2f} USDT</div>
                </div>
                <div class="dash-stat green">
                    <div class="label">{LANG[lang].get('active_plan', 'Active Plan')}</div>
                    <div class="value" style="font-size:16px;">⭐ {active_plan_name}</div>
                    <div class="sub">👥 {len(referrals)} referrals</div>
                </div>
                <div class="dash-stat blue">
                    <div class="label">{LANG[lang].get('total_investment', 'Total Investment')}</div>
                    <div class="value">{total_investment_amount:.2f} <span>USDT</span></div>
                    <div class="sub">💰 Investi</div>
                </div>
                <div class="dash-stat purple">
                    <div class="label">{LANG[lang].get('referral_bonus_label', 'Referral Bonus')}</div>
                    <div class="value">{total_bonus:.2f} <span>USDT</span></div>
                    <div class="sub">🎁 {REFERRAL_MIN_INVESTORS - qualified_investors} restants</div>
                </div>
                <div class="dash-stat red" style="grid-column: span 1;">
                    <div class="label">{LANG[lang].get('pending_withdraw', 'Pending Withdraw')}</div>
                    <div class="value" style="color:#fbbf24;">{pending_withdraw_amount:.2f} <span>USDT</span></div>
                    <div class="sub">⏳ En attente</div>
                </div>
            </div>
            
            <!-- ACTIONS -->
            <div class="actions">
                <a href="/deposit-page" class="btn">💵 {LANG[lang].get('dashboard_deposit', 'Deposit')}</a>
                <a href="#" onclick="document.getElementById('withdrawSection').scrollIntoView(); return false;" class="btn btn-secondary">💸 {LANG[lang].get('dashboard_withdraw', 'Withdraw')}</a>
                <a href="/referral" class="btn btn-secondary">👥 {LANG[lang].get('dashboard_referral', 'Referral')}</a>
            </div>
            
            <!-- CARDS -->
            <div class="cards">
                <div class="card">
                    <div class="icon">💰</div>
                    <div class="label">{LANG[lang].get('dashboard_balance', 'BALANCE')}</div>
                    <div class="value gold">{user.balance:.2f} USDT</div>
                </div>
                <div class="card">
                    <div class="icon">⭐</div>
                    <div class="label">{LANG[lang].get('active_plan', 'Active Plan')}</div>
                    <div class="value green">{active_plan_name}</div>
                </div>
                <div class="card">
                    <div class="icon">📊</div>
                    <div class="label">{LANG[lang].get('total_investment', 'Total Investment')}</div>
                    <div class="value blue">{total_investment_amount:.2f} USDT</div>
                </div>
                <div class="card">
                    <div class="icon">🎁</div>
                    <div class="label">{LANG[lang].get('referral_bonus_label', 'Referral Bonus')}</div>
                    <div class="value purple">{total_bonus:.2f} USDT</div>
                </div>
                <div class="card">
                    <div class="icon">⏳</div>
                    <div class="label">{LANG[lang].get('pending_withdraw', 'Pending Withdraw')}</div>
                    <div class="value red">{pending_withdraw_amount:.2f} USDT</div>
                </div>
            </div>
            
            <!-- SECTIONS -->
            <div class="sections">
                <div class="section">
                    <h4>📜 {LANG[lang].get('recent_transactions', 'Recent Transactions')} <span>Dènye aktivite</span></h4>
                    {history_html if history_html else '<div style="color:rgba(255,255,255,0.15);font-size:12px;text-align:center;padding:15px 0;">Pa gen tranzaksyon</div>'}
                </div>
                <div>
                    <div class="section" style="margin-bottom:12px;">
                        <h4>📈 {LANG[lang].get('earnings_history', 'Earnings History')}</h4>
                        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.02);">
                            <span style="color:rgba(255,255,255,0.4);font-size:12px;">Today</span>
                            <span style="color:#4ade80;font-size:12px;font-weight:600;">+0.00 USDT</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;padding:8px 0;">
                            <span style="color:rgba(255,255,255,0.4);font-size:12px;">This month</span>
                            <span style="color:#4ade80;font-size:12px;font-weight:600;">+{total_bonus:.2f} USDT</span>
                        </div>
                    </div>
                    <div class="section">
                        <h4>📰 {LANG[lang].get('news', 'News')}</h4>
                        <div class="news-item">
                            <div class="title">🎉 Bienvenue sur VestiCore!</div>
                            <div class="date">{datetime.now().strftime('%d/%m/%Y')}</div>
                        </div>
                        <div class="news-item">
                            <div class="title">💰 Nouveaux plans disponibles</div>
                            <div class="date">{datetime.now().strftime('%d/%m/%Y')}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- PROMOTIONS -->
            <div class="section" style="margin-bottom:15px;">
                <h4>🎯 {LANG[lang].get('promotions', 'Promotions')}</h4>
                <div class="promo-item">
                    <div class="title">🎁 Bonus de parrainage</div>
                    <div class="desc">Gagnez 2% sur les dépôts de vos 10 premiers investisseurs!</div>
                </div>
                <div class="promo-item">
                    <div class="title">💰 Plan VIP Pro</div>
                    <div class="desc">Investissez 2000 USDT et gagnez 1.90% par jour pendant 120 jours</div>
                </div>
            </div>
            
            <!-- PROFILE SECTION -->
            <div id="profileSection" class="section" style="margin-top:15px;">
                <h4>👤 {LANG[lang].get('my_profile', 'My Profile')}</h4>
                <div class="profile-info">
                    {profile_items}
                </div>
                <div style="margin-top:12px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">
                    <h4 style="color:#ffffff;font-size:13px;">🪪 KYC Verification</h4>
                    <div style="padding:10px;border-radius:8px;text-align:center;margin:8px 0;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);">
                        <strong>Status:</strong> {kyc_status_text}
                    </div>
                    <a href="/kyc" class="btn btn-secondary" style="display:inline-block;padding:8px 20px;font-size:12px;text-decoration:none;color:#fff;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;cursor:pointer;">Gérer KYC</a>
                </div>
            </div>
            
            <!-- WITHDRAW SECTION -->
            <div id="withdrawSection" class="withdraw-section">
                <h4>💸 {LANG[lang].get('dashboard_withdraw', 'Withdraw')}</h4>
                <div class="form-group">
                    <input type="number" id="withdrawAmount" placeholder="{LANG[lang].get('dashboard_withdraw_placeholder', 'USDT Amount')}" step="0.01" min="1">
                </div>
                <div class="form-group">
                    <input type="text" id="withdrawWallet" placeholder="{LANG[lang].get('dashboard_withdraw_wallet', 'Your TRC20 address')}">
                </div>
                <button onclick="faireRetrait()" class="btn btn-secondary" style="width:100%;padding:12px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-weight:700;font-size:14px;cursor:pointer;">{LANG[lang].get('dashboard_withdraw_btn', 'Submit request')}</button>
                <p style="color:rgba(255,255,255,0.2);font-size:10px;text-align:center;margin-top:8px;">⚠️ {LANG[lang].get('dashboard_withdraw_warning', 'Withdrawals are subject to admin approval')}</p>
            </div>
            
            <!-- FOOTER -->
            <div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
                {admin_link}
                <span style="color:rgba(255,255,255,0.08);font-size:9px;">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</span>
            </div>
        </div>
        
        <!-- PLANS MODAL -->
        <div id="plansModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-btn" onclick="closePlansModal()">✕</button>
                <h3>💼 {LANG[lang].get('dashboard_plans', 'Investment Plans')}</h3>
                {plan_modal_html}
            </div>
        </div>
        
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# KYC PAGE
# =====================

@app.get("/kyc", response_class=HTMLResponse)
def kyc_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    lang = get_lang(request)
    return f"""
    <html>
    <head>
        <title>KYC - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:600px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">KYC</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← Retour</a>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">🪪 Vérification KYC</div>
            <div style="color:rgba(255,255,255,0.4);font-size:13px;text-align:center;margin-bottom:22px;">Téléchargez vos documents pour vérifier votre identité</div>
            
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:20px;border:1px solid rgba(255,255,255,0.04);">
                <div style="margin-bottom:15px;">
                    <label style="color:rgba(255,255,255,0.6);font-size:12px;display:block;margin-bottom:5px;">Status actuel</label>
                    <div style="padding:10px;border-radius:8px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);">
                        <span style="color:#ffffff;">{user.kyc_status.upper()}</span>
                    </div>
                </div>
                
                <form method="post" action="/kyc/submit">
                    <div class="form-group">
                        <label style="color:rgba(255,255,255,0.6);font-size:12px;display:block;margin-bottom:5px;">Nom complet</label>
                        <input type="text" name="full_name" value="{user.full_name or ''}" placeholder="Votre nom complet" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;">
                    </div>
                    <div class="form-group">
                        <label style="color:rgba(255,255,255,0.6);font-size:12px;display:block;margin-bottom:5px;">Email</label>
                        <input type="email" name="email" value="{user.email or ''}" placeholder="votre@email.com" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;">
                    </div>
                    <div class="form-group">
                        <label style="color:rgba(255,255,255,0.6);font-size:12px;display:block;margin-bottom:5px;">Téléphone</label>
                        <input type="text" name="phone" value="{user.phone or ''}" placeholder="+509 0000 0000" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;">
                    </div>
                    <div class="form-group">
                        <label style="color:rgba(255,255,255,0.6);font-size:12px;display:block;margin-bottom:5px;">Pays</label>
                        <input type="text" name="country" value="{user.country or ''}" placeholder="Haïti" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;">
                    </div>
                    <button type="submit" class="btn" style="width:100%;padding:14px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:8px;color:#0a0e27;font-weight:700;font-size:15px;cursor:pointer;">Soumettre KYC</button>
                </form>
            </div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

@app.post("/kyc/submit")
def kyc_submit(
    request: Request,
    full_name: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    country: str = Form(None),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)
    
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if phone:
        user.phone = phone
    if country:
        user.country = country
    
    user.kyc_status = "pending"
    user.kyc_submitted_at = datetime.now()
    
    db.commit()
    add_log(db, user.username, "Soumis KYC")
    return RedirectResponse(url="/dashboard?success=KYC+soumis+avec+succès", status_code=303)

# =====================
# BUY PLAN
# =====================

@app.post("/buy-plan/{plan_id}")
def buy_plan(
    plan_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = request.session.get("username")
    if not username:
        return JSONResponse(status_code=401, content={"success": False, "message": "Ou dwe konekte"})
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return JSONResponse(status_code=404, content={"success": False, "message": "Itilizatè pa jwenn"})
    
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        return JSONResponse(content={"success": False, "message": LANG[get_lang(request)].get('plan_not_found', 'Plan not found')})
    
    existing = db.query(UserPlan).filter(
        UserPlan.user_id == user.id,
        UserPlan.status == "active"
    ).first()
    if existing:
        return JSONResponse(content={"success": False, "message": LANG[get_lang(request)].get('already_has_plan', 'You already have an active plan')})
    
    if user.balance < plan.price:
        return JSONResponse(content={"success": False, "message": LANG[get_lang(request)].get('insufficient_balance', 'Insufficient balance')})
    
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
    
    return JSONResponse(content={"success": True, "message": LANG[get_lang(request)].get('plan_bought', 'Plan purchased successfully!')})

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
        <title>{LANG[lang].get('deposit_title', 'Deposit')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:550px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← {LANG[lang].get('deposit_back', 'Back')}</a>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('deposit_title', '💰 USDT Deposit')}</div>
            
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
                <button type="submit" class="btn" style="width:100%;padding:14px;background:linear-gradient(135deg,#ffd700,#f0a500);border:none;border-radius:8px;color:#0a0e27;font-weight:700;font-size:15px;cursor:pointer;">{LANG[lang].get('deposit_btn', 'Submit deposit')}</button>
            </form>
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
# WITHDRAW
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
        return JSONResponse(status_code=401, content={"success": False, "message": "Ou dwe konekte"})
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return JSONResponse(status_code=404, content={"success": False, "message": "Itilizatè pa jwenn"})
    
    active_plan_info = get_user_active_plan(db, user.id)
    if not active_plan_info:
        return JSONResponse(content={"success": False, "message": LANG[get_lang(request)].get('no_active_plan', 'You must have an active plan to withdraw')})
    
    if amount <= 0:
        return JSONResponse(content={"success": False, "message": "Montan pa valab"})
    
    if user.balance < amount:
        return JSONResponse(content={"success": False, "message": LANG[get_lang(request)].get('insufficient_balance_withdraw', 'Insufficient balance for this withdrawal')})
    
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
    add_log(db, user.username, f"Demann retrè {amount} USDT voye (frè: {fee} USDT)")
    db.commit()
    
    return JSONResponse(content={"success": True, "message": LANG[get_lang(request)].get('withdraw_success', 'Withdrawal request sent successfully!')})

# =====================
# INFO PAGE
# =====================

@app.get("/info", response_class=HTMLResponse)
def info_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    lang = get_lang(request)
    
    plans = db.query(Plan).all()
    plan_html = ""
    for plan in plans:
        total_return = plan.price * (plan.daily_return / 100) * plan.duration
        plan_html += f"""
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:10px 14px;margin:6px 0;border:1px solid rgba(255,255,255,0.04);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
            <div>
                <span style="color:#ffd700;font-size:13px;font-weight:600;">{plan.name}</span>
                <span style="color:rgba(255,255,255,0.3);font-size:11px;margin-left:8px;">{plan.duration} jours</span>
            </div>
            <div>
                <span style="color:rgba(255,255,255,0.4);font-size:12px;">{plan.daily_return}%/jour</span>
                <span style="color:#ffffff;font-size:14px;font-weight:700;margin-left:12px;">{plan.price} USDT</span>
                <span style="color:#4ade80;font-size:11px;margin-left:8px;">+{total_return:.2f}</span>
            </div>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <title>Info - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:750px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← {LANG[lang].get('info_back', 'Back to Dashboard')}</a>
            </div>
            
            <div style="text-align:center;margin-bottom:25px;">
                <div style="font-size:40px;margin-bottom:8px;">ℹ️</div>
                <h1 style="color:#ffffff;font-size:26px;font-weight:700;">{LANG[lang].get('info_title', 'About VestiCore')}</h1>
                <p style="color:rgba(255,255,255,0.4);font-size:14px;">{LANG[lang].get('info_subtitle', 'Everything you need to know')}</p>
            </div>
            
            <!-- SECTION 1 -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(255,215,0,0.05);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:8px;">💎 {LANG[lang].get('info_section1_title', 'What is VestiCore?')}</h3>
                <p style="color:rgba(255,255,255,0.7);font-size:14px;line-height:1.8;">{LANG[lang].get('info_section1_text', 'VestiCore is a digital finance platform that allows users to invest in rewarding plans and earn daily profits in USDT.')}</p>
            </div>
            
            <!-- SECTION 2 -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(255,215,0,0.05);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:8px;">⚙️ {LANG[lang].get('info_section2_title', 'How does it work?')}</h3>
                <div style="color:rgba(255,255,255,0.7);font-size:14px;line-height:2.2;">
                    <div>1️⃣ Créez votre compte gratuitement</div>
                    <div>2️⃣ Déposez des USDT sur votre portefeuille</div>
                    <div>3️⃣ Choisissez un plan d'investissement</div>
                    <div>4️⃣ Recevez des bénéfices chaque jour</div>
                    <div>5️⃣ Retirez vos gains à tout moment</div>
                </div>
            </div>
            
            <!-- SECTION 3: PLAN -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(255,215,0,0.05);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:8px;">📊 {LANG[lang].get('info_section5_title', 'Investment Plans')}</h3>
                {plan_html}
            </div>
            
            <!-- SECTION 4: SECURITE -->
            <div style="background:rgba(74,222,128,0.03);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(74,222,128,0.08);">
                <h3 style="color:#4ade80;font-size:16px;margin-bottom:8px;">🔒 {LANG[lang].get('info_section3_title', 'Security')}</h3>
                <p style="color:rgba(255,255,255,0.7);font-size:14px;line-height:1.8;">{LANG[lang].get('info_section3_text', 'VestiCore uses advanced technologies to secure your data and transactions: SSL encryption, secure authentication, KYC, and manual approval of withdrawals by the administrator.')}</p>
            </div>
            
            <!-- SECTION 5: REFERRAL -->
            <div style="background:rgba(255,215,0,0.03);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(255,215,0,0.08);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:8px;">🎁 {LANG[lang].get('info_section4_title', 'Referral Program')}</h3>
                <p style="color:rgba(255,255,255,0.7);font-size:14px;line-height:1.8;">{LANG[lang].get('info_section4_text', 'Invite your friends and earn 2% bonus on the deposits of your first 10 qualified investors.')}</p>
            </div>
            
            <!-- SECTION 6: FAQ -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:18px;margin-bottom:12px;border:1px solid rgba(255,255,255,0.04);">
                <h3 style="color:#ffffff;font-size:16px;margin-bottom:8px;">❓ FAQ - Questions fréquentes</h3>
                <div style="color:rgba(255,255,255,0.6);font-size:13px;line-height:2;">
                    <div><strong style="color:#ffffff;">Quel est le minimum de dépôt ?</strong> 10 USDT</div>
                    <div><strong style="color:#ffffff;">Quand puis-je retirer ?</strong> À tout moment, après approbation admin</div>
                    <div><strong style="color:#ffffff;">Y a-t-il des frais ?</strong> 3% sur les dépôts, 5% sur les retraits</div>
                    <div><strong style="color:#ffffff;">Comment gagner plus ?</strong> Parrainez des amis et choisissez des plans supérieurs</div>
                </div>
            </div>
            
            <div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:15px;">
                <p style="color:rgba(255,255,255,0.08);font-size:10px;">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</p>
            </div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# SETTINGS PAGE
# =====================

@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, db: Session = Depends(get_db), error: str = None, success: str = None):
    user = current_user(request, db)
    lang = get_lang(request)
    
    error_html = f'<div class="error-message">❌ {error}</div>' if error else ''
    success_html = f'<div class="success-message">✅ {success}</div>' if success else ''
    
    # Transactions
    deposits = db.query(Deposit).filter(Deposit.username == user.username).order_by(Deposit.date.desc()).limit(20).all()
    withdraws = db.query(Withdraw).filter(Withdraw.username == user.username).order_by(Withdraw.date.desc()).limit(20).all()
    
    tx_html = ""
    for d in deposits[:10]:
        tx_html += f"""
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
            <div>
                <span style="color:#4ade80;">💰 Dépôt</span>
                <span style="color:rgba(255,255,255,0.3);font-size:11px;margin-left:10px;">{d.date.strftime('%d/%m/%Y %H:%M')}</span>
            </div>
            <div>
                <span style="color:#ffffff;">+{d.net_amount:.2f} USDT</span>
                <span style="color:rgba(255,255,255,0.2);font-size:10px;margin-left:8px;">{d.status}</span>
            </div>
        </div>
        """
    
    for w in withdraws[:10]:
        tx_html += f"""
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
            <div>
                <span style="color:#fbbf24;">💸 Retrait</span>
                <span style="color:rgba(255,255,255,0.3);font-size:11px;margin-left:10px;">{w.date.strftime('%d/%m/%Y %H:%M')}</span>
            </div>
            <div>
                <span style="color:#ffffff;">-{w.amount:.2f} USDT</span>
                <span style="color:rgba(255,255,255,0.2);font-size:10px;margin-left:8px;">{w.status}</span>
            </div>
        </div>
        """
    
    if not tx_html:
        tx_html = f'<div style="color:rgba(255,255,255,0.2);text-align:center;padding:20px 0;">{LANG[lang].get("no_transactions", "No transactions")}</div>'
    
    # Earnings
    earnings = db.query(ActivityLog).filter(
        ActivityLog.username == user.username,
        ActivityLog.action.like("Benefis%")
    ).order_by(ActivityLog.date.desc()).limit(20).all()
    
    earnings_html = ""
    for e in earnings[:10]:
        amount = e.action.split(":")[-1].strip() if ":" in e.action else "0.00"
        earnings_html += f"""
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
            <div>
                <span style="color:#4ade80;">📈 {e.action[:30]}...</span>
                <span style="color:rgba(255,255,255,0.3);font-size:11px;margin-left:10px;">{e.date.strftime('%d/%m/%Y %H:%M')}</span>
            </div>
            <div>
                <span style="color:#4ade80;">+{amount} USDT</span>
            </div>
        </div>
        """
    
    if not earnings_html:
        earnings_html = f'<div style="color:rgba(255,255,255,0.2);text-align:center;padding:20px 0;">{LANG[lang].get("no_earnings", "No earnings")}</div>'
    
    # Sessions
    sessions_html = f"""
    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
        <div>
            <span style="color:rgba(255,255,255,0.7);font-size:13px;">{LANG[lang].get('current_session', 'Current session')}</span>
            <span style="color:rgba(255,255,255,0.2);font-size:11px;margin-left:10px;">{request.client.host if request.client else '127.0.0.1'}</span>
        </div>
        <div>
            <span style="color:#4ade80;font-size:11px;">✅ {LANG[lang].get('active', 'Active')}</span>
        </div>
    </div>
    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
        <div>
            <span style="color:rgba(255,255,255,0.4);font-size:13px;">{LANG[lang].get('last_login', 'Last login')}</span>
        </div>
        <div>
            <span style="color:rgba(255,255,255,0.2);font-size:11px;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
        </div>
    </div>
    """
    
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('settings', 'Settings')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:750px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">{LANG[lang].get('settings', 'Settings')}</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← Retour</a>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;margin-bottom:20px;">⚙️ {LANG[lang].get('settings', 'Settings')}</div>
            
            {success_html}
            {error_html}
            
            <!-- CHANGER MODPAS -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.04);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:12px;">🔐 {LANG[lang].get('change_password', 'Change Password')}</h3>
                <form method="post" action="/settings/change-password">
                    <div class="form-group" style="margin-bottom:10px;">
                        <input type="password" name="current_password" placeholder="{LANG[lang].get('current_password', 'Current password')}" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;" required>
                    </div>
                    <div class="form-group" style="margin-bottom:10px;">
                        <input type="password" name="new_password" placeholder="{LANG[lang].get('new_password', 'New password')}" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;" required>
                    </div>
                    <div class="form-group" style="margin-bottom:10px;">
                        <input type="password" name="confirm_password" placeholder="{LANG[lang].get('confirm_password', 'Confirm password')}" style="width:100%;padding:12px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;color:#ffffff;font-size:14px;outline:none;" required>
                    </div>
                    <button type="submit" class="btn btn-secondary" style="width:100%;padding:12px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.12);border-radius:8px;color:#ffd700;font-weight:700;font-size:14px;cursor:pointer;">{LANG[lang].get('change_password', 'Change password')}</button>
                </form>
            </div>
            
            <!-- SECURITE -->
            <div style="background:rgba(59,130,246,0.03);border-radius:12px;padding:20px;margin-bottom:15px;border:1px solid rgba(59,130,246,0.08);">
                <h3 style="color:#3b82f6;font-size:16px;margin-bottom:12px;">🔐 {LANG[lang].get('security', 'Security')}</h3>
                
                <!-- 2FA -->
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
                    <div>
                        <span style="color:#ffffff;font-size:14px;">{LANG[lang].get('two_factor', 'Two-Factor Authentication (2FA)')}</span>
                        <span style="color:rgba(255,255,255,0.3);font-size:11px;display:block;">{LANG[lang].get('enable_2fa', 'Activate 2FA for more security')}</span>
                    </div>
                    <button onclick="showModal('Fonctionnalité 2FA en cours de développement', '🔑 2FA', 'info')" style="padding:8px 20px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.1);border-radius:8px;color:#ffd700;font-weight:600;font-size:12px;cursor:pointer;">{LANG[lang].get('enable_2fa', 'Enable')}</button>
                </div>
                
                <!-- Sessions -->
                <div style="margin-top:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <span style="color:#ffffff;font-size:14px;">{LANG[lang].get('session_management', 'Session Management')}</span>
                        <button onclick="showModal('Vous êtes déconnecté de tous les appareils', '🚪 Déconnexion', 'info')" style="padding:6px 16px;background:rgba(255,107,107,0.08);border:1px solid rgba(255,107,107,0.1);border-radius:6px;color:#ff6b6b;font-weight:600;font-size:11px;cursor:pointer;">{LANG[lang].get('logout_all', 'Logout All')}</button>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:8px 12px;">
                        {sessions_html}
                    </div>
                </div>
            </div>
            
            <!-- TRANSACTIONS -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.04);">
                <h3 style="color:#4ade80;font-size:16px;margin-bottom:12px;">📊 {LANG[lang].get('transactions_history', 'Transactions History')}</h3>
                <div style="max-height:250px;overflow-y:auto;">
                    {tx_html}
                </div>
            </div>
            
            <!-- EARNINGS -->
            <div style="background:rgba(255,255,255,0.02);border-radius:12px;padding:20px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.04);">
                <h3 style="color:#ffd700;font-size:16px;margin-bottom:12px;">📈 {LANG[lang].get('earnings_history', 'Earnings History')}</h3>
                <div style="max-height:250px;overflow-y:auto;">
                    {earnings_html}
                </div>
            </div>
            
            <div style="text-align:center;margin-top:15px;border-top:1px solid rgba(255,255,255,0.03);padding-top:15px;">
                <p style="color:rgba(255,255,255,0.08);font-size:10px;">{LANG[lang].get('footer', '© 2026 VestiCore. All rights reserved.')}</p>
            </div>
        </div>
        {get_modal_html()}
    </body>
    </html>
    """

# =====================
# CHANGE PASSWORD
# =====================

@app.post("/settings/change-password")
def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)
    
    if not verify_password(current_password, user.password):
        return RedirectResponse(url="/settings?error=Mot+de+passe+actuel+incorrect", status_code=303)
    
    if new_password != confirm_password:
        return RedirectResponse(url="/settings?error=Les+mots+de+passe+ne+correspondent+pas", status_code=303)
    
    if new_password == current_password:
        return RedirectResponse(url="/settings?error=Le+nouveau+mot+de+passe+doit+être+différent", status_code=303)
    
    user.password = hash_password(new_password)
    db.commit()
    add_log(db, user.username, "Modpas chanje")
    
    return RedirectResponse(url="/settings?success=Mot+de+passe+changé+avec+succès", status_code=303)

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
        <title>{LANG[lang].get('referral_title', 'Referral')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:550px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← {LANG[lang].get('referral_back', 'Back')}</a>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">👥 {LANG[lang].get('referral_title', 'Referral')}</div>
            
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
    tickets = db.query(Ticket).all()
    pending_deposits = db.query(Deposit).filter(Deposit.status == "pending").all()
    pending_withdraws = db.query(Withdraw).filter(Withdraw.status == "pending").all()
    pending_kyc = db.query(User).filter(User.kyc_status == "pending").all()
    
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
    
    kyc_html = ""
    for k in pending_kyc:
        kyc_html += f"""
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;margin:6px 0;border:1px solid rgba(255,255,255,0.03);">
            <p style="color:#ffffff;font-size:13px;"><strong>{k.username}</strong> - KYC en attente</p>
            <div style="display:flex;gap:6px;margin-top:6px;">
                <form method="post" action="/admin/approve-kyc/{k.id}" style="display:inline;">
                    <button style="background:#4ade80;border:none;padding:6px 14px;border-radius:6px;color:#0a0e27;font-weight:700;cursor:pointer;font-size:12px;">✅ Approuver</button>
                </form>
                <form method="post" action="/admin/reject-kyc/{k.id}" style="display:inline;">
                    <button style="background:#ff6b6b;border:none;padding:6px 14px;border-radius:6px;color:#ffffff;font-weight:700;cursor:pointer;font-size:12px;">❌ Rejeter</button>
                </form>
            </div>
        </div>
        """
    
    tickets_html = ""
    for t in tickets[:5]:
        status_class = "open" if t.status == "open" else "closed" if t.status == "closed" else "waiting"
        tickets_html += f"""
        <div style="background:rgba(255,255,255,0.02);border-radius:8px;padding:12px;margin:6px 0;border:1px solid rgba(255,255,255,0.03);">
            <div>
                <span style="color:#ffffff;font-size:13px;font-weight:600;">{t.subject}</span>
                <span style="font-size:10px;font-weight:600;padding:2px 10px;border-radius:10px;display:inline-block;background:rgba(74,222,128,0.12);color:#4ade80;">{t.status.upper()}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;">
                <span style="color:rgba(255,255,255,0.3);font-size:10px;">{t.username}</span>
                <span style="color:rgba(255,255,255,0.2);font-size:10px;">{t.created_at.strftime('%d/%m %H:%M')}</span>
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
        <div class="container" style="max-width:700px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond" style="width:40px;height:40px;">
                        {LOGO_SVG}
                    </div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">ADMIN</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">{LANG[lang].get('admin_back', '← Back')}</a>
            </div>
            
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin-bottom:15px;">
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">USERS</p>
                    <p style="color:#ffffff;font-size:20px;font-weight:700;">{len(users)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">DEPOSITS</p>
                    <p style="color:#4ade80;font-size:20px;font-weight:700;">{len(deposits)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">WITHDRAWS</p>
                    <p style="color:#fbbf24;font-size:20px;font-weight:700;">{len(withdraws)}</p>
                </div>
                <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;text-align:center;">
                    <p style="color:rgba(255,255,255,0.3);font-size:9px;">TICKETS</p>
                    <p style="color:#a855f7;font-size:20px;font-weight:700;">{len(tickets)}</p>
                </div>
            </div>
            
            <h3 style="color:#ffd700;font-size:14px;">📋 KYC En attente</h3>
            {kyc_html if kyc_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>Aucune demande KYC</p>"}
            
            <h3 style="color:#ffd700;font-size:14px;margin-top:12px;">⏳ Dépôts en attente</h3>
            {deposit_html if deposit_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>{no_pending}</p>"}
            
            <h3 style="color:#ffd700;font-size:14px;margin-top:12px;">⏳ Retraits en attente</h3>
            {withdraw_html if withdraw_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>{no_pending}</p>"}
            
            <h3 style="color:#ffd700;font-size:14px;margin-top:12px;">🎫 Tickets récents</h3>
            {tickets_html if tickets_html else f"<p style='color:rgba(255,255,255,0.2);font-size:12px;'>Aucun ticket</p>"}
            
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
# ADMIN APPROVE KYC
# =====================

@app.post("/admin/approve-kyc/{user_id}")
def approve_kyc(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Itilizatè pa jwenn")
    user.kyc_status = "verified"
    add_log(db, user.username, f"KYC apwouve pa admin")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/reject-kyc/{user_id}")
def reject_kyc(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin_user(request, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Itilizatè pa jwenn")
    user.kyc_status = "rejected"
    add_log(db, user.username, f"KYC rejete pa admin")
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

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
# BACKUP BAZ DONE
# =====================

@app.get("/admin/backup")
def admin_backup(request: Request, db: Session = Depends(get_db)):
    admin_user(request, db)
    
    users = db.query(User).all()
    plans = db.query(Plan).all()
    user_plans = db.query(UserPlan).all()
    deposits = db.query(Deposit).all()
    withdraws = db.query(Withdraw).all()
    referrals = db.query(Referral).all()
    logs = db.query(ActivityLog).all()
    
    data = {
        "users": [{"id": u.id, "username": u.username, "balance": u.balance, "is_admin": u.is_admin, "referral_code": u.referral_code, "kyc_status": u.kyc_status, "created_at": u.created_at.isoformat()} for u in users],
        "plans": [{"id": p.id, "name": p.name, "price": p.price, "duration": p.duration, "daily_return": p.daily_return} for p in plans],
        "user_plans": [{"id": up.id, "user_id": up.user_id, "plan_id": up.plan_id, "amount": up.amount, "status": up.status, "start_date": up.start_date.isoformat(), "total_returned": up.total_returned} for up in user_plans],
        "deposits": [{"id": d.id, "username": d.username, "amount": d.amount, "fee": d.fee, "net_amount": d.net_amount, "txid": d.txid, "status": d.status, "date": d.date.isoformat()} for d in deposits],
        "withdraws": [{"id": w.id, "username": w.username, "amount": w.amount, "fee": w.fee, "net_amount": w.net_amount, "wallet": w.wallet, "status": w.status, "date": w.date.isoformat()} for w in withdraws],
        "referrals": [{"id": r.id, "referrer": r.referrer, "invited_user": r.invited_user, "has_invested": r.has_invested, "bonus_amount": r.bonus_amount} for r in referrals],
        "logs": [{"id": l.id, "username": l.username, "action": l.action, "date": l.date.isoformat()} for l in logs]
    }
    
    json_data = json.dumps(data, indent=2)
    encoded = base64.b64encode(json_data.encode()).decode()
    
    return JSONResponse(content={"backup": encoded, "size": len(json_data)})

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
