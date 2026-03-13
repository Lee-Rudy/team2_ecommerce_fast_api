"""Product model and schemas.

This module defines the Product SQLAlchemy model and related Pydantic schemas
for API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.product_category import product_categories


class Product(Base):
    """SQLAlchemy model representing a product in the catalog.

    This model defines the database table used to store product
    information in the e-commerce inventory system.

    Attributes:
        id_product (int): Unique identifier of the product.
        name_product (str): Name of the product.
        description_product (str): Description of the product.
        brand (str): Brand or manufacturer of the product.
        price (float): Price of the product.
        stock_quantity (int): Available quantity in stock.
        created_at (datetime): Timestamp when the product was created.
        updated_at (datetime): Timestamp when the product was last updated.
        categories: Relationship to categories through product_categories table.
    """

    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    name_product = Column(String, nullable=False, index=True)
    description_product = Column(String, nullable=True)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False, index=True)
    stock_quantity = Column(Integer, nullable=False, default=0, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    # Relationships
    stock_movements = relationship(
        "StockMovement", back_populates="product", cascade="all, delete"
    )

    categories = relationship(
        "Category", secondary=product_categories, back_populates="products"
    )


class ProductBase(BaseModel):
    """Base schema for product data.

    Attributes:
        name_product: Product name (2-100 characters).
        description_product: Optional product description.
        brand: Product brand or manufacturer.
        price: Product price (must be positive).
        stock_quantity: Available quantity in stock (non-negative).
    """

    name_product: str = Field(..., min_length=2, max_length=100)
    description_product: Optional[str] = None
    brand: str
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a new product.

    Attributes:
        category_ids: List of category IDs to associate with the product.
    """

    category_ids: Optional[list[int]] = Field(
        default=[], description="List of category IDs"
    )


class ProductUpdate(BaseModel):
    """Schema for updating an existing product.

    All fields are optional to allow partial updates.

    Attributes:
        name_product: Updated product name.
        description_product: Updated description.
        brand: Updated brand.
        price: Updated price.
        stock_quantity: Updated stock quantity.
        category_ids: Updated list of category IDs.
    """

    name_product: Optional[str] = None
    description_product: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_ids: Optional[list[int]] = None


class CategorySchema(BaseModel):
    """Schema for category information in product responses.

    Attributes:
        id_category: Category unique identifier.
        name_category: Category name.
        description_category: Optional category description.
    """

    id_category: int
    name_category: str
    description_category: Optional[str] = None

    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    """Schema for product API responses.

    Extends ProductBase with database-generated fields and relationships.

    Attributes:
        id_product: Unique identifier of the product.
        created_at: Timestamp when product was created.
        updated_at: Timestamp when product was last updated.
        categories: List of categories associated with the product.
    """

    id_product: int
    created_at: datetime
    updated_at: Optional[datetime]
    categories: list[CategorySchema] = []

    class Config:
        from_attributes = True
