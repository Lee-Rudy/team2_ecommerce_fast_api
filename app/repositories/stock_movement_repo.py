from sqlalchemy.orm import Session
from app.models.stock_movement import StockMovement
from sqlalchemy import desc

class StockMovementRepository:

    @staticmethod
    def create(db: Session, movement: StockMovement):
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_all(db: Session):
        """Get all movements (most recent first)."""
        return db.query(StockMovement).order_by(
            desc(StockMovement.created_at)
        ).all()