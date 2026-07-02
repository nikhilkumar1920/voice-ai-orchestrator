import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.campaigns import router as campaigns_router
from api.companies import router as companies_router
from api.customers import router as customers_router
from routes.webhook import router as webhook_router

load_dotenv()


def _get_cors_origins() -> list[str]:
    configured_origins = os.getenv("FRONTEND_URLS") or os.getenv("FRONTEND_URL")
    if configured_origins:
        return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_origin_regex=os.getenv("FRONTEND_URL_REGEX", r"https://.*\.onrender\.com"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies_router)
app.include_router(customers_router)
app.include_router(campaigns_router)
app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "Voice AI Backend Running 🚀"}