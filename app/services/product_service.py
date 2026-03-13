from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import ProductCreate, ProductUpdate, Product
from app.repositories.product_repo import ProductRepository


class ProductService:
    """Service layer responsible for product business logic."""

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product."""
        return ProductRepository.create(db, product_data)

    @staticmethod
    def get_all_products(db: Session):
        """Retrieve all products."""
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        """Retrieve a product by its ID."""
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product:
        """Update an existing product."""
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return ProductRepository.update(db, product, product_data)

    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        """Delete a product."""
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        ProductRepository.delete(db, product)
