from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import Base
from app.services.product_service import ProductService
from app.database import SessionLocal
from app.models.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProductResponse], summary="List all products", description="Retrieve all products from the catalog.")
def get_products(db: Session = Depends(get_db)):
    """Retrieve all products."""
    return ProductService.get_all_products(db)

@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by its ID."""
    return ProductService.get_product_by_id(db, product_id)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Create a new product")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product in the catalog."""
    return ProductService.create_product(db, product)

@router.put("/{product_id}", response_model=ProductResponse, summary="Update a product")
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update an existing product."""
    return ProductService.update_product(db, product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from the catalog."""
    ProductService.delete_product(db, product_id)
