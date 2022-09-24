from typing import Any

from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
def hello_world() -> Any:
    return {"message": "Hello World"}
