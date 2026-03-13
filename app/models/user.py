"""User model and database schema.

This module defines the User SQLAlchemy model for the users table.
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """SQLAlchemy model representing a user in the system.

    Attributes:
        id_user: Unique identifier for the user.
        username: Unique username for authentication.
        email: Unique email address.
        password: Hashed password for authentication.
        role: User role (0=user, 1=admin, 2=superadmin).
        created_at: Timestamp when user was created.
        updated_at: Timestamp when user was last updated.
    """

    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
