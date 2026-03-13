"""Stock movement model and schemas.

This module defines the StockMovement model for tracking inventory changes
and related Pydantic schemas for API requests and responses.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class StockMovement(Base):
    """SQLAlchemy model representing inventory movements.

    Tracks stock changes (IN/OUT) for products, maintaining an audit trail
    of all inventory modifications.

    Attributes:
        id_stock_movement: Unique identifier for the movement.
        id_product: Foreign key to the product.
        movement_type: Type of movement (IN for additions, OUT for removals).
        quantity: Quantity of items moved.
        created_at: Timestamp when movement was recorded.
        product: Relationship to the associated product.
    """

    __tablename__ = "stock_movements"

    id_stock_movement = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(
        Integer, ForeignKey("products.id_product", ondelete="CASCADE"), nullable=False
    )
    movement_type = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="stock_movements")


class StockMovementBase(BaseModel):
    """Base schema for stock movement data.

    Attributes:
        id_product: ID of the product being moved.
        movement_type: Type of movement (IN or OUT).
        quantity: Quantity being moved.
    """

    id_product: int
    movement_type: Literal["IN", "OUT"]
    quantity: int


class StockMovementCreate(StockMovementBase):
    """Schema for creating a new stock movement."""

    pass


class StockMovementResponse(StockMovementBase):
    """Schema for stock movement API responses.

    Attributes:
        id_stock_movement: Unique identifier of the movement.
        created_at: Timestamp when movement was created.
    """

    id_stock_movement: int
    created_at: datetime

    model_config = {"from_attributes": True}
