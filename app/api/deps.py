from typing import List, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.security import oauth2_scheme, TokenData
from app.core.config import settings
from app.models.user import User, UserRole
from app.repositories.user_repo import user_repo


def get_current_user(
    request: Request, token: str = Depends(oauth2_scheme)
) -> User:
    db: Session = request.state.db
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = user_repo.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def RoleRequired(allowed_roles: Optional[List[UserRole]] = None):
    """
    A factory that returns a dependency checking for authentication and,
    optionally, for specific user roles.

    :param allowed_roles: An optional list of roles that are allowed.
                          If None or empty, any authenticated user is allowed.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if allowed_roles and current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have enough privileges",
            )
        return current_user
    
    return role_checker
