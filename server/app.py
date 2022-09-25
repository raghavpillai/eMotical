from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.api_v1.api import api_router


def create_app() -> FastAPI:
    """
    Creates FastAPI app
    """
    app = FastAPI(title="Carmotion Emotions API", version="0.1.0")
    app.include_router(api_router, prefix="/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
