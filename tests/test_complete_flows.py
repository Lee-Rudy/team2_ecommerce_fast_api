"""Tests de flux complets end-to-end."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_complete_category_workflow():
    """Test workflow complet catégorie."""
    create_resp = client.post(
        "/categories/", json={"name_category": "Flow1", "description_category": "D1"}
    )
    assert create_resp.status_code in [200, 201]

    if create_resp.status_code in [200, 201]:
        cat_id = create_resp.json()["id_category"]

        get_resp = client.get(f"/categories/{cat_id}")
        assert get_resp.status_code == 200

        update_resp = client.put(
            f"/categories/{cat_id}", json={"description_category": "Updated"}
        )
        assert update_resp.status_code == 200

        delete_resp = client.delete(f"/categories/{cat_id}")
        assert delete_resp.status_code == 200


def test_complete_product_workflow():
    """Test workflow complet produit."""
    cat_resp = client.post(
        "/categories/", json={"name_category": "FlowCat", "description_category": "D"}
    )

    if cat_resp.status_code in [200, 201]:
        cat_id = cat_resp.json()["id_category"]

        prod_resp = client.post(
            "/products/",
            json={
                "name_product": "FlowProduct",
                "brand": "FlowBrand",
                "price": 99.99,
                "stock_quantity": 50,
                "category_ids": [cat_id],
            },
        )

        if prod_resp.status_code in [200, 201]:
            prod_id = prod_resp.json()["id_product"]

            get_resp = client.get(f"/products/{prod_id}")
            assert get_resp.status_code == 200

            update_resp = client.put(
                f"/products/{prod_id}", json={"price": 149.99}
            )
            assert update_resp.status_code == 200

            stock_in = client.post(
                "/stock-movements/",
                json={
                    "id_product": prod_id,
                    "movement_type": "IN",
                    "quantity": 20,
                },
            )
            assert stock_in.status_code in [200, 201]

            stock_out = client.post(
                "/stock-movements/",
                json={
                    "id_product": prod_id,
                    "movement_type": "OUT",
                    "quantity": 10,
                },
            )
            assert stock_out.status_code in [200, 201]

            movements = client.get("/stock-movements/")
            assert movements.status_code == 200

            search_resp = client.get("/products/search?name=Flow")
            assert search_resp.status_code == 200

            filter_resp = client.get("/products/filter?in_stock=true&min_price=100")
            assert filter_resp.status_code == 200

            delete_resp = client.delete(f"/products/{prod_id}")
            assert delete_resp.status_code == 204


def test_create_product_with_invalid_category():
    """Test création produit avec catégorie invalide."""
    response = client.post(
        "/products/",
        json={
            "name_product": "Invalid",
            "brand": "B",
            "price": 10.0,
            "stock_quantity": 1,
            "category_ids": [99999],
        },
    )
    assert response.status_code == 404
