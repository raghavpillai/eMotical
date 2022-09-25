<<<<<<< HEAD
from fastapi import WebSocket
=======
from tkinter import S
>>>>>>> 58effa05bcbeda41af6e21efb52139dc614156c4
from .session import Session
from .recommendations import Recommendations


class SessionHandler:
    """
    Global session handler class
    """

    # Global session objects
<<<<<<< HEAD
    current_session: Session = None
    recommendations: Recommendations = None

    # Websocket local to session handler
    websocket_obj: WebSocket = None
    
    def create_session(self, session_id: str) -> None:
=======
    recommendations: Recommendations = Recommendations()

    def create_session(self, session_id: str) -> Session:
>>>>>>> 58effa05bcbeda41af6e21efb52139dc614156c4
        """
        Creates a new section
        @param session_id: str: unique ID to define session
        """
        self.current_session = Session(session_id)

    def update_entity(self, category: str, url: str, amount: int) -> None:
        """
        Updates weights based on parameters
        @param category: str: Array category to update
        @param url: str: url (without youtube link) to use as key
        @param amount: int: Amount to update weights with
        """
<<<<<<< HEAD
        self.recommendations.adjust_all_weights(category, "https://www.youtube.com/watch?v="+url, amount)
=======
        self.recommendations.adjust_weights(
            category, "https://www.youtube.com/watch?v=" + url, amount
        )
>>>>>>> 58effa05bcbeda41af6e21efb52139dc614156c4

    def get_recs(self, category: str) -> None:
        """
        Gets recommendation from current recommendation update
        @param category: str: Category to return
        """
        return self.recommendations.generate_recommendations(category)

    def prompt_chat_message(self) -> str:
        """
        Begin prompt for chat msg
        @return str: returns initial chat to fire back to client
        """
        initial_msg: str = self.current_session.start_chat()
        return initial_msg

    def process_chat_msg(self, msg:str) -> str:
        """
        Processes a chat when a chat is fired to the server
        @return str: returns response string to fire back to client
        """
        new_msg: str = self.current_session.process_chat(msg)
        return new_msg

    def __init__(self):
        """
        Function initalization
        """
        print("Initialized session handler")
