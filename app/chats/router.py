from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.common.schemas.session_schemas import CreateChatsSession, Session as SessionSchema
from app.common.dependencies.auth import RoleRequired
from app.common.models.user import User, UserRole
from app.common.utils.pagination import pagination_parameters, PaginatedResponse
from .services.chat_service import chat_service

router = APIRouter()

@router.post("/newSession", response_model=SessionSchema)
def new_session(
    request: Request, 
    payload: CreateChatsSession,
    current_user: User = Depends(RoleRequired([UserRole.employee, UserRole.company]))
):
    db: Session = request.state.db
    return chat_service.create_session(db=db, user_id=current_user.id, session_data=payload)

@router.get("/sessions", response_model=PaginatedResponse[SessionSchema])
def get_sessions(
    request: Request,
    current_user: User = Depends(RoleRequired()),
    pagination: dict = Depends(pagination_parameters),
):
    db: Session = request.state.db
    sessions, total = chat_service.get_sessions_by_user_id(
        db=db, user_id=current_user.id, skip=pagination["skip"], limit=pagination["limit"]
    )
    return PaginatedResponse(
        total=total,
        page=pagination["page"],
        size=pagination["size"],
        results=sessions,
    )
