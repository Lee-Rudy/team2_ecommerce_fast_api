from typing import List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.UserService import (
    UserService,
    UserCreate,
    UserUpdate,
    UserRead,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_db():
    """Fournit une session DB pour les endpoints FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(x_role: int = Header(...)):
    """
    Guard : l'appelant doit être admin (role >= 1) ou superadmin (role >= 2).
    En production, remplacer ce header par un token JWT vérifié.
    """
    if x_role < 1:
        raise HTTPException(status_code=403, detail="Accès réservé aux admins.")
    return x_role


def require_superadmin(x_role: int = Header(...)):
    """Guard : l'appelant doit être superadmin (role == 2)."""
    if x_role < 2:
        raise HTTPException(status_code=403, detail="Accès réservé aux superadmins.")
    return x_role


# --- Endpoints CRUD ---

@router.get("/", response_model=List[UserRead])
def read_users(
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """[Admin+] Retourne tous les utilisateurs."""
    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """[Admin+] Retourne un utilisateur par son ID."""
    service = UserService(db)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    role: int = Depends(require_superadmin),
):
    """[Superadmin] Crée un nouvel utilisateur."""
    service = UserService(db)
    return service.create(user)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    role: int = Depends(require_admin),
):
    """
    [Admin+] Met à jour un utilisateur.
    La modification du rôle est réservée au superadmin.
    """
    service = UserService(db)
    try:
        updated = service.update(user_id, user, requester_role=role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    role: int = Depends(require_superadmin),
):
    """[Superadmin] Supprime un utilisateur par son ID."""
    service = UserService(db)
    success = service.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
