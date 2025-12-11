from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.auth import SignupPayload
from app.repositories.company_repo import company_repo
from app.repositories.user_repo import user_repo
from app.models.user import UserRole
from app.schemas.company import CompanyCreate
from app.schemas.user import UserCreate

from app.schemas.user import User

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
            return db_user

        # 3. Handle Company Admin Signup
        elif payload.role == UserRole.company:
            # Prepare company data - name will be payload.name
            company_data = CompanyCreate(name=payload.name) # Use payload.name here
            db_company = company_repo.create_company(db, company_data)
            
            db_user = user_repo.create_user(
                db, user=user_data, role=UserRole.company, company_id=db_company.id
            )
            # For this flow, returning the company seems more appropriate
            return db_company
        
auth_service = AuthService()