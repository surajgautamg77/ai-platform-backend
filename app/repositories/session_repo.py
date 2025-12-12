from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.chats import CreateChatsSession
from typing import List

class SessionRepository:
    def create_session(self, db: Session, user_id: int, session_data: CreateChatsSession) -> SessionModel:
        db_session = SessionModel(
            session_name=session_data.session_name,
            user_id=user_id
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    def get_sessions_by_user_id(self, db: Session, user_id: int) -> List[SessionModel]:
        return db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

session_repo = SessionRepository()
