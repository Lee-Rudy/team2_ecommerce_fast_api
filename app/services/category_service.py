"""Category service and schemas.

This module provides the business logic layer for category operations
and defines Pydantic schemas for API interactions.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repo import CategoryRepo


class CategoryCreate(BaseModel):
    """Schema for creating a new category.

    Attributes:
        name_category: Name of the category.
        description_category: Optional description of the category.
    """

    name_category: str
    description_category: Optional[str] = None


class CategoryUpdate(BaseModel):
    """Schema for updating an existing category.

    All fields are optional to allow partial updates.

    Attributes:
        name_category: Updated category name.
        description_category: Updated category description.
    """

    name_category: Optional[str] = None
    description_category: Optional[str] = None


class CategoryRead(BaseModel):
    """Schema for reading category data in API responses.

    Attributes:
        id_category: Unique identifier of the category.
        name_category: Name of the category.
        description_category: Description of the category.
        created_at: Timestamp when category was created.
        updated_at: Timestamp when category was last updated.
    """

    id_category: int
    name_category: str
    description_category: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CategoryService:
    """Service layer for category CRUD operations.

    This service uses CategoryRepo to interact with the database
    and implements business logic for category management.
    """

    def __init__(self, db_session: Session):
        """Initialize the service with a database session.

        Args:
            db_session: SQLAlchemy database session.
        """
        self.repo = CategoryRepo(db_session)

    def get_all(self) -> List[Category]:
        """Retrieve all categories.

        Returns:
            List of all Category objects.
        """
        return self.repo.get_all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve a category by its ID.

        Args:
            category_id: Unique identifier of the category.

        Returns:
            Category object if found, None otherwise.
        """
        return self.repo.get_by_id(category_id)

    def create(self, category_data: CategoryCreate) -> Category:
        """Create a new category.

        Args:
            category_data: Data for the new category.

        Returns:
            Created Category object.
        """
        category = Category(
            name_category=category_data.name_category,
            description_category=category_data.description_category,
        )
        return self.repo.create(category)

    def update(
        self, category_id: int, category_data: CategoryUpdate
    ) -> Optional[Category]:
        """Update an existing category.

        Args:
            category_id: ID of the category to update.
            category_data: Updated category data.

        Returns:
            Updated Category object if found, None otherwise.
        """
        category = self.repo.get_by_id(category_id)
        if not category:
            return None
        if category_data.name_category is not None:
            setattr(category, "name_category", category_data.name_category)
        if category_data.description_category is not None:
            setattr(
                category, "description_category", category_data.description_category
            )
        return self.repo.update(category)

    def delete(self, category_id: int) -> bool:
        """Delete a category by its ID.

        Args:
            category_id: ID of the category to delete.

        Returns:
            True if deletion succeeded, False if category not found.
        """
        category = self.repo.get_by_id(category_id)
        if not category:
            return False
        return self.repo.delete(category)
