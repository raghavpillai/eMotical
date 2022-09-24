from fastapi import APIRouter
from .endpoints import emotion_router

api_router = APIRouter()
api_router.include_router(
    emotion_router.router, prefix="/emotions", tags=["Emotions"]
)