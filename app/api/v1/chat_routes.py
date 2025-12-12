from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.chats import ChatsSession
from typing import Any
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.session_repo import session_repo

router = APIRouter()

@router.get("/")
def get_chats(request: Request):
    db: Session = request.state.db
    # Add your logic here
    return {"message": "This is the chat route"}


@router.post("/newSession")
def newSession(request: Request, payload: ChatsSession, current_user: User = Depends(get_current_user)):
    db: Session = request.state.db
    session = session_repo.create_session(db=db, user_id=current_user.id, session_data=payload)
    return session
