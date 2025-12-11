import sys
import os
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.hashing import Hasher

def seed_superadmin():
    db: Session = SessionLocal()
    try:
        # Check if superadmin already exists
        superadmin = db.query(User).filter(User.role == UserRole.superadmin).first()
        if superadmin:
            print("Superadmin already exists.")
            return

        # Create superadmin user
        superadmin_user = User(
            email="superadmin@example.com",
            hashed_password=Hasher.get_password_hash("superadminpassword"),
            full_name="Super Admin",
            role=UserRole.superadmin,
            is_active=True,
        )
        db.add(superadmin_user)
        db.commit()
        print("Superadmin created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_superadmin()
