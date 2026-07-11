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
