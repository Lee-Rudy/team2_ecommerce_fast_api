"""User service and schemas.

This module provides the business logic layer for user operations
and defines Pydantic schemas for API interactions.
"""

from datetime import datetime
from typing import List, Optional

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.UserRepo import UserRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    """Schema for creating a new user.

    Attributes:
        username: Unique username for the user.
        email: User's email address.
        password: Plain text password (will be hashed).
        role: User role (0=user, 1=admin, 2=superadmin).
    """

    username: str
    email: EmailStr
    password: str
    role: Optional[int] = 0


class UserUpdate(BaseModel):
    """Schema for updating an existing user.

    All fields are optional to allow partial updates.

    Attributes:
        username: Updated username.
        email: Updated email address.
        password: Updated password (plain text, will be hashed).
        role: Updated role.
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[int] = None


class UserRead(BaseModel):
    """Schema for reading user data in API responses.

    Excludes sensitive information like password.

    Attributes:
        id_user: Unique identifier of the user.
        username: User's username.
        email: User's email address.
        role: User's role level.
        created_at: Timestamp when user was created.
        updated_at: Timestamp when user was last updated.
    """

    id_user: int
    username: str
    email: str
    role: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserService:
    """Service layer for user CRUD operations.

    This service uses UserRepo to interact with the database
    and implements business logic for user management including
    password hashing and role-based access control.
    """

    def __init__(self, db_session: Session):
        """Initialize the service with a database session.

        Args:
            db_session: SQLAlchemy database session.
        """
        self.repo = UserRepo(db_session)

    def get_all(self) -> List[User]:
        """Retrieve all users.

        Returns:
            List of all User objects.
        """
        return self.repo.get_all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            User object if found, None otherwise.
        """
        return self.repo.get_by_id(user_id)

    def create(self, user_data: UserCreate) -> User:
        """Create a new user with hashed password.

        Args:
            user_data: Data for the new user.

        Returns:
            Created User object.
        """
        hashed_pw = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_pw,
            role=user_data.role,
        )
        return self.repo.create(user)

    def update(
        self, user_id: int, user_data: UserUpdate, requester_role: int
    ) -> Optional[User]:
        """Update an existing user.

        Only superadmins (role=2) can modify user roles.

        Args:
            user_id: ID of the user to update.
            user_data: Updated user data.
            requester_role: Role of the user making the request.

        Returns:
            Updated User object if found, None otherwise.

        Raises:
            PermissionError: If non-superadmin tries to modify role.
        """
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.password is not None:
            user.password = pwd_context.hash(user_data.password)
        if user_data.role is not None:
            if requester_role < 2:
                raise PermissionError("Seul un superadmin peut modifier le rôle.")
            user.role = user_data.role
        return self.repo.update(user)

    def delete(self, user_id: int) -> bool:
        """Delete a user by their ID.

        Args:
            user_id: ID of the user to delete.

        Returns:
            True if deletion succeeded, False if user not found.
        """
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        return self.repo.delete(user)
