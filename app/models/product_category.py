from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column(
        "id_product",
        Integer,
        ForeignKey("products.id_product", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "id_category",
        Integer,
        ForeignKey("categories.id_category", ondelete="CASCADE"),
        primary_key=True
    ),
)