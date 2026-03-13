"""Product service module.

This module provides the business logic layer for product operations
including CRUD operations, filtering, and category management.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product, ProductCreate, ProductUpdate
from app.repositories.product_repo import ProductRepository


class ProductService:
    """Service layer responsible for product business logic.

    This service implements business rules and coordinates between
    repositories and API endpoints for product operations.
    """

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product with associated categories.

        Args:
            db: Database session.
            product_data: Product creation data including category_ids.

        Returns:
            Created Product object with its categories.

        Raises:
            HTTPException: If any category ID is not found.
        """
        if product_data.category_ids:
            categories = (
                db.query(Category)
                .filter(Category.id_category.in_(product_data.category_ids))
                .all()
            )

            if len(categories) != len(product_data.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found",
                )

        return ProductRepository.create(db, product_data)

    @staticmethod
    def get_all_products(db: Session):
        """Retrieve all products with their categories.

        Args:
            db: Database session.

        Returns:
            List of all Product objects.
        """
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        """Retrieve a product by its ID with its categories.

        Args:
            db: Database session.
            product_id: ID of the product to retrieve.

        Returns:
            Product object with its categories.

        Raises:
            HTTPException: If product is not found.
        """
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    @staticmethod
    def search_products(db: Session, name: str):
        """Search products by name using case-insensitive matching.

        Args:
            db: Database session.
            name: Search term for product name.

        Returns:
            List of matching Product objects.
        """
        return ProductRepository.search_by_name(db, name)

    @staticmethod
    def filter_products(
        db: Session,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool | None = None,
    ):
        """Filter products by various criteria.

        Args:
            db: Database session.
            category_id: Filter by specific category ID.
            min_price: Minimum price threshold.
            max_price: Maximum price threshold.
            in_stock: Filter for in-stock items only (stock > 0).

        Returns:
            List of Product objects matching the criteria.
        """
        return ProductRepository.filter_products(
            db, category_id, min_price, max_price, in_stock
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product:
        """Update an existing product and its categories.

        Args:
            db: Database session.
            product_id: ID of product to update.
            product_data: Updated product data.

        Returns:
            Updated Product object.

        Raises:
            HTTPException: If product not found or category IDs invalid.
        """
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if product_data.category_ids:
            categories = (
                db.query(Category)
                .filter(Category.id_category.in_(product_data.category_ids))
                .all()
            )

            if len(categories) != len(product_data.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found",
                )

        return ProductRepository.update(db, product, product_data)

    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        """Delete a product from the catalog.

        Args:
            db: Database session.
            product_id: ID of product to delete.

        Raises:
            HTTPException: If product not found.
        """
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        ProductRepository.delete(db, product)

    @staticmethod
    def add_category_to_product(
        db: Session, product_id: int, category_id: int
    ) -> Product:
        """Add a category to an existing product.

        Args:
            db: Database session.
            product_id: ID of the product.
            category_id: ID of the category to add.

        Returns:
            Updated Product object.

        Raises:
            HTTPException: If product or category not found.
        """
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        category = (
            db.query(Category).filter(Category.id_category == category_id).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return ProductRepository.add_category_to_product(db, product_id, category_id)

    @staticmethod
    def remove_category_from_product(
        db: Session, product_id: int, category_id: int
    ) -> Product:
        """Remove a category from a product.

        Args:
            db: Database session.
            product_id: ID of the product.
            category_id: ID of the category to remove.

        Returns:
            Updated Product object.

        Raises:
            HTTPException: If product or category not found.
        """
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        category = (
            db.query(Category).filter(Category.id_category == category_id).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return ProductRepository.remove_category_from_product(
            db, product_id, category_id
        )

    @staticmethod
    def get_products_by_category(db: Session, category_id: int):
        """Get all products in a specific category.

        Args:
            db: Database session.
            category_id: ID of the category.

        Returns:
            List of Product objects in the category.

        Raises:
            HTTPException: If category not found.
        """
        category = (
            db.query(Category).filter(Category.id_category == category_id).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return ProductRepository.get_products_by_category(db, category_id)

    @staticmethod
    def search_by_category_and_name(db: Session, category_id: int, name: str):
        """Search products by category and name.

        Args:
            db: Database session.
            category_id: ID of the category to search within.
            name: Product name search term.

        Returns:
            List of matching Product objects.

        Raises:
            HTTPException: If category not found.
        """
        category = (
            db.query(Category).filter(Category.id_category == category_id).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return ProductRepository.search_by_category_and_name(db, category_id, name)
