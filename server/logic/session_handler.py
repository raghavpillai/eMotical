from fastapi import WebSocket
from typing import List
from .session import Session
from .recommendations import Recommendations


class SessionHandler:
    """
    Global session handler class
    """
    
    # Global session objects
    current_session: Session = None
    recommendations: Recommendations = None

    # Websocket local to session handler
    websocket_obj: WebSocket = None
    
    def create_session(self, session_id: str) -> None:
        """
        Creates a new section
        @param session_id: str: unique ID to define session
        """
        if self.current_session is not None:
            print(f"!! Abandoning session {self.current_session.session_id}, lasted {self.current_session.duration}s !!")
            self.current_session = None
        self.current_session = Session(session_id)

    async def end_session(self) -> None:
        analysis: List = self.current_session.create_analysis()
        print(f"Ended session {self.current_session.session_id}, duration {self.current_session.duration}s")
        self.current_session = None
        return analysis

    def update_ind_entity(self, category: str, tag: str, amount: int) -> None:
        """
        Updates weights based on parameters
        @param category: str: Array category to update
        @param tag: str: tag to use as key
        @param amount: int: Amount to update weights with
        """
        self.recommendations.adjust_ind_weight(category, tag, amount)

    def update_entity(self, category: str, url: str, amount: int) -> None:
        """
        Updates weights based on parameters
        @param category: str: Array category to update
        @param url: str: url (without youtube link) to use as key
        @param amount: int: Amount to update weights with
        """
        self.recommendations.adjust_all_weights(category, url, amount)

    def get_recs(self, category: str) -> None:
        """
        Gets recommendation from current recommendation update
        @param category: str: Category to return
        """
        return self.recommendations.generate_recommendations(category)


    def process_chat_msg(self, msg:str, category, detail) -> str:
        """
        Processes a chat when a chat is fired to the server
        @return str: returns response string to fire back to client
        """
        new_msg: str = self.current_session.process_chat(msg, category, detail)
        return new_msg

    def __init__(self):
        """
        Function initalization
        """
        self.recommendations = Recommendations()
        print("Initialized session handler")
