"""Stock movement repository module.

This module provides database access layer for stock movement operations.
"""

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.stock_movement import StockMovement


class StockMovementRepository:
    """Repository for database operations on stock_movements table.

    Provides methods for creating and retrieving stock movement records.
    """

    @staticmethod
    def create(db: Session, movement: StockMovement):
        """Create a new stock movement in the database.

        Args:
            db: Database session.
            movement: StockMovement object to create.

        Returns:
            Created StockMovement object with generated ID.
        """
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_all(db: Session):
        """Retrieve all stock movements ordered by most recent first.

        Args:
            db: Database session.

        Returns:
            List of all StockMovement objects ordered by created_at desc.
        """
        return db.query(StockMovement).order_by(desc(StockMovement.created_at)).all()
