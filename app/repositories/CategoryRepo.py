from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.Category import Category

class CategoryRepo:
    """Accès aux données Category."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id_category == category_id).first()

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> bool:
        self.db.delete(category)
        self.db.commit()
        return True