"""Tests d'intégration simples pour les endpoints API."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test endpoint racine."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories_list():
    """Test liste des catégories."""
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_products_list():
    """Test liste des produits."""
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_stock_movements_list():
    """Test liste des mouvements de stock."""
    response = client.get("/stock-movements/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_product_not_found():
    """Test produit inexistant retourne 404."""
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_category_not_found():
    """Test catégorie inexistante retourne 404."""
    response = client.get("/categories/99999")
    assert response.status_code == 404


def test_login_invalid_credentials():
    """Test login avec credentials invalides."""
    response = client.post(
        "/auth/login", json={"username": "invalid", "password": "wrong"}
    )
    assert response.status_code == 401


def test_users_list_unauthorized():
    """Test liste utilisateurs sans auth."""
    response = client.get("/users/", headers={"x-role": "0"})
    assert response.status_code == 403


def test_create_user_unauthorized():
    """Test création utilisateur sans superadmin."""
    response = client.post(
        "/users/",
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "pass",
            "role": 0,
        },
        headers={"x-role": "1"},
    )
    assert response.status_code == 403
