from pydantic import BaseModel, Field
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str = Field(..., max_length=72)
    company_id: int | None = None

class User(UserBase):
    id: int
    role: UserRole
    company_id: int | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
