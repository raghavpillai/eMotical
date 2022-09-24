from fastapi import Request, status
from fastapi.responses import JSONResponse


class CarmotionException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "An exception occurred.",
    ):
        self.status_code = status_code
        self.detail = detail


def carmotion_exception_handler(
    request: Request, exc: CarmotionException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}
    )
