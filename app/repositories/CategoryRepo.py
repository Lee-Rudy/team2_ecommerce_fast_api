from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.Category import Category


class CategoryRepo:
    """Accès aux données pour la table Category."""

    def __init__(self, db_session: Session):
        """Initialise le repository avec une session SQLAlchemy."""
        self.db = db_session

    def get_all(self) -> List[Category]:
        """Retourne toutes les catégories."""
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Retourne une catégorie par son ID."""
        return (
            self.db.query(Category)
            .filter(Category.id_category == category_id)
            .first()
        )

    def create(self, category: Category) -> Category:
        """Crée une nouvelle catégorie et la retourne."""
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        """Met à jour une catégorie existante."""
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> bool:
        """Supprime une catégorie et retourne True si réussi."""
        self.db.delete(category)
        self.db.commit()
        return True
