"""Product-Category association table.

This module defines the many-to-many relationship table
between products and categories.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column(
        "id_product",
        Integer,
        ForeignKey("products.id_product", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_category",
        Integer,
        ForeignKey("categories.id_category", ondelete="CASCADE"),
        primary_key=True,
    ),
)
