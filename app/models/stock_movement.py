from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


# =========================
# SQLAlchemy Model
# =========================

class StockMovement(Base):

    __tablename__ = "stock_movements"

    id_stock_movement = Column(Integer, primary_key=True, autoincrement=True)

    id_product = Column(
        Integer,
        ForeignKey("products.id_product", ondelete="CASCADE"),
        nullable=False
    )

    movement_type = Column(Text, nullable=False)

    quantity = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    product = relationship("Product", back_populates="stock_movements")


# =========================
# Pydantic Schemas (comme Product)
# =========================

class StockMovementBase(BaseModel):
    id_product: int
    movement_type: Literal["IN", "OUT"]
    quantity: int


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id_stock_movement: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }