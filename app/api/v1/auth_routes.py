from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.auth import LoginPayload, LoginResponse, SignupPayload, SignupResponse
from app.services.auth_service import auth_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupPayload, db: Session = Depends(get_db)):
    return auth_service.signup(db, payload)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)