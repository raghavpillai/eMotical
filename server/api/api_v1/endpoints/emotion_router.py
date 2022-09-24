from typing import Any
from fastapi import APIRouter, WebSocket
from server.logic.session_handler import SessionHandler

router = APIRouter()
s_handler: SessionHandler = SessionHandler()


@router.get("/create/{session_id}")
async def create_session(*, session_id: str) -> Any:
    """
    Creates a session given a session ID
    """
    s_handler.create_session(session_id)
    return f"Created new session {session_id}"


@router.get("/update_entity/{category}/{url}/{amount}")
async def update_entity(*, category: str, url: str, amount: str) -> Any:
    """
    Updates all weights for a category and url to a constant amount
    """
    if s_handler:
        s_handler.update_entity(category, url, int(amount))
        return True
    return False


@router.get("/get_recs/{category}")
async def get_recs(*, category: str) -> Any:
    """
    Returns the top 5 recs (or random if no prev data) for a given category
    """
    if s_handler:
        return s_handler.get_recs(category)
    return False


@router.post("/image")
async def process_image() -> Any:
    """
    Given a prompt to process image, process image and return data
    """
    session = SessionHandler.current_session
    res = session.process_image(session.session_id)
    return res


@router.get("/video")
async def process_video() -> Any:
    """
    Given a prompt to process video, process video and return data
    """
    session = SessionHandler.current_session
    res = session.process_video(session.session_id)
    return res

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket to handle chatting for local session
    """
    SessionHandler.websocket_obj = WebSocket
    await websocket.accept()
    websocket.send_text(SessionHandler.prompt_chat_message())
    while True:
        data = await websocket.receive_text()
        msg_to_send = SessionHandler.process_chat_msg(data)
        await websocket.send_text(msg_to_send)
