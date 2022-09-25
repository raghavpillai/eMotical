from typing import Any
from fastapi import APIRouter
from server.logic.session_handler import SessionHandler

print("> Beginning build")
router = APIRouter()
s_handler: SessionHandler = SessionHandler()


@router.post("/create/{session_id}")
async def create_session(*, session_id: str) -> Any:
    """
    Creates a session given a session ID
    """
    s_handler.create_session(session_id)
    return {"message": f"Created new session {session_id}"}


@router.get("/report")
async def generate_report(*, draw_boxes=True) -> Any:
    """
    Given a prompt to process image, process image and return data
    """
    if s_handler.current_session:
        res = await s_handler.generate_report(draw_boxes)
        return res
    return False
