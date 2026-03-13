"""Product repository module.

This module provides database access layer for product operations
including CRUD, filtering, and category management.
"""

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product, ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for database operations on products table.

    Provides methods for CRUD operations, filtering, and category
    association management for Product entities.
    """

    @staticmethod
    def create(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product in the database with categories.

        Args:
            db: Database session.
            product_data: Product creation data including category_ids.

        Returns:
            Created Product object with associated categories.
        """
        category_ids = product_data.category_ids or []
        product_dict = product_data.model_dump(exclude={"category_ids"})
        product = Product(**product_dict)

        if category_ids:
            categories = (
                db.query(Category).filter(Category.id_category.in_(category_ids)).all()
            )
            product.categories.extend(categories)

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all(db: Session):
        """Retrieve all products from the database.

        Args:
            db: Database session.

        Returns:
            List of all Product objects.
        """
        return db.query(Product).all()

    @staticmethod
    def search_by_name(db: Session, name: str):
        """Search products by name using case-insensitive matching.

        Args:
            db: Database session.
            name: Search term for product name.

        Returns:
            List of matching Product objects.
        """
        return db.query(Product).filter(Product.name_product.ilike(f"%{name}%")).all()

    @staticmethod
    def filter_products(
        db: Session,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool | None = None,
    ):
        """Filter products according to given parameters.

        Args:
            db: Database session.
            category_id: Filter by specific category ID.
            min_price: Minimum price threshold.
            max_price: Maximum price threshold.
            in_stock: Filter for products with stock > 0.

        Returns:
            List of Product objects matching the criteria.
        """
        query = db.query(Product)

        if category_id:
            query = (
                query.join(Product.categories)
                .filter(Category.id_category == category_id)
                .distinct()
            )

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if in_stock:
            query = query.filter(Product.stock_quantity > 0)

        return query.all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        """Retrieve a product by its ID.

        Args:
            db: Database session.
            product_id: Unique identifier of the product.

        Returns:
            Product object if found, None otherwise.
        """
        return db.query(Product).filter(Product.id_product == product_id).first()

    @staticmethod
    def update(db: Session, product: Product, product_data: ProductUpdate) -> Product:
        """Update an existing product and its categories.

        Args:
            db: Database session.
            product: Product object to update.
            product_data: Updated product data.

        Returns:
            Updated Product object.
        """
        update_data = product_data.model_dump(exclude_unset=True)
        category_ids = update_data.pop("category_ids", None)

        for field, value in update_data.items():
            if value is not None:
                setattr(product, field, value)

        if category_ids is not None:
            new_categories = (
                db.query(Category).filter(Category.id_category.in_(category_ids)).all()
            )
            product.categories = new_categories

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        """Delete a product from the database.

        Args:
            db: Database session.
            product: Product object to delete.
        """
        db.delete(product)
        db.commit()

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
        """
        product = db.query(Product).filter(Product.id_product == product_id).first()

        if product:
            category = (
                db.query(Category).filter(Category.id_category == category_id).first()
            )

            if category and category not in product.categories:
                product.categories.append(category)
                db.commit()
                db.refresh(product)

        return product

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
        """
        product = db.query(Product).filter(Product.id_product == product_id).first()

        if product:
            category = (
                db.query(Category).filter(Category.id_category == category_id).first()
            )

            if category and category in product.categories:
                product.categories.remove(category)
                db.commit()
                db.refresh(product)

        return product

    @staticmethod
    def get_products_by_category(db: Session, category_id: int):
        """Get all products belonging to a specific category.

        Args:
            db: Database session.
            category_id: ID of the category.

        Returns:
            List of Product objects in the category.
        """
        return (
            db.query(Product)
            .join(Product.categories)
            .filter(Category.id_category == category_id)
            .all()
        )

    @staticmethod
    def search_by_category_and_name(db: Session, category_id: int, name: str):
        """Search products by both category and name.

        Args:
            db: Database session.
            category_id: ID of the category to search within.
            name: Product name search term.

        Returns:
            List of matching Product objects.
        """
        return (
            db.query(Product)
            .join(Product.categories)
            .filter(
                and_(
                    Category.id_category == category_id,
                    Product.name_product.ilike(f"%{name}%"),
                )
            )
            .all()
        )
