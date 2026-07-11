from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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




@app.get("/")
def home():
    return FileResponse("index.html")
    
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
    User.email == email.strip()
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
