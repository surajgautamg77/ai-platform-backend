from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from app.models.user import User

def create_access_token(
    user: User, expires_delta: timedelta = None
) -> str:
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
    
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
