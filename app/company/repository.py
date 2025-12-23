import secrets
from sqlalchemy.orm import Session
from app.models.company import Company
from .schemas import CompanyCreate

class CompanyRepo:
    def create_company(self, db: Session, company: CompanyCreate) -> Company:
        unique_code = secrets.token_urlsafe(6).upper()
        db_company = Company(
            name=company.name,
            address=company.address,
            phone_number=company.phone_number,
            unique_code=unique_code,
        )
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company

    def get_company_by_code(self, db: Session, code: str) -> Company | None:
        return db.query(Company).filter(Company.unique_code == code).first()

company_repo = CompanyRepo()