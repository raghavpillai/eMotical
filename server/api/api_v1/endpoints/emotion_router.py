from typing import Any
from fastapi import APIRouter
from server.logic.session_handler import SessionHandler

router = APIRouter()
s_handler: SessionHandler = SessionHandler()


@router.post("/create/{session_id}")
async def create_session(*, session_id: str) -> Any:
    s_handler.create_session(session_id)
    return {"message": f"Created new session {session_id}"}


@router.put("/update_entity/{category}/{url}/{amount}")
async def update_entity(*, category: str, url: str, amount: str) -> Any:
    if s_handler:
        s_handler.update_entity(category, url, int(amount))
        return {"success": True}
    return {"success": False}


@router.get("/get_recs/{category}")
async def get_recs(*, category: str) -> Any:
    if s_handler:
        return s_handler.get_recs(category)
    return {"success": False}


@router.get("/analysis")
async def process_image() -> Any:
    session = s_handler.current_session
    res = await session.process_images(session.session_id)
    return res
