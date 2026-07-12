from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime
import os


# =====================
# KONFIGIRASYON APP
# =====================

app = FastAPI(
    title="VestiCore",
    description="Platfòm VestiCore",
    version="2.0"
)


DATABASE_URL = "sqlite:///./vesticore.db"


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

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    balance = Column(
        Float,
        default=0
    )

    is_admin = Column(
        Integer,
        default=0
    )

    referral_code = Column(
        String,
        unique=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )


class Plan(Base):

    __tablename__ = "plans"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    duration = Column(Integer)

    description = Column(String)



class UserPlan(Base):

    __tablename__ = "user_plans"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer
    )

    plan_id = Column(
        Integer
    )

    amount = Column(
        Float
    )

    status = Column(
        String,
        default="active"
    )

    start_date = Column(
        DateTime,
        default=datetime.now
    )



class Deposit(Base):

    __tablename__ = "deposits"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(String)

    amount = Column(Float)

    txid = Column(String)

    status = Column(
        String,
        default="pending"
    )

    date = Column(
        DateTime,
        default=datetime.now
    )



class Withdraw(Base):

    __tablename__ = "withdraws"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(String)

    amount = Column(Float)

    wallet = Column(String)

    status = Column(
        String,
        default="pending"
    )

    date = Column(
        DateTime,
        default=datetime.now
    )



class Referral(Base):

    __tablename__ = "referrals"

    id = Column(
        Integer,
        primary_key=True
    )

    referrer = Column(String)

    invited_user = Column(String)

    status = Column(
        String,
        default="pending"
    )


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(String)

    action = Column(String)

    date = Column(
        DateTime,
        default=datetime.now
    )



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

    log = ActivityLog(
        username=username,
        action=action
    )

    db.add(log)
    db.commit()



# =====================
# INITIAL PLANS
# =====================

def create_default_plans():

    db = SessionLocal()

    plans = db.query(Plan).all()

    if len(plans) == 0:

        starter = Plan(
            name="Starter",
            duration=30,
            description="Plan debaz VestiCore"
        )


        standard = Plan(
            name="Standard",
            duration=60,
            description="Plan entèmedyè VestiCore"
        )


        premium = Plan(
            name="Premium",
            duration=90,
            description="Plan avanse VestiCore"
        )


        vip = Plan(
            name="VIP",
            duration=120,
            description="Plan VIP VestiCore"
        )


        db.add_all([
            starter,
            standard,
            premium,
            vip
        ])

        db.commit()


    db.close()



create_default_plans()
