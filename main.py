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

    referred_by = Column(
        String,
        nullable=True
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
# =====================
# HOME PAGE
# =====================

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
        <title>VestiCore</title>
    </head>

    <body>

        <h1>VestiCore</h1>

        <h2>Platfòm dijital nou an</h2>

        <p>
        Kreye kont oswa konekte pou jwenn aksè ak espas ou.
        </p>

        <a href="/register">
            Kreye kont
        </a>

        <br><br>

        <a href="/login">
            Konekte
        </a>

    </body>
    </html>
    """



# =====================
# REGISTER PAGE
# =====================

@app.get("/register", response_class=HTMLResponse)
def register_page():

    return """
    <html>
    <body>

    <h2>Kreye kont</h2>

    <form method="post">

        <input name="username"
        placeholder="Non itilizatè">

        <br><br>

        <input
        type="password"
        name="password"
        placeholder="Modpas">

        <br><br>

        <input
        name="ref"
        placeholder="Kòd referral (opsyonèl)">

        <br><br>

        <button>
        Kreye kont
        </button>

    </form>

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

    user_exist = db.query(User).filter(
        User.username == username
    ).first()


    if user_exist:

        raise HTTPException(
            status_code=400,
            detail="Kont sa deja egziste"
        )


    new_user = User(

    username=username,

    password=hash_password(password),

    referral_code=create_referral_code(username),

    referred_by=ref

)


    db.add(new_user)


    if ref:

        referral = Referral(

            referrer=ref,

            invited_user=username

        )

        db.add(referral)


    log = ActivityLog(

        username=username,

        action="Kreye nouvo kont"

    )

    db.add(log)


    db.commit()


    return RedirectResponse(
        url="/login",
        status_code=303
    )
# =====================
# LOGIN PAGE
# =====================

@app.get("/login", response_class=HTMLResponse)
def login_page():

    return """
    <html>
    <body>

    <h2>Konekte</h2>

    <form method="post">

        <input
        name="username"
        placeholder="Non itilizatè">

        <br><br>

        <input
        type="password"
        name="password"
        placeholder="Modpas">

        <br><br>

        <button>
        Konekte
        </button>

    </form>

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

    user = db.query(User).filter(
        User.username == username
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="Itilizatè pa jwenn"
        )


    if not verify_password(
        password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Modpas pa bon"
        )


    request.session["username"] = username


    create_log(
        db,
        username,
        "Koneksyon fèt"
    )


    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )



# =====================
# CHECK LOGIN
# =====================

def current_user(
    request: Request,
    db: Session
):

    username = request.session.get(
        "username"
    )


    if not username:

        raise HTTPException(
            status_code=401,
            detail="Ou dwe konekte"
        )


    user = db.query(User).filter(
        User.username == username
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="Kont pa jwenn"
        )


    return user
# =====================
# USER DASHBOARD
# =====================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    plans = db.query(Plan).all()


    plan_html = ""


    for plan in plans:

        plan_html += f"""
        <div>
            <h3>{plan.name}</h3>
            <p>{plan.description}</p>
            <p>Dire: {plan.duration} jou</p>
        </div>
        <hr>
        """



    return f"""

    <html>

    <head>
        <title>VestiCore Dashboard</title>
    </head>


    <body>

    <h1>Byenveni {user.username}</h1>


    <h3>Balans</h3>

    <p>
    {user.balance} USDT
    </p>


    <h2>Sèvis nou yo</h2>

    <p>
    💰 Depo USDT
    </p>

    <p>
    💸 Retrè
    </p>

    <p>
    👥 Referral
    </p>


    <h2>Plan VestiCore</h2>


    {plan_html}


    </body>

    </html>

    """
from starlette.middleware.sessions import SessionMiddleware


# =====================
# SESSION SECURITY
# =====================

app.add_middleware(
    SessionMiddleware,
    secret_key="vesticore-secret-key-change-later"
)



# =====================
# DEPOSIT INFO
# =====================

@app.get("/deposit-info")
def deposit_info(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    return {
        "network": "TRC20",
        "currency": "USDT",
        "wallet": USDT_TRON_ADDRESS,
        "fee": "3%"
    }



# =====================
# CREATE DEPOSIT
# =====================

@app.post("/deposit")
def deposit(
    request: Request,
    amount: float = Form(...),
    txid: str = Form(...),
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Montan pa valab"
        )


    fee = amount * DEPOSIT_FEE / 100


    deposit = Deposit(
        username=user.username,
        amount=amount,
        txid=txid,
        status="pending"
    )


    db.add(deposit)


    create_log(
        db,
        user.username,
        "Depo voye pou verifikasyon"
    )


    db.commit()


    return {
        "message": "Depo resevwa",
        "fee": fee,
        "status": "pending"
    }



# =====================
# CREATE WITHDRAW
# =====================

@app.post("/withdraw")
def withdraw(
    request: Request,
    amount: float = Form(...),
    wallet: str = Form(...),
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    if amount < MIN_WITHDRAW:

        raise HTTPException(
            status_code=400,
            detail="Minimum retrè se 10 USDT"
        )


    if amount > STARTER_MAX_WITHDRAW:

        raise HTTPException(
            status_code=400,
            detail="Limit retrè depase"
        )


    if user.balance < amount:

        raise HTTPException(
            status_code=400,
            detail="Balans pa ase"
        )


    fee = amount * WITHDRAW_FEE / 100


    withdraw = Withdraw(
        username=user.username,
        amount=amount,
        wallet=wallet,
        status="pending"
    )


    db.add(withdraw)


    create_log(
        db,
        user.username,
        "Demann retrè voye"
    )


    db.commit()


    return {
        "message": "Retrè voye pou verifikasyon",
        "fee": fee,
        "status": "pending"
    }
# =====================
# ADMIN CHECK
# =====================

def admin_user(
    request: Request,
    db: Session
):

    user = current_user(
        request,
        db
    )

    if user.is_admin != 1:

        raise HTTPException(
            status_code=403,
            detail="Aksè admin sèlman"
        )

    return user



# =====================
# ADMIN DASHBOARD
# =====================

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    admin_user(
        request,
        db
    )


    users = db.query(User).all()

    deposits = db.query(Deposit).all()

    withdraws = db.query(Withdraw).all()

    logs = db.query(ActivityLog).all()


    return f"""

    <html>

    <head>
        <title>VestiCore Admin</title>
    </head>

    <body>

    <h1>Admin Dashboard</h1>


    <h2>Itilizatè yo</h2>

    <p>
    Total: {len(users)}
    </p>


    <h2>Depo</h2>

    <p>
    Total demann: {len(deposits)}
    </p>


    <h2>Retrè</h2>

    <p>
    Total demann: {len(withdraws)}
    </p>


    <h2>Activity Logs</h2>

    <p>
    Total aktivite: {len(logs)}
    </p>


    </body>

    </html>

    """
# =====================
# LOGOUT
# =====================

@app.get("/logout")
def logout(
    request: Request
):

    request.session.clear()


    return RedirectResponse(
        url="/",
        status_code=303
    )



# =====================
# REFERRAL PAGE
# =====================

@app.get("/referral", response_class=HTMLResponse)
def referral_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    referrals = db.query(Referral).filter(
        Referral.owner == user.referral_code
    ).all()



    return f"""

    <html>

    <head>
        <title>Referral</title>
    </head>


    <body>

    <h1>Referral VestiCore</h1>


    <p>
    Kòd pa ou:
    {user.referral_code}
    </p>


    <p>
    Lyen envitasyon:
    /register?ref={user.referral_code}
    </p>


    <h3>
    Moun ou envite:
    {len(referrals)}
    </h3>


    <a href="/dashboard">
    Retounen Dashboard
    </a>


    </body>

    </html>

    """



# =====================
# PROFILE
# =====================

@app.get("/profile")
def profile(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(
        request,
        db
    )


    return {

        "username": user.username,

        "balance": user.balance,

        "referral_code": user.referral_code

    }
# =====================
# PLANS API
# =====================

@app.get("/plans")
def get_plans(
    request: Request,
    db: Session = Depends(get_db)
):

    current_user(
        request,
        db
    )


    plans = db.query(Plan).all()


    return [

        {
            "name": plan.name,
            "price": plan.price,
            "duration": plan.duration,
            "description": plan.description
        }

        for plan in plans

    ]



# =====================
# CREATE DEFAULT PLANS
# =====================

@app.on_event("startup")
def startup_plans():

    db = next(get_db())


    total = db.query(Plan).count()


    if total == 0:

        plans = [

            Plan(
                name="Starter",
                price=10,
                duration=30,
                description="Plan debaz"
            ),

            Plan(
                name="Standard",
                price=50,
                duration=60,
                description="Plan entèmedyè"
            ),

            Plan(
                name="Premium",
                price=100,
                duration=90,
                description="Plan avanse"
            ),

            Plan(
                name="VIP",
                price=500,
                duration=120,
                description="Plan VIP"
            )

        ]


        db.add_all(plans)

        db.commit()


    db.close()



# =====================
# HEALTH CHECK
# =====================

@app.get("/status")
def status():

    return {

        "platform": "VestiCore",

        "status": "online"

    }
