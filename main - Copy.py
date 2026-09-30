from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router

settings = get_settings()

app = FastAPI(
    title="LegalEase AI API",
    version="1.0.0",
    description="AI-assisted legal document drafting API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "LegalEase AI API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "demo_mode": settings.demo_mode,
        "model": settings.gemini_model,
    }
