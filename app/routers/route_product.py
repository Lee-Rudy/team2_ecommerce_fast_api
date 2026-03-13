"""Product router module.

This module provides API endpoints for product CRUD operations,
search, and filtering functionality.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


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


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="List all products",
    description="Retrieve all products from the catalog.",
)
def get_products(db: Session = Depends(get_db)):
    """Retrieve all products with their categories.

    Args:
        db: Database session (injected).

    Returns:
        List of all products.
    """
    return ProductService.get_all_products(db)


@router.get("/search")
def search_products(name: str, db: Session = Depends(get_db)):
    """Search products by name using case-insensitive matching.

    Args:
        name: Search term for product name.
        db: Database session (injected).

    Returns:
        List of matching products.
    """
    return ProductService.search_products(db, name)


@router.get("/filter")
def filter_products(
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
    db: Session = Depends(get_db),
):
    """Filter products by category, price range, and stock status.

    Args:
        category_id: Filter by category ID.
        min_price: Minimum price threshold.
        max_price: Maximum price threshold.
        in_stock: Filter for in-stock items only.
        db: Database session (injected).

    Returns:
        List of products matching the criteria.
    """
    return ProductService.filter_products(
        db, category_id, min_price, max_price, in_stock
    )


@router.get(
    "/{product_id}", response_model=ProductResponse, summary="Get product by ID"
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by its ID.

    Args:
        product_id: Unique identifier of the product.
        db: Database session (injected).

    Returns:
        Product object with categories.

    Raises:
        HTTPException: 404 if product not found.
    """
    return ProductService.get_product_by_id(db, product_id)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product in the catalog.

    Args:
        product: Product creation data including category IDs.
        db: Database session (injected).

    Returns:
        Created product object.

    Raises:
        HTTPException: 404 if any category ID is invalid.
    """
    return ProductService.create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse, summary="Update a product")
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    """Update an existing product.

    Args:
        product_id: ID of the product to update.
        product: Updated product data.
        db: Database session (injected).

    Returns:
        Updated product object.

    Raises:
        HTTPException: 404 if product or category not found.
    """
    return ProductService.update_product(db, product_id, product)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from the catalog.

    Args:
        product_id: ID of the product to delete.
        db: Database session (injected).

    Raises:
        HTTPException: 404 if product not found.
    """
    ProductService.delete_product(db, product_id)
