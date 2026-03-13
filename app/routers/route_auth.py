"""Authentication router module.

This module provides API endpoints for user authentication
including login functionality.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Schema for login request data.

    Attributes:
        username: Username for authentication.
        password: Plain text password.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """User data returned after successful login.

    Attributes:
        id_user: Unique identifier of the user.
        username: User's username.
        email: User's email address.
        role: User's role level.
    """

    id_user: int
    username: str
    email: str
    role: int


class LoginResponse(BaseModel):
    """Response schema for successful login.

    Attributes:
        access_token: JWT access token.
        token_type: Type of token (always "bearer").
        user: User information.
    """

    access_token: str
    token_type: str
    user: UserResponse


def get_db():
    """Provide database session for dependency injection.

    Yields:
        SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token.

    Args:
        credentials: Username and password for authentication.
        db: Database session (injected).

    Returns:
        LoginResponse containing access token and user info.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    result = AuthService.authenticate_user(
        db, credentials.username, credentials.password
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user, token = result

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }
