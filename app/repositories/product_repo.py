from sqlalchemy.orm import Session

from app.models.product import Product, ProductCreate, ProductUpdate


class ProductRepository:
    """Handles database operations for Product entities."""

    @staticmethod
    def create(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product in the database."""
        product = Product(**product_data.model_dump())

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all(db: Session):
        """Retrieve all products."""
        return db.query(Product).all()

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
        """Update an existing product."""
        update_data = product_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        """Delete a product from the database."""
        db.delete(product)
        db.commit()