from tkinter import S
from .session import Session
from .recommendations import Recommendations


class SessionHandler:
    """
    Global session handler class
    """

    # Global session objects
    recommendations: Recommendations = Recommendations()

    def create_session(self, session_id: str) -> Session:
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
        self.recommendations.adjust_weights(
            category, "https://www.youtube.com/watch?v=" + url, amount
        )

    def get_recs(self, category: str) -> None:
        """
        Gets recommendation from current recommendation update
        @param category: str: Category to return
        """
        return self.recommendations.generate_recommendations(category)

    def __init__(self):
        """
        Function initalization
        """
        print("Initialized session handler")
