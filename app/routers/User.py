"""User management router module.

This module provides API endpoints for user CRUD operations
with role-based access control.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.UserService import UserCreate, UserRead, UserService, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


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


def require_admin(x_role: int = Header(...)):
    """Require admin or superadmin role (role >= 1).

    In production, replace this header with JWT token verification.

    Args:
        x_role: Role level from request header.

    Returns:
        Role level if authorized.

    Raises:
        HTTPException: 403 if role is insufficient.
    """
    if x_role < 1:
        raise HTTPException(status_code=403, detail="Accès réservé aux admins.")
    return x_role


def require_superadmin(x_role: int = Header(...)):
    """Require superadmin role (role == 2).

    Args:
        x_role: Role level from request header.

    Returns:
        Role level if authorized.

    Raises:
        HTTPException: 403 if not superadmin.
    """
    if x_role < 2:
        raise HTTPException(status_code=403, detail="Accès réservé aux superadmins.")
    return x_role


@router.get("/", response_model=List[UserRead])
def read_users(
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """Retrieve all users (Admin+ only).

    Args:
        db: Database session (injected).
        role: User role from header (injected).

    Returns:
        List of all users.
    """
    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """Retrieve a single user by ID (Admin+ only).

    Args:
        user_id: ID of the user to retrieve.
        db: Database session (injected).
        role: User role from header (injected).

    Returns:
        User object.

    Raises:
        HTTPException: 404 if user not found.
    """
    service = UserService(db)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    role: int = Depends(require_superadmin),
):
    """Create a new user (Superadmin only).

    Args:
        user: User creation data.
        db: Database session (injected).
        role: User role from header (injected).

    Returns:
        Created user object.
    """
    service = UserService(db)
    return service.create(user)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """Update an existing user (Admin+ only).

    Role modification requires superadmin privileges.

    Args:
        user_id: ID of the user to update.
        user: Updated user data.
        db: Database session (injected).
        role: User role from header (injected).

    Returns:
        Updated user object.

    Raises:
        HTTPException: 403 if insufficient privileges, 404 if user not found.
    """
    service = UserService(db)
    try:
        updated = service.update(user_id, user, requester_role=role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: int = Depends(require_superadmin),
):
    """Delete a user (Superadmin only).

    Args:
        user_id: ID of the user to delete.
        db: Database session (injected).
        role: User role from header (injected).

    Returns:
        Success message.

    Raises:
        HTTPException: 404 if user not found.
    """
    service = UserService(db)
    success = service.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
