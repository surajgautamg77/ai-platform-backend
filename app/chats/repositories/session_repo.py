from sqlalchemy.orm import Session
from app.common.models.session import Session as SessionModel
from ..schemas.session_schemas import CreateChatsSession
from typing import List, Tuple

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

    def get_sessions_by_user_id(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 20
    ) -> Tuple[List[SessionModel], int]:
        query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
        total = query.count()
        sessions = query.offset(skip).limit(limit).all()
        return sessions, total

session_repo = SessionRepository()
