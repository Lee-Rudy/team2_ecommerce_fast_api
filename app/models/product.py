import datetime
from pydantic import BaseModel
"""Represents a product.

    This model defines the structure of a product.

    Attributes:
        id_product (int): Unique identifier of the product.
        product_name (str): Name of the product.
        product_description (str): Detailed description of the product.
        brand (str): Brand or manufacturer of the product.
        price (float): Price of the product.
        stock_quantity (int): Available quantity of the product in stock.
        created_at (datetime): Date and time when the product was created.
        updated_at (datetime): Date and time when the product was last updated.
"""
class Product(BaseModel):
    id_product: int
    product_name: str
    product_description: str
    brand: str
    price: float
    stock_quantity: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
