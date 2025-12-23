from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.common.schemas.session_schemas import CreateChatsSession, Session as SessionSchema
from app.common.repositories.session_repo import session_repo
from app.common.dependencies.auth import RoleRequired
from app.common.models.user import User, UserRole
from app.common.utils.pagination import pagination_parameters, PaginatedResponse

router = APIRouter()

@router.post("/newSession", response_model=SessionSchema)
def newSession(
    request: Request, 
    payload: CreateChatsSession,
    current_user: User = Depends(RoleRequired([UserRole.employee, UserRole.company]))
):
    db: Session = request.state.db
    session = session_repo.create_session(db=db, user_id=current_user.id, session_data=payload)
    return session

@router.get("/sessions", response_model=PaginatedResponse[SessionSchema])
def get_sessions(
    request: Request,
    current_user: User = Depends(RoleRequired()),
    pagination: dict = Depends(pagination_parameters),
):
    db: Session = request.state.db
    sessions, total = session_repo.get_sessions_by_user_id(
        db=db, user_id=current_user.id, skip=pagination["skip"], limit=pagination["limit"]
    )
    return PaginatedResponse(
        total=total,
        page=pagination["page"],
        size=pagination["size"],
        results=sessions,
    )
