from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #2563eb);
                color: white;
                text-align: center;
                padding: 60px 20px;
            }}

            .box {{
                background: white;
                color: #111;
                padding: 35px;
                border-radius: 20px;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}

            h1 {{
                color: #2563eb;
            }}

            button {{
                padding: 12px 18px;
                margin: 6px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                font-size: 15px;
            }}
        </style>
    </head>

    <body>
        <div class="box">
            <h1>{data["title"]}</h1>
            <p>{data["text"]}</p>

            <a href="/?lang=ht">
                <button>🇭🇹 Kreyòl</button>
            </a>

            <a href="/?lang=fr">
                <button>🇫🇷 Français</button>
            </a>

            <a href="/?lang=en">
                <button>🇺🇸 English</button>
            </a>
        </div>
    </body>
    </html>
    """

@app.get("/status")
def status():
    return {
        "status": "API a ap mache"
    }
