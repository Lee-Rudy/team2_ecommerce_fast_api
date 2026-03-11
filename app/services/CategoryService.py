from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.Category import Category
from app.repositories.CategoryRepo import CategoryRepo


# --- Pydantic schemas ---

class CategoryCreate(BaseModel):
    """Schéma pour la création d'une catégorie."""
    name_category: str
    description_category: Optional[str] = None


class CategoryUpdate(BaseModel):
    """Schéma pour la mise à jour d'une catégorie."""
    name_category: Optional[str] = None
    description_category: Optional[str] = None


class CategoryRead(BaseModel):
    """Schéma pour la lecture d'une catégorie."""
    id_category: int
    name_category: str
    description_category: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# --- Service CRUD ---

class CategoryService:
    """Service CRUD pour Category utilisant CategoryRepo."""

    def __init__(self, db_session: Session):
        self.repo = CategoryRepo(db_session)

    def get_all(self) -> List[Category]:
        """Retourne toutes les catégories."""
        return self.repo.get_all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Retourne une catégorie par son ID."""
        return self.repo.get_by_id(category_id)

    def create(self, category_data: CategoryCreate) -> Category:
        """Crée une nouvelle catégorie."""
        category = Category(
            name_category=category_data.name_category,
            description_category=category_data.description_category,
        )
        return self.repo.create(category)

    def update(self, category_id: int,
               category_data: CategoryUpdate) -> Optional[Category]:
        """Met à jour une catégorie existante."""
        category = self.repo.get_by_id(category_id)
        if not category:
            return None
        if category_data.name_category is not None:
            category.name_category = category_data.name_category
        if category_data.description_category is not None:
            category.description_category = category_data.description_category
        return self.repo.update(category)

    def delete(self, category_id: int) -> bool:
        """Supprime une catégorie par son ID."""
        category = self.repo.get_by_id(category_id)
        if not category:
            return False
        return self.repo.delete(category)
