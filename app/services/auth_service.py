from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repositories.UserRepo import UserRepo as UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CHANGE_THIS_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    """Service responsible for authentication logic."""

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Generate a JWT access token.

        Args:
            data: Data to encode in the token.

        Returns:
            Encoded JWT token.
        """
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str
    ):
        """Authenticate a user.

        Args:
            db: Database session.
            username: Username provided by user.
            password: Password provided by user.

        Returns:
            Tuple containing user and token if authentication succeeds.
        """

        repo = UserRepository(db)
        user = repo.get_by_username(username)

        if not user:
            return None

        if not AuthService.verify_password(password, user.password):
            return None

        token = AuthService.create_access_token({
            "sub": user.username,
            "user_id": user.id_user,
            "role": user.role
        })

        return user, token