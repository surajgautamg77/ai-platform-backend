from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate

class CompanyRepo:
    def create_company(self, db: Session, company: CompanyCreate) -> Company:
        db_company = Company(
            name=company.name,
            address=company.address,
            phone_number=company.phone_number,
        )
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company

company_repo = CompanyRepo()
