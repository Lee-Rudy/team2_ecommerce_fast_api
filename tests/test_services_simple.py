"""Tests unitaires simples des services."""

from app.services.auth_service import AuthService
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_verify_password_correct():
    """Test vérification mot de passe correct."""
    plain = "testpassword"
    hashed = pwd_context.hash(plain)
    assert AuthService.verify_password(plain, hashed) is True


def test_verify_password_incorrect():
    """Test vérification mot de passe incorrect."""
    hashed = pwd_context.hash("correct")
    assert AuthService.verify_password("wrong", hashed) is False


def test_create_access_token():
    """Test création token JWT."""
    data = {"sub": "user", "user_id": 1}
    token = AuthService.create_access_token(data)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
