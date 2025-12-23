from fastapi import APIRouter, status, Request
from sqlalchemy.orm import Session
from .schemas.auth_schemas import LoginPayload, LoginResponse, SignupPayload, SignupResponse
from .services.auth_service import auth_service

router = APIRouter()

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_200_OK)
def signup(request: Request, payload: SignupPayload):
    db: Session = request.state.db
    return auth_service.signup(db, payload)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(request: Request, payload: LoginPayload):
    db: Session = request.state.db
    return auth_service.login(db, payload)