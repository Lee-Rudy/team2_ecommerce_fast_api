from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, DateTime
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
    """

    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    name_product = Column(String, nullable=False, index=True)
    description_product = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    categories = relationship(
        "Category",
        secondary=product_categories,
        back_populates="products"
    )

class ProductBase(BaseModel):
    """Base schema for product data."""

    name_product: str = Field(..., min_length=2, max_length=100)
    description_product: Optional[str] = None
    brand: str
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)

    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    """Schema used when creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema used when updating a product."""

    name_product: Optional[str] = None
    description_product: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None


class ProductResponse(ProductBase):
    """Schema returned in API responses."""

    id_product: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True