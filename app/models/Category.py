from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.database import Base

# --- SQLAlchemy ORM + Pydantic v2 ---
class Category(Base):
    __tablename__ = "categories"

    # ORM fields
    id_category = Column(Integer, primary_key=True, index=True)
    name_category = Column(String, nullable=False, unique=True)
    description_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    # Pydantic config pour validation + sérialisation
    model_config = {
        "from_attributes": True,  # permet de créer le modèle Pydantic depuis ORM
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id_category": 1,
                "name_category": "Électronique",
                "description_category": "Catégorie pour tous les produits électroniques",
                "created_at": "2026-03-11T12:00:00",
                "updated_at": "2026-03-11T12:00:00"
            }
        }
    }