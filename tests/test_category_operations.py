"""Tests simples des opérations catégories."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_category_simple():
    """Test création catégorie."""
    response = client.post(
        "/categories/", json={"name_category": "TestCat", "description_category": "D"}
    )
    assert response.status_code in [200, 201]
    if response.status_code in [200, 201]:
        data = response.json()
        assert data["name_category"] == "TestCat"
        cat_id = data["id_category"]

        get_response = client.get(f"/categories/{cat_id}")
        assert get_response.status_code == 200

        update_response = client.put(
            f"/categories/{cat_id}", json={"description_category": "Updated"}
        )
        assert update_response.status_code == 200

        delete_response = client.delete(f"/categories/{cat_id}")
        assert delete_response.status_code == 200


def test_update_category_not_found():
    """Test update catégorie inexistante."""
    response = client.put("/categories/99999", json={"name_category": "Test"})
    assert response.status_code == 404


def test_delete_category_not_found():
    """Test delete catégorie inexistante."""
    response = client.delete("/categories/99999")
    assert response.status_code == 404
