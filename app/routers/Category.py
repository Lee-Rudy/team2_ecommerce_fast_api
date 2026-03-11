from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.CategoryService import (
    CategoryService,
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
)

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


def get_db():
    """Fournit une session DB pour les endpoints FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoints CRUD ---

@router.get("/", response_model=List[CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    """Retourne toutes les catégories."""
    service = CategoryService(db)
    return service.get_all()


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Retourne une catégorie par son ID."""
    service = CategoryService(db)
    category = service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle catégorie."""
    service = CategoryService(db)
    return service.create(category)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category: CategoryUpdate,
                    db: Session = Depends(get_db)):
    """Met à jour une catégorie existante."""
    service = CategoryService(db)
    updated = service.update(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Supprime une catégorie par son ID."""
    service = CategoryService(db)
    success = service.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}
