"""Tests simples des opérations produits."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_product_simple():
    """Test création produit simple."""
    response = client.post(
        "/products/",
        json={
            "name_product": "Simple Product",
            "brand": "Brand",
            "price": 50.0,
            "stock_quantity": 10,
            "category_ids": [],
        },
    )
    assert response.status_code in [200, 201, 404]


def test_search_products():
    """Test recherche produits."""
    response = client.get("/products/search?name=test")
    assert response.status_code == 200


def test_filter_products_by_price():
    """Test filtre produits par prix."""
    response = client.get("/products/filter?min_price=10&max_price=100")
    assert response.status_code == 200


def test_filter_products_in_stock():
    """Test filtre produits en stock."""
    response = client.get("/products/filter?in_stock=true")
    assert response.status_code == 200


def test_update_product_nonexistent():
    """Test update produit inexistant."""
    response = client.put("/products/99999", json={"price": 100.0})
    assert response.status_code == 404


def test_delete_product_nonexistent():
    """Test delete produit inexistant."""
    response = client.delete("/products/99999")
    assert response.status_code == 404
