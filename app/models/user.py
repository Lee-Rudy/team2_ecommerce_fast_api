from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class User(Base):
    """SQLAlchemy model representing a user."""

    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)