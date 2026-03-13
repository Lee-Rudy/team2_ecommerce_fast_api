"""Tests for main application module.

Tests the main FastAPI application setup and root endpoint.
"""

from fastapi.testclient import TestClient

from app.main import app, build_status

client = TestClient(app)


def test_build_status():
    """Test build_status function returns correct format."""
    result = build_status()
    assert result == {"status": "ok"}
    assert isinstance(result, dict)


def test_root() -> None:
    """Test root endpoint returns status ok.

    Verifies that the / endpoint is accessible and returns
    the expected status response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
