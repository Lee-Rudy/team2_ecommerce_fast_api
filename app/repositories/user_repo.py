from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """Repository responsible for user database operations."""

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        """Retrieve a user by username.

        Args:
            db: Database session.
            username: Username to search.

        Returns:
            User if found, otherwise None.
        """
        return db.query(User).filter(User.username == username).first()