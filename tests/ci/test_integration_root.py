import httpx

from app.main import app


def test_root_integration_returns_ok():
    transport = httpx.ASGITransport(app=app)
    with httpx.Client(transport=transport, base_url="http://test") as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

