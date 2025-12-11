from pydantic import BaseModel
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    address: str | None = None
    phone_number: str | None = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
