from sqlalchemy.orm import Session
from typing import List, Tuple
from app.common.repositories.session_repo import session_repo
from app.common.schemas.session_schemas import CreateChatsSession
from app.common.models.session import Session as SessionModel

class ChatService:
    def create_session(self, db: Session, user_id: int, session_data: CreateChatsSession) -> SessionModel:
        """
        Creates a new chat session.
        """
        return session_repo.create_session(db=db, user_id=user_id, session_data=session_data)

    def get_sessions_by_user_id(
        self, db: Session, user_id: int, skip: int, limit: int
    ) -> Tuple[List[SessionModel], int]:
        """
        Retrieves a paginated list of sessions for a given user.
        """
        return session_repo.get_sessions_by_user_id(
            db=db, user_id=user_id, skip=skip, limit=limit
        )

chat_service = ChatService()
