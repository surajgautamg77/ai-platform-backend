from pydantic import BaseModel
from app.schemas.company import CompanyCreate
from app.schemas.user import UserCreate

class SignupPayload(BaseModel):
    company: CompanyCreate
    user: UserCreate