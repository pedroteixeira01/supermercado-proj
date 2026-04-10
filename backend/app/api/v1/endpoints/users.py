from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core import security
from app.db import models
from app.db.database import get_db

router = APIRouter()


def _user_out(user: models.User) -> schemas.UserOut:
    return schemas.UserOut(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        role=user.role.name if user.role else None,
    )


@router.get("/", response_model=List[schemas.UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    users = db.query(models.User).all()
    return [_user_out(u) for u in users]


@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user_role = db.query(models.Role).filter(models.Role.name == "user").first()

    user = models.User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=True,
        role_id=user_role.id if user_role else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _user_out(user)
