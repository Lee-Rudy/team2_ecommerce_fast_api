"""Category repository module.

This module provides database access layer for category operations.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepo:
    """Repository for database operations on categories table.

    Provides methods for CRUD operations and queries on Category entities.
    """

    def __init__(self, db_session: Session):
        """Initialize the repository with a database session.

        Args:
            db_session: SQLAlchemy database session.
        """
        self.db = db_session

    def get_all(self) -> List[Category]:
        """Retrieve all categories from the database.

        Returns:
            List of all Category objects.
        """
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve a category by its ID.

        Args:
            category_id: Unique identifier of the category.

        Returns:
            Category object if found, None otherwise.
        """
        return (
            self.db.query(Category).filter(Category.id_category == category_id).first()
        )

    def create(self, category: Category) -> Category:
        """Create a new category in the database.

        Args:
            category: Category object to create.

        Returns:
            Created Category object with generated ID.
        """
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        """Update an existing category in the database.

        Args:
            category: Category object with updated fields.

        Returns:
            Updated Category object.
        """
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> bool:
        """Delete a category from the database.

        Args:
            category: Category object to delete.

        Returns:
            True if deletion succeeded.
        """
        self.db.delete(category)
        self.db.commit()
        return True
