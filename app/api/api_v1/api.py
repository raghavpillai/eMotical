from fastapi import APIRouter
from .endpoints import emotions

api_router = APIRouter()
api_router.include_router(
    emotions.router, prefix="/emotions", tags=["Emotions"]
)
