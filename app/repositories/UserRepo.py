"""User repository module.

This module provides database access layer for user operations.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepo:
    """Repository for database operations on users table.

    Provides methods for CRUD operations and queries on User entities.
    """

    def __init__(self, db_session: Session):
        """Initialize the repository with a database session.

        Args:
            db_session: SQLAlchemy database session.
        """
        self.db = db_session

    def get_all(self) -> List[User]:
        """Retrieve all users from the database.

        Returns:
            List of all User objects.
        """
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            User object if found, None otherwise.
        """
        return self.db.query(User).filter(User.id_user == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username.

        Args:
            username: Username to search for.

        Returns:
            User object if found, None otherwise.
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.

        Args:
            email: Email address to search for.

        Returns:
            User object if found, None otherwise.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        """Create a new user in the database.

        Args:
            user: User object to create.

        Returns:
            Created User object with generated ID.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Update an existing user in the database.

        Args:
            user: User object with updated fields.

        Returns:
            Updated User object.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        """Delete a user from the database.

        Args:
            user: User object to delete.

        Returns:
            True if deletion succeeded.
        """
        self.db.delete(user)
        self.db.commit()
        return True
