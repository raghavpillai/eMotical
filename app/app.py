from fastapi import FastAPI
from .api.api_v1.api import api_router
from .exceptions.carmotion import (
    CarmotionException,
    carmotion_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(title="Carmotion Emotions API", version="0.1.0")
    app.add_exception_handler(CarmotionException, carmotion_exception_handler)
    app.include_router(api_router, prefix="/v1")
    return app