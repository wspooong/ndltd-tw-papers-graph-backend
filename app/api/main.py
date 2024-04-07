from fastapi import APIRouter

from app.api.routes import document, genai, stats

api_router = APIRouter()
api_router.include_router(document.router, prefix="/document", tags=["document"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(genai.router, prefix="/genai", tags=["genai"])
