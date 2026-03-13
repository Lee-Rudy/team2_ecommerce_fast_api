"""Stock movement router module.

This module provides API endpoints for stock movement operations
including recording inventory changes and retrieving movement history.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.stock_movement import StockMovementCreate, StockMovementResponse
from app.services.stock_movement_service import StockMovementService

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


def get_db():
    """Provide database session for dependency injection.

    Yields:
        SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED
)
def create_stock_movement(movement: StockMovementCreate, db: Session = Depends(get_db)):
    """Record a new stock movement and update product inventory.

    Args:
        movement: Stock movement data (product_id, type, quantity).
        db: Database session (injected).

    Returns:
        Created stock movement record.

    Raises:
        HTTPException: 404 if product not found, 400 for invalid data.
    """
    return StockMovementService.create_stock_movement(db, movement)


@router.get("/", response_model=list[StockMovementResponse])
def get_all_movements(db: Session = Depends(get_db)):
    """Retrieve all stock movements ordered by most recent first.

    Args:
        db: Database session (injected).

    Returns:
        List of all stock movements.
    """
    return StockMovementService.get_all_movements(db)
