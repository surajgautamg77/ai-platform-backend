from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.schemas.chats import CreateChatsSession, Session as SessionSchema
from typing import Any, List
from app.api.deps import RoleRequired
from app.models.user import User, UserRole # Import UserRole
from app.repositories.session_repo import session_repo

router = APIRouter()

@router.get("/")
def get_chats(request: Request):
    db: Session = request.state.db
    # Add your logic here
    return {"message": "This is the chat route"}


@router.post("/newSession", response_model=SessionSchema)
def newSession(
    request: Request, 
    payload: CreateChatsSession,
    current_user: User = Depends(RoleRequired([UserRole.employee, UserRole.company]))
):
    db: Session = request.state.db
    session = session_repo.create_session(db=db, user_id=current_user.id, session_data=payload)
    return session

@router.get("/sessions", response_model=List[SessionSchema])
def get_sessions(
    request: Request,
    current_user: User = Depends(RoleRequired())
):
    db: Session = request.state.db
    sessions = session_repo.get_sessions_by_user_id(db=db, user_id=current_user.id)
    return sessions
