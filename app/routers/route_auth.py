from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str
    password: str


class UserResponse(BaseModel):
    """User data returned after login."""

    id_user: int
    username: str
    email: str
    role: int


class LoginResponse(BaseModel):
    """Response returned after successful login."""

    access_token: str
    token_type: str
    user: UserResponse


def get_db():
    """Provide database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate a user and return a JWT token."""

    result = AuthService.authenticate_user(
        db,
        credentials.username,
        credentials.password
    )

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    user, token = result

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }