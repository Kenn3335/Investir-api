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
            Plan(name="Starter Basic", price=10, duration=30, daily_return=0.50, description="Plan Starter debaz - 30 jou"),
            Plan(name="Starter Plus", price=25, duration=30, daily_return=0.60, description="Plan Starter Plus - 30 jou"),
            Plan(name="Standard Basic", price=50, duration=60, daily_return=0.70, description="Plan Standard debaz - 60 jou"),
            Plan(name="Standard Plus", price=100, duration=60, daily_return=0.80, description="Plan Standard Plus - 60 jou"),
            Plan(name="Premium Basic", price=200, duration=90, daily_return=0.90, description="Plan Premium debaz - 90 jou"),
            Plan(name="Premium Plus", price=350, duration=90, daily_return=1.00, description="Plan Premium Plus - 90 jou"),
            Plan(name="Premium Pro", price=500, duration=90, daily_return=1.10, description="Plan Premium Pro - 90 jou"),
            Plan(name="VIP Basic", price=750, duration=120, daily_return=1.20, description="Plan VIP debaz - 120 jou"),
            Plan(name="VIP Plus", price=1000, duration=120, daily_return=1.30, description="Plan VIP Plus - 120 jou"),
            Plan(name="VIP Pro", price=2000, duration=120, daily_return=1.50, description="Plan VIP Pro - 120 jou")
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
    
    .logo-diamond {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #ffd700, #f0a500);
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(255,215,0,0.2);
    }
    .logo-diamond span {
        font-size: 18px;
        font-weight: 900;
        color: #0a0e27;
    }
    .logo-text {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .logo-text span { color: #ffd700; }
    
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        flex-wrap: wrap;
        gap: 10px;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .header-right {
        display: flex;
        align-items: center;
        gap: 15px;
        flex-wrap: wrap;
    }
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
    .user-info .name {
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
    }
    .user-info .id {
        color: rgba(255,255,255,0.3);
        font-size: 10px;
    }
    .user-plan-badge {
        background: rgba(255,215,0,0.12);
        color: #ffd700;
        font-size: 9px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 10px;
        border: 1px solid rgba(255,215,0,0.1);
    }
    .notif-bell {
        color: rgba(255,255,255,0.4);
        font-size: 18px;
        position: relative;
        cursor: pointer;
    }
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
    }
    .nav a:hover {
        color: #ffffff;
        background: rgba(255,255,255,0.05);
    }
    .nav a.active {
        color: #ffd700;
        background: rgba(255,215,0,0.08);
    }
    
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
    .dash-stat .label {
        color: rgba(255,255,255,0.3);
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dash-stat .value {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        margin-top: 4px;
    }
    .dash-stat .value span { color: #ffd700; font-size: 14px; }
    .dash-stat .sub {
        color: rgba(255,255,255,0.25);
        font-size: 11px;
        margin-top: 2px;
    }
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
    .actions .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255,215,0,0.2);
    }
    .actions .btn-secondary {
        background: rgba(255,255,255,0.06);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .actions .btn-secondary:hover {
        background: rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(255,255,255,0.05);
    }
    .btn-danger {
        background: linear-gradient(135deg, #ff6b6b, #ee4444);
        color: #fff;
    }
    .btn-danger:hover {
        box-shadow: 0 10px 30px rgba(255,107,107,0.3);
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
    .card:hover {
        background: rgba(255,255,255,0.04);
        transform: translateY(-2px);
    }
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
    .section h4 {
        color: #ffffff;
        font-size: 14px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section h4 span { color: rgba(255,255,255,0.2); font-size: 12px; font-weight: 400; }
    
    .plan-card {
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        padding: 14px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .plan-card h4 { color: #ffd700; font-size: 14px; }
    .plan-card p { color: rgba(255,255,255,0.4); font-size: 11px; margin: 2px 0; }
    .plan-card .return { color: #4ade80; font-weight: 600; }
    .plan-card .plan-price { color: #ffffff; font-size: 16px; font-weight: 700; text-align: right; }
    .plan-card .plan-price small { color: rgba(255,255,255,0.3); font-size: 10px; font-weight: 400; }
    .plan-card .btn-sm {
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
    .plan-card .btn-sm:hover {
        transform: scale(1.05);
    }
    
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
    
    .news-item {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.02);
    }
    .news-item .title { color: #ffffff; font-size: 12px; font-weight: 500; }
    .news-item .date { color: rgba(255,255,255,0.2); font-size: 10px; }
    
    .promo-item {
        background: rgba(255,215,0,0.04);
        border-radius: 8px;
        padding: 10px 12px;
        margin: 6px 0;
        border: 1px solid rgba(255,215,0,0.06);
    }
    .promo-item .title { color: #ffd700; font-size: 12px; font-weight: 600; }
    .promo-item .desc { color: rgba(255,255,255,0.4); font-size: 11px; }
    
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
    .dropdown a:hover {
        background: rgba(255,255,255,0.05);
        color: #ffffff;
    }
    .dropdown a .icon { font-size: 16px; }
    .dropdown .divider {
        border-top: 1px solid rgba(255,255,255,0.05);
        margin: 6px 12px;
    }
    .dropdown .logout { color: #ff6b6b; }
    .dropdown .logout:hover { background: rgba(255,107,107,0.05); }
    
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
    .modal.active { display: flex; }
    .modal-content {
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
    .modal-content h3 { color: #ffffff; font-size: 20px; margin-bottom: 10px; }
    .modal-content p { color: rgba(255,255,255,0.5); font-size: 14px; line-height: 1.6; margin-bottom: 20px; }
    .modal-content .btn { width: auto; display: inline-block; padding: 10px 30px; background: linear-gradient(135deg, #ffd700, #f0a500); border: none; border-radius: 8px; color: #0a0e27; font-weight: 700; cursor: pointer; }
    .modal-content .icon-big { font-size: 48px; margin-bottom: 15px; display: block; }
    
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
    
    .kyc-status {
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    .kyc-status.pending { background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.15); color: #fbbf24; }
    .kyc-status.verified { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.15); color: #4ade80; }
    .kyc-status.rejected { background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.15); color: #ff6b6b; }
    .kyc-status.unverified { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); color: rgba(255,255,255,0.4); }
    
    .ticket-item {
        background: rgba(255,255,255,0.02);
        padding: 12px 14px;
        border-radius: 8px;
        margin: 6px 0;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .ticket-item .ticket-title { color: #ffffff; font-size: 13px; font-weight: 600; }
    .ticket-item .ticket-status { font-size: 10px; font-weight: 600; padding: 2px 10px; border-radius: 10px; display: inline-block; }
    .ticket-item .ticket-status.open { background: rgba(74,222,128,0.12); color: #4ade80; }
    .ticket-item .ticket-status.closed { background: rgba(255,107,107,0.12); color: #ff6b6b; }
    .ticket-item .ticket-status.waiting { background: rgba(251,191,36,0.12); color: #fbbf24; }
    .ticket-item .ticket-date { color: rgba(255,255,255,0.2); font-size: 10px; }
    
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

function toggleDropdown() {
    document.getElementById('userDropdown').classList.toggle('active');
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

function showProfile() {
    document.getElementById('profileSection').scrollIntoView({ behavior: 'smooth' });
}

function showPlans() {
    document.getElementById('plansSection').scrollIntoView({ behavior: 'smooth' });
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
        "kyc_title": "Vérification KYC",
        "kyc_pending": "En attente de vérification",
        "kyc_verified": "✅ Vérifié",
        "kyc_rejected": "❌ Rejeté",
        "kyc_unverified": "Non vérifié",
        "kyc_submit": "Soumettre pour vérification",
        "tickets_title": "Mes tickets",
        "ticket_new": "Nouveau ticket",
        "ticket_open": "Ouvert",
        "ticket_closed": "Fermé",
        "ticket_waiting": "En attente"
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
        "kyc_title": "KYC Verification",
        "kyc_pending": "Pending verification",
        "kyc_verified": "✅ Verified",
        "kyc_rejected": "❌ Rejected",
        "kyc_unverified": "Unverified",
        "kyc_submit": "Submit for verification",
        "tickets_title": "My Tickets",
        "ticket_new": "New ticket",
        "ticket_open": "Open",
        "ticket_closed": "Closed",
        "ticket_waiting": "Waiting"
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
        "kyc_title": "Verificación KYC",
        "kyc_pending": "Pendiente de verificación",
        "kyc_verified": "✅ Verificado",
        "kyc_rejected": "❌ Rechazado",
        "kyc_unverified": "No verificado",
        "kyc_submit": "Enviar para verificación",
        "tickets_title": "Mis tickets",
        "ticket_new": "Nuevo ticket",
        "ticket_open": "Abierto",
        "ticket_closed": "Cerrado",
        "ticket_waiting": "En espera"
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
    # KYC
    kyc_status = Column(String, default="unverified")  # unverified, pending, verified, rejected
    kyc_document = Column(String, nullable=True)
    kyc_submitted_at = Column(DateTime, nullable=True)
    # Profile
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

# =====================
# TICKET SYSTEM
# =====================

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    subject = Column(String)
    message = Column(Text)
    status = Column(String, default="open")  # open, waiting, closed
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
        <div class="container" style="max-width:600px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond"><span>V</span></div>
                    <div>
                        <div style="color:#ffffff;font-size:22px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
                <div style="display:flex;gap:6px;">
                    <a href="/set-lang/fr" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:12px;padding:4px 8px;border-radius:4px;">FR</a>
                    <a href="/set-lang/en" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:12px;padding:4px 8px;border-radius:4px;">EN</a>
                    <a href="/set-lang/es" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:12px;padding:4px 8px;border-radius:4px;">ES</a>
                </div>
            </div>
            
            <div style="text-align:center;margin:20px 0 30px;">
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
# REGISTER
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, ref: str = None):
    lang = get_lang(request)
    ref_value = f'value="{ref}"' if ref else ''
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('register_title', 'Create account')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:500px;">
            <div style="display:flex;justify-content:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond"><span>V</span></div>
                    <div>
                        <div style="color:#ffffff;font-size:22px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('register_title', 'Create your account')}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:13px;text-align:center;margin-bottom:22px;">{LANG[lang].get('register_sub', 'Start your investment journey')}</div>
            
            <form method="post">
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
    return RedirectResponse(url="/login", status_code=303)

# =====================
# LOGIN - AVEC ERÈ RESTE SOU MENM PAJ
# =====================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None):
    lang = get_lang(request)
    error_html = f'<div class="error-message">❌ {error}</div>' if error else ''
    return f"""
    <html>
    <head>
        <title>{LANG[lang].get('login_title', 'Login')} - VestiCore</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {STYLE}
    </head>
    <body>
        <div class="container" style="max-width:500px;">
            <div style="display:flex;justify-content:center;margin-bottom:20px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="logo-diamond"><span>V</span></div>
                    <div>
                        <div style="color:#ffffff;font-size:22px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('login_title', 'Welcome back')}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:13px;text-align:center;margin-bottom:22px;">{LANG[lang].get('login_sub', 'Login to access your space')}</div>
            
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
# DASHBOARD - AVEC PLAN AK PROFIL
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
    
    notifications = db.query(Notification).filter(Notification.username == user.username, Notification.read == False).all()
    notif_count = len(notifications)
    
    logs = db.query(ActivityLog).filter(ActivityLog.username == user.username).order_by(ActivityLog.date.desc()).limit(10).all()
    
    total_investment = db.query(UserPlan).filter(UserPlan.user_id == user.id, UserPlan.status == "active").first()
    total_investment_amount = total_investment.amount if total_investment else 0
    
    pending_withdraw = db.query(Withdraw).filter(Withdraw.username == user.username, Withdraw.status == "pending").all()
    pending_withdraw_amount = sum(w.amount for w in pending_withdraw)
    
    active_plan_name = active_plan_info["plan"].name if active_plan_info else "Aucun"
    
    # KYC status
    kyc_status_text = {
        "unverified": LANG[lang].get('kyc_unverified', 'Unverified'),
        "pending": LANG[lang].get('kyc_pending', 'Pending verification'),
        "verified": LANG[lang].get('kyc_verified', '✅ Verified'),
        "rejected": LANG[lang].get('kyc_rejected', '❌ Rejected')
    }.get(user.kyc_status, 'Unverified')
    
    kyc_class = {
        "unverified": "unverified",
        "pending": "pending",
        "verified": "verified",
        "rejected": "rejected"
    }.get(user.kyc_status, "unverified")
    
    # Profile info
    profile_items = f"""
    <div class="profile-item"><div class="label">Nom d'utilisateur</div><div class="value">{user.username}</div></div>
    <div class="profile-item"><div class="label">ID</div><div class="value gold">{user.user_id_display or 'VC000001'}</div></div>
    <div class="profile-item"><div class="label">Plan actif</div><div class="value">{active_plan_name}</div></div>
    <div class="profile-item"><div class="label">Solde</div><div class="value gold">{user.balance:.2f} USDT</div></div>
    <div class="profile-item"><div class="label">Bonus de parrainage</div><div class="value">{total_bonus:.2f} USDT</div></div>
    <div class="profile-item"><div class="label">Membres depuis</div><div class="value">{user.created_at.strftime('%d/%m/%Y')}</div></div>
    """
    
    # Plans
    plan_html = ""
    for plan in plans:
        total_return = plan.price * (plan.daily_return / 100) * plan.duration
        plan_html += f"""
        <div class="plan-card">
            <div>
                <h4>{plan.name}</h4>
                <p>{plan.description}</p>
                <p>⏳ {plan.duration} jours • <span class="return">📈 {plan.daily_return}% / jour</span></p>
                <p style="color:rgba(255,255,255,0.2);font-size:10px;">💎 Total: +{total_return:.2f} USDT</p>
            </div>
            <div class="plan-price">
                {plan.price} <small>USDT</small>
                <br>
                <button onclick="acheterPlan({plan.id})" class="btn-sm">{LANG[lang].get('dashboard_buy', 'Buy')}</button>
            </div>
        </div>
        """
    
    # History
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
                    <div class="logo-diamond"><span>V</span></div>
                    <div class="logo-text">Vesti<span>Core</span></div>
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
                    <!-- Dropdown -->
                    <div id="userDropdown" class="dropdown">
                        <a href="#" onclick="showProfile(); toggleDropdown(); return false;"><span class="icon">👤</span> {LANG[lang].get('my_profile', 'My Profile')}</a>
                        <a href="#" onclick="showPlans(); toggleDropdown(); return false;"><span class="icon">📊</span> {LANG[lang].get('dashboard_plans', 'Plans')}</a>
                        <a href="#"><span class="icon">🔐</span> {LANG[lang].get('security', 'Security')}</a>
                        <a href="#"><span class="icon">⚙️</span> {LANG[lang].get('settings', 'Settings')}</a>
                        <div class="divider"></div>
                        <a href="/logout" class="logout"><span class="icon">🚪</span> {LANG[lang].get('logout', 'Logout')}</a>
                    </div>
                </div>
            </div>
            
            <!-- NAV -->
            <div class="nav">
                <a href="/dashboard" class="active">🏠 {LANG[lang].get('home', 'Home')}</a>
                <a href="#" onclick="showPlans(); return false;">💼 {LANG[lang].get('investment', 'Investment')}</a>
                <a href="/deposit-page">💳 {LANG[lang].get('wallet', 'Wallet')}</a>
                <a href="/referral">👥 {LANG[lang].get('referral', 'Referral')}</a>
                <a href="#" onclick="showProfile(); return false;">👤 {LANG[lang].get('my_profile', 'Profile')}</a>
                <a href="#">📚 {LANG[lang].get('academy', 'Academy')}</a>
                <a href="#">🛠 {LANG[lang].get('tools', 'Tools')}</a>
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
                    <div class="desc">Investissez 2000 USDT et gagnez 1.50% par jour pendant 120 jours</div>
                </div>
            </div>
            
            <!-- PLANS SECTION -->
            <div id="plansSection" class="section">
                <h4>💼 {LANG[lang].get('dashboard_plans', 'Investment Plans')}</h4>
                {plan_html}
            </div>
            
            <!-- PROFILE SECTION -->
            <div id="profileSection" class="section" style="margin-top:15px;">
                <h4>👤 {LANG[lang].get('my_profile', 'My Profile')}</h4>
                <div class="profile-info">
                    {profile_items}
                </div>
                
                <!-- KYC -->
                <div style="margin-top:12px;border-top:1px solid rgba(255,255,255,0.03);padding-top:12px;">
                    <h4 style="color:#ffffff;font-size:13px;">🪪 {LANG[lang].get('kyc_title', 'KYC Verification')}</h4>
                    <div class="kyc-status {kyc_class}">
                        <strong>Status:</strong> {kyc_status_text}
                    </div>
                    {f'<a href="#" onclick="showModal(\'Votre demande KYC a été soumise. Admin va vérifier.\', \'📋 KYC Soumis\', \'info\')" class="btn btn-secondary" style="display:inline-block;padding:8px 20px;font-size:12px;text-decoration:none;color:#fff;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);border-radius:8px;cursor:pointer;">{LANG[lang].get("kyc_submit", "Submit for verification")}</a>' if user.kyc_status in ['unverified', 'rejected'] else ''}
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
        
        {get_modal_html()}
    </body>
    </html>
    """

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
                    <div class="logo-diamond"><span>V</span></div>
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
    add_log(db, user.username, f"Demann retrè {amount} USDT voye")
    db.commit()
    
    return JSONResponse(content={"success": True, "message": LANG[get_lang(request)].get('withdraw_success', 'Withdrawal request sent successfully!')})

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
                    <div class="logo-diamond"><span>V</span></div>
                    <div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">Vesti<span style="color:#ffd700;">Core</span></div>
                        <div style="color:rgba(255,255,255,0.2);font-size:9px;letter-spacing:3px;">FINANCE & REWARDS</div>
                    </div>
                </div>
                <a href="/dashboard" style="color:rgba(255,255,255,0.3);text-decoration:none;font-size:13px;">← {LANG[lang].get('referral_back', 'Back')}</a>
            </div>
            
            <div style="color:#ffffff;font-size:22px;font-weight:600;text-align:center;">{LANG[lang].get('referral_title', '👥 Referral')}</div>
            
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
        <div class="ticket-item">
            <div>
                <span class="ticket-title">{t.subject}</span>
                <span class="ticket-status {status_class}">{t.status.upper()}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;">
                <span style="color:rgba(255,255,255,0.3);font-size:10px;">{t.username}</span>
                <span class="ticket-date">{t.created_at.strftime('%d/%m %H:%M')}</span>
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
                    <div class="logo-diamond"><span>V</span></div>
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
