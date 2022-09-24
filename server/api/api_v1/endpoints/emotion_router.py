from typing import Any
from fastapi import APIRouter
from server.logic.session_handler import SessionHandler

router = APIRouter()
s_handler: SessionHandler = SessionHandler()


@router.get("/create/{session_id}")
async def create_session(*, session_id: str) -> Any:
    s_handler.create_session(session_id)
    return f"Created new session {session_id}"


@router.get("/update_entity/{category}/{url}/{amount}")
async def update_entity(*, category: str, url: str, amount: str) -> Any:
    if s_handler:
        s_handler.update_entity(category, url, int(amount))
        return True
    return False


@router.get("/get_recs/{category}")
async def get_recs(*, category: str) -> Any:
    if s_handler:
        return s_handler.get_recs(category)
    return False


@router.post("/image")
async def process_image() -> Any:
    session = SessionHandler.current_session
    res = session.process_image(session.session_id)
    return res


@router.get("/video")
async def process_video() -> Any:
    session = SessionHandler.current_session
    res = session.process_video(session.session_id)
    return res
