"""Tests simples des schémas Pydantic."""

import pytest
from pydantic import ValidationError

from app.models.product import ProductBase, ProductCreate, ProductUpdate
from app.models.stock_movement import StockMovementCreate
from app.services.category_service import CategoryCreate
from app.services.UserService import UserCreate


def test_product_base_valid():
    """Test schéma ProductBase valide."""
    product = ProductBase(
        name_product="Test", brand="Brand", price=10.0, stock_quantity=5
    )
    assert product.name_product == "Test"
    assert product.price == 10.0


def test_product_base_invalid_price():
    """Test ProductBase rejette prix négatif."""
    with pytest.raises(ValidationError):
        ProductBase(name_product="Test", brand="Brand", price=-10.0, stock_quantity=5)


def test_product_create_with_categories():
    """Test ProductCreate avec catégories."""
    product = ProductCreate(
        name_product="Test",
        brand="Brand",
        price=10.0,
        stock_quantity=5,
        category_ids=[1, 2],
    )
    assert product.category_ids == [1, 2]


def test_product_update_partial():
    """Test ProductUpdate permet mise à jour partielle."""
    update = ProductUpdate(price=29.99)
    assert update.price == 29.99
    assert update.name_product is None


def test_user_create_valid():
    """Test UserCreate valide."""
    user = UserCreate(
        username="test", email="test@example.com", password="pass123", role=0
    )
    assert user.username == "test"
    assert user.email == "test@example.com"


def test_user_create_invalid_email():
    """Test UserCreate rejette email invalide."""
    with pytest.raises(ValidationError):
        UserCreate(username="test", email="invalid-email", password="pass123")


def test_category_create_valid():
    """Test CategoryCreate valide."""
    category = CategoryCreate(name_category="Test", description_category="Desc")
    assert category.name_category == "Test"


def test_stock_movement_create_valid():
    """Test StockMovementCreate valide."""
    movement = StockMovementCreate(id_product=1, movement_type="IN", quantity=10)
    assert movement.movement_type == "IN"
    assert movement.quantity == 10


def test_stock_movement_invalid_type():
    """Test StockMovementCreate rejette type invalide."""
    with pytest.raises(ValidationError):
        StockMovementCreate(id_product=1, movement_type="INVALID", quantity=10)
