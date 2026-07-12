from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime
import os


# =====================
# KONFIGIRASYON
# =====================

app = FastAPI(
    title="VestiCore",
    description="Platfòm envestisman USDT TRC20",
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


USDT_TRON_ADDRESS = os.getenv(
    "USDT_TRON_ADDRESS",
    "METE_WALLET_TRON_LA"
)


# =====================
# DATABASE MODELS
# =====================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    balance = Column(Float, default=0)
    is_admin = Column(Integer, default=0)



class Deposit(Base):

    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    txid = Column(String)
    status = Column(String, default="pending")
    date = Column(String, default=str(datetime.now()))



class Withdraw(Base):

    __tablename__ = "withdraws"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Float)
    wallet = Column(String)
    status = Column(String, default="pending")
    date = Column(String, default=str(datetime.now()))



Base.metadata.create_all(bind=engine)



# =====================
# DATABASE
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

    with open("index.html","r",encoding="utf-8") as file:

        return file.read()



# =====================
# DASHBOARD
# =====================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    with open("dashboard.html","r",encoding="utf-8") as file:

        return file.read()
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


    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )



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


    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )



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
