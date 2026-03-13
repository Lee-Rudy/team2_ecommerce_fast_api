"""Tests simples des opérations utilisateurs."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_users_list_as_admin():
    """Test liste utilisateurs en tant qu'admin."""
    response = client.get("/users/", headers={"x-role": "1"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id_not_found():
    """Test get utilisateur inexistant."""
    response = client.get("/users/99999", headers={"x-role": "2"})
    assert response.status_code == 404


def test_create_user_as_superadmin():
    """Test création utilisateur en tant que superadmin."""
    response = client.post(
        "/users/",
        json={
            "username": "testuser123",
            "email": "test123@example.com",
            "password": "pass123",
            "role": 0,
        },
        headers={"x-role": "2"},
    )
    assert response.status_code in [200, 201]
    if response.status_code in [200, 201]:
        user_id = response.json()["id_user"]

        update_response = client.put(
            f"/users/{user_id}",
            json={"username": "updated_user"},
            headers={"x-role": "1"},
        )
        assert update_response.status_code == 200

        delete_response = client.delete(f"/users/{user_id}", headers={"x-role": "2"})
        assert delete_response.status_code == 200


def test_update_user_not_found():
    """Test update utilisateur inexistant."""
    response = client.put(
        "/users/99999", json={"username": "test"}, headers={"x-role": "2"}
    )
    assert response.status_code == 404


def test_delete_user_not_found():
    """Test delete utilisateur inexistant."""
    response = client.delete("/users/99999", headers={"x-role": "2"})
    assert response.status_code == 404


def test_update_user_role_permission_error():
    """Test update role utilisateur sans permission."""
    response = client.put("/users/1", json={"role": 2}, headers={"x-role": "1"})
    assert response.status_code in [403, 404]
