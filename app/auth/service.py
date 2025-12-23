from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .schemas import LoginPayload, SignupPayload
from app.company.repository import company_repo
from app.users.repository import user_repo
from app.models.user import User, UserRole
from app.company.schemas import CompanyCreate
from app.users.schemas import UserCreate
from app.utils.token import create_access_token
from app.utils.hashing import Hasher

class AuthService:
    def signup(self, db: Session, payload: SignupPayload):
        # Prevent superadmin signup via API
        if payload.role == UserRole.superadmin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Superadmin signup is not allowed via this API.",
            )

        # 1. Check if user with this email already exists
        if user_repo.get_user_by_email(db, payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        user_data = UserCreate(
            email=payload.email,
            password=payload.password,
            full_name=payload.name # Use payload.name here
        )

        db_user = None
        # 2. Handle Employee Signup
        if payload.role == UserRole.employee:
            db_company = company_repo.get_company_by_code(db, payload.company_code)
            if not db_company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with code {payload.company_code} not found",
                )
            
            db_user = user_repo.create_user(
                db, user=user_data, role=UserRole.employee, company_id=db_company.id
            )

        # 3. Handle Company Admin Signup
        elif payload.role == UserRole.company:
            # Prepare company data - name will be payload.name
            company_data = CompanyCreate(name=payload.name) # Use payload.name here
            db_company = company_repo.create_company(db, company_data)
            
            db_user = user_repo.create_user(
                db, user=user_data, role=UserRole.company, company_id=db_company.id
            )

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User could not be created.",
            )

        access_token = create_access_token(user=db_user)
        return {
            "user": db_user,
            "company_code": db_company.unique_code,
            "token": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }

    def login(self, db: Session, payload: LoginPayload):
        db_user = user_repo.get_user_by_email(db, payload.email)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {payload.email} not found",
            )

        if not Hasher.verify_password(payload.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        access_token = create_access_token(user=db_user)
        return {
            "user": db_user,
            "token": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }

auth_service = AuthService()