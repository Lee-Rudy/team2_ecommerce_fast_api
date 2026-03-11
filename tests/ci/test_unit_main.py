from app.main import build_status


def test_build_status_unit():
    assert build_status() == {"status": "ok"}
