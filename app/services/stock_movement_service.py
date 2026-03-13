"""Stock movement service module.

This module provides the business logic for stock movement operations
including inventory adjustments and movement tracking.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_movement import StockMovement, StockMovementCreate
from app.repositories.stock_movement_repo import StockMovementRepository


class StockMovementService:
    """Service layer for stock movement operations.

    Handles business logic for recording and retrieving inventory movements,
    including stock validation and product quantity updates.
    """

    @staticmethod
    def create_stock_movement(db: Session, data: StockMovementCreate):
        """Create a new stock movement and update product inventory.

        Args:
            db: Database session.
            data: Stock movement creation data.

        Returns:
            Created StockMovement object.

        Raises:
            HTTPException: If product not found, quantity invalid,
                or insufficient stock for OUT movements.
        """
        product = (
            db.query(Product).filter(Product.id_product == data.id_product).first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be > 0")

        if data.movement_type == "IN":
            new_qty = product.stock_quantity + data.quantity
            setattr(product, "stock_quantity", new_qty)

        elif data.movement_type == "OUT":
            if product.stock_quantity < data.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")
            new_qty = product.stock_quantity - data.quantity
            setattr(product, "stock_quantity", new_qty)

        else:
            raise HTTPException(status_code=400, detail="Invalid movement type")

        movement = StockMovement(
            id_product=data.id_product,
            movement_type=data.movement_type,
            quantity=data.quantity,
        )

        StockMovementRepository.create(db, movement)

        db.commit()
        db.refresh(product)
        db.refresh(movement)

        return movement

    @staticmethod
    def get_all_movements(db: Session):
        """Retrieve all stock movements ordered by most recent first.

        Args:
            db: Database session.

        Returns:
            List of all StockMovement objects.
        """
        return StockMovementRepository.get_all(db)
