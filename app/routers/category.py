"""Category router module.

This module provides API endpoints for category CRUD operations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.category_service import (
    CategoryCreate,
    CategoryRead,
    CategoryService,
    CategoryUpdate,
)

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


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


@router.get("/", response_model=List[CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    """Retrieve all categories.

    Args:
        db: Database session (injected).

    Returns:
        List of all categories.
    """
    service = CategoryService(db)
    return service.get_all()


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve a single category by its ID.

    Args:
        category_id: Unique identifier of the category.
        db: Database session (injected).

    Returns:
        Category object.

    Raises:
        HTTPException: 404 if category not found.
    """
    service = CategoryService(db)
    category = service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category.

    Args:
        category: Category creation data.
        db: Database session (injected).

    Returns:
        Created category object.
    """
    service = CategoryService(db)
    return service.create(category)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    """Update an existing category.

    Args:
        category_id: ID of the category to update.
        category: Updated category data.
        db: Database session (injected).

    Returns:
        Updated category object.

    Raises:
        HTTPException: 404 if category not found.
    """
    service = CategoryService(db)
    updated = service.update(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category by its ID.

    Args:
        category_id: ID of the category to delete.
        db: Database session (injected).

    Returns:
        Success message.

    Raises:
        HTTPException: 404 if category not found.
    """
    service = CategoryService(db)
    success = service.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}
