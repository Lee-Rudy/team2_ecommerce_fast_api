from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.stock_movement import (
    StockMovementCreate,
    StockMovementResponse
)
from app.services.stock_movement_service import StockMovementService


router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock_movement(
    movement: StockMovementCreate,
    db: Session = Depends(get_db)
):
    return StockMovementService.create_stock_movement(db, movement)