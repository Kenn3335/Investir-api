from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

app = FastAPI(
    title="Envesti API",
    description="Platfòm envestisman ak login, depo, retrè ak balans",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./investir.db"

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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(Integer, default=0)


Base.metadata.create_all(bind=engine)


messages = {
    "ht": {
        "title": "Byenveni sou Envesti API",
        "text": "Platfòm envestisman ou a pare pou itilize."
    },
    "fr": {
        "title": "Bienvenue sur Envesti API",
        "text": "Votre plateforme d'investissement est prête."
    },
    "en": {
        "title": "Welcome to Envesti API",
        "text": "Your investment platform is ready."
    }
}


@app.get("/", response_class=HTMLResponse)
def home(lang: str = "ht"):
    data = messages.get(lang, messages["ht"])

    return f"""
    <html>
    <head>
        <title>Envesti API</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body style="font-family:Arial;text-align:center;padding:50px">
        <h1>{data["title"]}</h1>
        <p>{data["text"]}</p>

        <a href="/?lang=ht">🇭🇹 Kreyòl</a>
        <br>
        <a href="/?lang=fr">🇫🇷 Français</a>
        <br>
        <a href="/?lang=en">🇺🇸 English</a>

    </body>
    </html>
    """
    
@app.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "Itilizatè sa deja egziste"
        }

    hashed_password = pwd_context.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        balance=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "Kont kreye avèk siksè",
        "username": username
    }


@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        db.close()
        return {
            "message": "Kont pa jwenn"
        }

    if not pwd_context.verify(password, user.password):
        db.close()
        return {
            "message": "Modpas la pa bon"
        }

    db.close()

    return {
        "message": "Koneksyon reyisi",
        "username": user.username,
        "balance": user.balance
    }


@app.get("/status")
def status():
    return {
        "status": "API a ap mache"
    }
