from typing import Any
from fastapi import APIRouter, WebSocket
from server.logic.session_handler import SessionHandler

print("> Beginning build")
router = APIRouter()
s_handler: SessionHandler = SessionHandler()


@router.get("/create/{session_id}")
async def create_session(*, session_id: str) -> Any:
    """
    Creates a session given a session ID
    """
    s_handler.create_session(session_id)
    return {"message": f"Created new session {session_id}"}

@router.get("/update_ind_entity/{category}/{tag}/{amount}")
async def update_entity(*, category: str, tag: str, amount: str) -> Any:
    """
    Updates individual tag entity
    """
    if s_handler:
        s_handler.update_ind_entity(category, tag, int(amount))
        return {"success": True}
    return {"success": False}

@router.get("/update_entity/{category}/{url}/{amount}")
async def update_entity(*, category: str, url: str, amount: str) -> Any:
    """
    Updates all weights for a category and url to a constant amount
    """
    if s_handler:
        s_handler.update_entity(category, url, int(amount))
        return {"success": True}
    return {"success": False}


@router.get("/get_recs/{category}")
async def get_recs(*, category: str) -> Any:
    """
    Returns the top 5 recs (or random if no prev data) for a given category
    """
    if s_handler:
        return s_handler.get_recs(category)
    return {"success": False}


@router.get("/end_session")
async def process_image() -> Any:
    """
    Given a prompt to process image, process image and return data
    """
    if s_handler.current_session:
        res = await s_handler.end_session()
        return res
    return False

@router.get("/chat/{msg}/{category}/{detail}")
async def prompt_chat_message(*, msg: str, category: str="", detail: str="") -> Any:
    msg_to_send = SessionHandler.process_chat_msg(msg, category, detail)
    return msg_to_send
