from sqlalchemy.orm import Session
from app.models.stock_movement import StockMovement


class StockMovementRepository:

    @staticmethod
    def create(db: Session, movement: StockMovement):
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement