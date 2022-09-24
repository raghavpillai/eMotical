from .session import Session

class SessionHandler:
    current_session: Session = None

    def create_session(self):
        self.current_session = Session()