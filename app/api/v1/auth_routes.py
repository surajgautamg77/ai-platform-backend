from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.auth import SignupPayload
from app.schemas.company import Company
from app.schemas.user import User
from app.services.auth_service import auth_service
from typing import Union

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=Union[Company, User], status_code=status.HTTP_201_CREATED)
def signup(payload: SignupPayload, db: Session = Depends(get_db)):
    return auth_service.signup(db, payload)