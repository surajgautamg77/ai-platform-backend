from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.utils.hashing import Hasher

class UserRepo:
    def create_user(self, db: Session, user: UserCreate, role: UserRole, company_id: int = None) -> User:
        db_user = User(
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            full_name=user.full_name,
            role=role,
            company_id=company_id,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()


user_repo = UserRepo()
