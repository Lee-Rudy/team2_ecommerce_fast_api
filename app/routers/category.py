from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.services.category_service import CategoryService, CategoryCreate, CategoryUpdate, CategoryRead
from app.models.category import Category

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# Dépendance pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints CRUD ---

@router.get("/", response_model=List[CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all()

@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    category = service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(category)

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    updated = service.update(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    success = service.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}