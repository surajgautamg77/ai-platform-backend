from pydantic import BaseModel, model_validator, Field
from app.common.models.user import UserRole
from app.users.schemas.user_schemas import User

class SignupPayload(BaseModel):
    name: str # Combined field for full_name or company_name
    email: str
    password: str = Field(..., max_length=72)
    role: UserRole
    company_code: str | None = None

    @model_validator(mode='after')
    def validate_role_dependencies(self) -> 'SignupPayload':
        role = self.role
        company_code = self.company_code
        
        if role == UserRole.employee:
            if not company_code:
                raise ValueError("company_code is required for the 'employee' role")
            # For employee, 'name' is full_name
        
        if role == UserRole.company:
            # For company, 'name' is company_name
            if company_code:
                raise ValueError("company_code should not be provided for the 'company' role")

        return self


class Token(BaseModel):
    access_token: str
    token_type: str


class SignupResponse(BaseModel):
    user: User
    company_code: str | None = None
    token: Token


class LoginPayload(BaseModel):
    email: str
    password: str = Field(..., max_length=72)


LoginResponse = SignupResponse


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

