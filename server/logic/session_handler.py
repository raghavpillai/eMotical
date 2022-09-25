from fastapi import WebSocket
from typing import List
from .session import Session


class SessionHandler:
    """
    Global session handler class
    """

    # Global session objects
    current_session: Session = None

    # Websocket local to session handler
    websocket_obj: WebSocket = None

    def create_session(self, session_id: str) -> None:
        """
        Creates a new section
        @param session_id: str: unique ID to define session
        """
        if self.current_session is not None:
            print(
                f"!! Abandoning session {self.current_session.session_id}, lasted {self.current_session.duration}s !!"
            )
            self.current_session = None
        self.current_session = Session(session_id)

    async def generate_report(self, draw_boxes=True) -> None:
        analysis: List = await self.current_session.process_images(draw_boxes)
        print(
            f"Ended session {self.current_session.session_id}, duration {self.current_session.duration}s"
        )
        self.current_session = None
        return analysis

    def __init__(self):
        """
        Function initalization
        """
        print("Initialized session handler")
