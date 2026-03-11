from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.Category import Category
from app.repositories.CategoryRepo import CategoryRepo
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryCreate(BaseModel):
    name_category: str
    description_category: Optional[str] = None

class CategoryUpdate(BaseModel):
    name_category: Optional[str] = None
    description_category: Optional[str] = None

class CategoryRead(BaseModel):
    id_category: int
    name_category: str
    description_category: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

class CategoryService:
    """Service CRUD pour Category avec repository."""

    def __init__(self, db_session: Session):
        self.repo = CategoryRepo(db_session)

    def get_all(self) -> List[Category]:
        return self.repo.get_all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.repo.get_by_id(category_id)

    def create(self, category_data: CategoryCreate) -> Category:
        category = Category(
            name_category=category_data.name_category,
            description_category=category_data.description_category
        )
        return self.repo.create(category)

    def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = self.repo.get_by_id(category_id)
        if not category:
            return None
        if category_data.name_category is not None:
            category.name_category = category_data.name_category
        if category_data.description_category is not None:
            category.description_category = category_data.description_category
        return self.repo.update(category)

    def delete(self, category_id: int) -> bool:
        category = self.repo.get_by_id(category_id)
        if not category:
            return False
        return self.repo.delete(category)