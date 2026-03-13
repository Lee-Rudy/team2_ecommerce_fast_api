"""Category model and database schema.

This module defines the Category SQLAlchemy model for product categorization.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.product_category import product_categories


class Category(Base):
    """SQLAlchemy model representing a product category.

    Categories are used to organize products into logical groups.
    Products can belong to multiple categories through the many-to-many
    relationship table.

    Attributes:
        id_category: Unique identifier for the category.
        name_category: Unique name of the category.
        description_category: Optional description of the category.
        created_at: Timestamp when category was created.
        updated_at: Timestamp when category was last updated.
        products: Relationship to products in this category.
    """

    __tablename__ = "categories"

    id_category = Column(Integer, primary_key=True, index=True)
    name_category = Column(String, nullable=False, unique=True)
    description_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    products = relationship(
        "Product", secondary=product_categories, back_populates="categories"
    )

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id_category": 1,
                "name_category": "Électronique",
                "description_category": (
                    "Catégorie pour tous les produits électroniques"
                ),
                "created_at": "2026-03-11T12:00:00",
                "updated_at": "2026-03-11T12:00:00",
            }
        },
    }
