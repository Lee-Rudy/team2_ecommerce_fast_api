from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_movement import (
    StockMovement,
    StockMovementCreate
)
from app.repositories.stock_movement_repo import StockMovementRepository


class StockMovementService:

    @staticmethod
    def create_stock_movement(
        db: Session,
        data: StockMovementCreate
    ):

        product = db.query(Product).filter(
            Product.id_product == data.id_product
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be > 0")

        if data.movement_type == "IN":
            product.stock_quantity += data.quantity

        elif data.movement_type == "OUT":

            if product.stock_quantity < data.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")

            product.stock_quantity -= data.quantity

        else:
            raise HTTPException(status_code=400, detail="Invalid movement type")

        movement = StockMovement(
            id_product=data.id_product,
            movement_type=data.movement_type,
            quantity=data.quantity
        )

        StockMovementRepository.create(db, movement)

        db.commit()
        db.refresh(product)
        db.refresh(movement)

        return movement

    @staticmethod
    def get_all_movements(db: Session):
        """Get all stock movements."""
        return StockMovementRepository.get_all(db)