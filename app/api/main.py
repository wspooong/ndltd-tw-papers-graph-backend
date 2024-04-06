from fastapi import APIRouter

from app.api.routes import document, genai

api_router = APIRouter()
api_router.include_router(document.router, prefix="/document", tags=["document"])
api_router.include_router(genai.router, prefix="/genai", tags=["genai"])