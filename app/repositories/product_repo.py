from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.product import Product, ProductCreate, ProductUpdate
from app.models.category import Category


class ProductRepository:
    """Handles database operations for Product entities."""

    @staticmethod
    def create(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product in the database with categories."""
        # Extraire les category_ids avant de créer le produit
        category_ids = product_data.category_ids or []
        
        # Créer le produit sans les category_ids
        product_dict = product_data.model_dump(exclude={'category_ids'})
        product = Product(**product_dict)

        # Ajouter les catégories si fournies
        if category_ids:
            categories = db.query(Category).filter(
                Category.id_category.in_(category_ids)
            ).all()
            product.categories.extend(categories)

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all(db: Session):
        """Retrieve all products."""
        return db.query(Product).all()

    @staticmethod
    def search_by_name(db: Session, name: str):
        """Search products by name."""
        return db.query(Product).filter(
            Product.name_product.ilike(f"%{name}%")
        ).all()

    @staticmethod
    def filter_products(
            db: Session,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            in_stock: bool | None = None
    ):
        """Filter products according to given parameters.
        
        Args:
            db: Database session
            category_id: Filter by specific category ID
            min_price: Minimum price filter
            max_price: Maximum price filter
            in_stock: Filter for products with stock > 0
        
        Returns:
            List of filtered products
        """

        query = db.query(Product)

        if category_id:
            # Join with categories through product_categories
            query = query.join(Product.categories).filter(
                Category.id_category == category_id
            ).distinct()

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if in_stock:
            query = query.filter(Product.stock_quantity > 0)

        return query.all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        """Retrieve a product by its ID."""
        return (
            db.query(Product)
            .filter(Product.id_product == product_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
        product_data: ProductUpdate
    ) -> Product:
        """Update an existing product and its categories."""
        # Séparer les category_ids des autres données
        update_data = product_data.model_dump(exclude_unset=True)
        category_ids = update_data.pop('category_ids', None)

        # Mettre à jour les champs du produit
        for field, value in update_data.items():
            if value is not None:
                setattr(product, field, value)

        # Mettre à jour les catégories si fournies
        if category_ids is not None:
            # Récupérer les nouvelles catégories
            new_categories = db.query(Category).filter(
                Category.id_category.in_(category_ids)
            ).all()
            # Remplacer les catégories existantes
            product.categories = new_categories

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        """Delete a product from the database."""
        db.delete(product)
        db.commit()

    @staticmethod
    def add_category_to_product(
        db: Session,
        product_id: int,
        category_id: int
    ) -> Product:
        """Add a category to an existing product."""
        product = db.query(Product).filter(
            Product.id_product == product_id
        ).first()

        if product:
            category = db.query(Category).filter(
                Category.id_category == category_id
            ).first()

            if category and category not in product.categories:
                product.categories.append(category)
                db.commit()
                db.refresh(product)

        return product

    @staticmethod
    def remove_category_from_product(
        db: Session,
        product_id: int,
        category_id: int
    ) -> Product:
        """Remove a category from a product."""
        product = db.query(Product).filter(
            Product.id_product == product_id
        ).first()

        if product:
            category = db.query(Category).filter(
                Category.id_category == category_id
            ).first()

            if category and category in product.categories:
                product.categories.remove(category)
                db.commit()
                db.refresh(product)

        return product

    @staticmethod
    def get_products_by_category(db: Session, category_id: int):
        """Get all products belonging to a specific category."""
        return db.query(Product).join(Product.categories).filter(
            Category.id_category == category_id
        ).all()

    @staticmethod
    def search_by_category_and_name(
        db: Session,
        category_id: int,
        name: str
    ):
        """Search products by both category and name."""
        return db.query(Product).join(Product.categories).filter(
            and_(
                Category.id_category == category_id,
                Product.name_product.ilike(f"%{name}%")
            )
        ).all()