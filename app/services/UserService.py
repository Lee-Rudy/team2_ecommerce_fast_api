from datetime import datetime
from typing import List, Optional

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.models.User import User
from app.repositories.UserRepo import UserRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Pydantic schemas ---

class UserCreate(BaseModel):
    """Schéma pour la création d'un utilisateur."""
    username: str
    email: EmailStr
    password: str
    role: Optional[int] = 0  # 0=user, 1=admin, 2=superadmin


class UserUpdate(BaseModel):
    """Schéma pour la mise à jour d'un utilisateur."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[int] = None


class UserRead(BaseModel):
    """Schéma pour la lecture d'un utilisateur (sans le mot de passe)."""
    id_user: int
    username: str
    email: str
    role: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# --- Service CRUD ---

class UserService:
    """Service CRUD pour User utilisant UserRepo."""

    def __init__(self, db_session: Session):
        self.repo = UserRepo(db_session)

    def get_all(self) -> List[User]:
        """Retourne tous les utilisateurs."""
        return self.repo.get_all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retourne un utilisateur par son ID."""
        return self.repo.get_by_id(user_id)

    def create(self, user_data: UserCreate) -> User:
        """Crée un nouvel utilisateur avec le mot de passe hashé."""
        hashed_pw = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_pw,
            role=user_data.role,
        )
        return self.repo.create(user)

    def update(self, user_id: int, user_data: UserUpdate,
               requester_role: int) -> Optional[User]:
        """
        Met à jour un utilisateur.
        Seul un superadmin (role=2) peut modifier le rôle.
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
        """Supprime un utilisateur par son ID."""
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        return self.repo.delete(user)
