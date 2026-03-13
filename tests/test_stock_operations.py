"""Tests simples des mouvements de stock."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_stock_movement_product_not_found():
    """Test mouvement pour produit inexistant."""
    response = client.post(
        "/stock-movements/",
        json={"id_product": 99999, "movement_type": "IN", "quantity": 10},
    )
    assert response.status_code == 404


def test_create_stock_movement_invalid_quantity():
    """Test mouvement avec quantité invalide."""
    response = client.post(
        "/stock-movements/",
        json={"id_product": 1, "movement_type": "IN", "quantity": 0},
    )
    assert response.status_code in [400, 404]


def test_create_stock_movement_insufficient_stock():
    """Test mouvement OUT avec stock insuffisant."""
    client.post(
        "/products/",
        json={
            "name_product": "LowStock",
            "brand": "B",
            "price": 10.0,
            "stock_quantity": 2,
            "category_ids": [],
        },
    )

    response = client.post(
        "/stock-movements/",
        json={"id_product": 1, "movement_type": "OUT", "quantity": 1000},
    )
    assert response.status_code in [400, 404]
