from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    return {
        "message": "Byenvini sou platfòm Envesti API"
    }

@app.get("/status")
def status():
    return {
        "status": "API a ap mache"
    }
