from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime
import os

# =====================
# KONFIGIRASYON
# =====================

app = FastAPI(
    title="Envesti USDT TRC20",
    description="Platfòm envestisman ak depo/retrè USDT",
    version="1.0"
)

DATABASE_URL = "sqlite:///./investi.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
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

# Mete wallet TRC20 ou la pita
USDT_TRON_ADDRESS = os.getenv(
    "USDT_TRON_ADDRESS",
    "METE_WALLET_TRON_LA"
)


# =====================
# DATABASE MODELS
# =====================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    balance = Column(Float, default=0)
    is_admin = Column(Integer, default=0)


class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    amount = Column(Float)
    txid = Column(String)
    status = Column(String, default="pending")
    date = Column(String, default=str(datetime.now()))


class Withdraw(Base):
    __tablename__ = "withdraws"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    amount = Column(Float)
    wallet = Column(String)
    status = Column(String, default="pending")
    date = Column(String, default=str(datetime.now()))


Base.metadata.create_all(bind=engine)


# =====================
# DATABASE CONNECTION
# =====================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================
# PASSWORD
# =====================

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


# =====================
# HOME
# =====================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Envesti USDT TRC20</h1>
    <p>Sistèm nan ap mache.</p>
    """
# =====================
# REGISTER
# =====================

@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_exist = db.query(User).filter(
        User.username == username
    ).first()

    if user_exist:
        raise HTTPException(
            status_code=400,
            detail="Non itilizatè sa deja egziste"
        )

    new_user = User(
        username=username,
        password=hash_password(password),
        balance=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Kont kreye avèk siksè",
        "username": username
    }


# =====================
# LOGIN
# =====================

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Itilizatè pa jwenn"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Modpas pa bon"
        )

    return {
        "message": "Login reyisi",
        "username": user.username,
        "balance": user.balance
    }


# =====================
# BALANCE
# =====================

@app.get("/balance/{username}")
def get_balance(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kont pa jwenn"
        )

    return {
        "username": user.username,
        "balance_usdt": user.balance
    }
# =====================
# DEPO USDT TRC20
# =====================

@app.get("/deposit-info")
def deposit_info():
    return {
        "network": "TRC20 (TRON)",
        "currency": "USDT",
        "wallet_address": USDT_TRON_ADDRESS,
        "instruction": "Voye USDT TRC20 sou adrès sa a epi mete TXID tranzaksyon an."
    }


@app.post("/deposit")
def create_deposit(
    username: str = Form(...),
    amount: float = Form(...),
    txid: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kont pa jwenn"
        )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Montan an pa valab"
        )

    deposit = Deposit(
        username=username,
        amount=amount,
        txid=txid,
        status="pending"
    )

    db.add(deposit)
    db.commit()
    db.refresh(deposit)

    return {
        "message": "Depo resevwa, li sou verifikasyon",
        "amount": amount,
        "txid": txid,
        "status": "pending"
    }


# =====================
# LISTE DEPO ITILIZATE A
# =====================

@app.get("/deposits/{username}")
def get_deposits(
    username: str,
    db: Session = Depends(get_db)
):

    deposits = db.query(Deposit).filter(
        Deposit.username == username
    ).all()

    return deposits
# =====================
# RETRÈ USDT TRC20
# =====================

@app.post("/withdraw")
def create_withdraw(
    username: str = Form(...),
    amount: float = Form(...),
    wallet: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kont pa jwenn"
        )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Montan pa valab"
        )

    if user.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Balans pa ase"
        )

    withdraw = Withdraw(
        username=username,
        amount=amount,
        wallet=wallet,
        status="pending"
    )

    db.add(withdraw)
    db.commit()
    db.refresh(withdraw)

    return {
        "message": "Demann retrè voye bay admin",
        "amount": amount,
        "wallet": wallet,
        "status": "pending"
    }


# =====================
# ADMIN WÈ RETRÈ YO
# =====================

@app.get("/admin/withdraws")
def admin_withdraws(
    db: Session = Depends(get_db)
):

    withdraws = db.query(Withdraw).filter(
        Withdraw.status == "pending"
    ).all()

    return withdraws


# =====================
# ADMIN APWOUVE RETRÈ
# =====================

@app.post("/admin/approve-withdraw/{withdraw_id}")
def approve_withdraw(
    withdraw_id: int,
    db: Session = Depends(get_db)
):

    withdraw = db.query(Withdraw).filter(
        Withdraw.id == withdraw_id
    ).first()

    if not withdraw:
        raise HTTPException(
            status_code=404,
            detail="Retrè pa jwenn"
        )

    user = db.query(User).filter(
        User.username == withdraw.username
    ).first()

    if user.balance < withdraw.amount:
        raise HTTPException(
            status_code=400,
            detail="Balans itilizatè a pa ase"
        )

    user.balance -= withdraw.amount
    withdraw.status = "approved"

    db.commit()

    return {
        "message": "Retrè apwouve",
        "amount": withdraw.amount
    }


# =====================
# ADMIN REFIZE RETRÈ
# =====================

@app.post("/admin/reject-withdraw/{withdraw_id}")
def reject_withdraw(
    withdraw_id: int,
    db: Session = Depends(get_db)
):

    withdraw = db.query(Withdraw).filter(
        Withdraw.id == withdraw_id
    ).first()

    if not withdraw:
        raise HTTPException(
            status_code=404,
            detail="Retrè pa jwenn"
        )

    withdraw.status = "rejected"

    db.commit()

    return {
        "message": "Retrè refize"
    }
# =====================
# CREATE ADMIN (PREMYE FWA)
# =====================

@app.post("/create-admin")
def create_admin(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    admin_exist = db.query(User).filter(
        User.is_admin == 1
    ).first()

    if admin_exist:
        raise HTTPException(
            status_code=400,
            detail="Gen yon admin deja"
        )

    admin = User(
        username=username,
        password=hash_password(password),
        balance=0,
        is_admin=1
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Admin kreye avèk siksè"
    }


# =====================
# ADMIN WÈ DEPO PENDING YO
# =====================

@app.get("/admin/deposits")
def admin_deposits(
    db: Session = Depends(get_db)
):

    deposits = db.query(Deposit).filter(
        Deposit.status == "pending"
    ).all()

    return deposits


# =====================
# ADMIN VALIDE DEPO
# =====================

@app.post("/admin/approve-deposit/{deposit_id}")
def approve_deposit(
    deposit_id: int,
    db: Session = Depends(get_db)
):

    deposit = db.query(Deposit).filter(
        Deposit.id == deposit_id
    ).first()

    if not deposit:
        raise HTTPException(
            status_code=404,
            detail="Depo pa jwenn"
        )

    user = db.query(User).filter(
        User.username == deposit.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Itilizatè pa jwenn"
        )

    user.balance += deposit.amount
    deposit.status = "approved"

    db.commit()

    return {
        "message": "Depo apwouve",
        "amount_added": deposit.amount
    }


# =====================
# API STATUS
# =====================

@app.get("/status")
def status():
    return {
        "status": "online",
        "platform": "Envesti USDT TRC20"
    }
