from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.auth import SignupPayload
from app.repositories.company_repo import company_repo
from app.repositories.user_repo import user_repo
from app.models.user import UserRole
from app.schemas.company import CompanyCreate
from app.schemas.user import UserCreate

class AuthService:
    def signup(self, db: Session, payload: SignupPayload):
        # Check if user with this email already exists
        if user_repo.get_user_by_email(db, payload.user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        # Create the company
        db_company = company_repo.create_company(db, payload.company)

        # Create the company admin user
        db_user = user_repo.create_user(
            db, payload.user, role=UserRole.company, company_id=db_company.id
        )

        return db_company

auth_service = AuthService()