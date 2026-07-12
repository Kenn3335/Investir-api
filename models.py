from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


# =====================
# USERS
# =====================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

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

    referral_code = Column(
        String,
        unique=True
    )

    referred_by = Column(
        String,
        nullable=True
    )

    is_admin = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )



# =====================
# PLANS
# =====================

class Plan(Base):

    __tablename__ = "plans"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String
    )

    price = Column(
        Float
    )

    duration = Column(
        Integer
    )

    description = Column(
        String
    )



# =====================
# USER PLANS
# =====================

class UserPlan(Base):

    __tablename__ = "user_plans"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    plan_name = Column(
        String
    )

    amount = Column(
        Float
    )

    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )



# =====================
# DEPOSITS
# =====================

class Deposit(Base):

    __tablename__ = "deposits"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    amount = Column(
        Float
    )

    txid = Column(
        String
    )

    status = Column(
        String,
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )



# =====================
# WITHDRAWALS
# =====================

class Withdraw(Base):

    __tablename__ = "withdraws"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    amount = Column(
        Float
    )

    wallet = Column(
        String
    )

    status = Column(
        String,
        default="pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )



# =====================
# REFERRALS
# =====================

class Referral(Base):

    __tablename__ = "referrals"

    id = Column(
        Integer,
        primary_key=True
    )

    owner = Column(
        String
    )

    invited_user = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )



# =====================
# ACTIVITY LOGS
# =====================

class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    action = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )
