from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.User import User


class UserRepo:
    """Accès aux données pour la table users."""

    def __init__(self, db_session: Session):
        """Initialise le repository avec une session SQLAlchemy."""
        self.db = db_session

    def get_all(self) -> List[User]:
        """Retourne tous les utilisateurs."""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retourne un utilisateur par son ID."""
        return self.db.query(User).filter(User.id_user == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Retourne un utilisateur par son username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Retourne un utilisateur par son email."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        """Crée un nouvel utilisateur et le retourne."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Met à jour un utilisateur existant."""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        """Supprime un utilisateur et retourne True si réussi."""
        self.db.delete(user)
        self.db.commit()
        return True
