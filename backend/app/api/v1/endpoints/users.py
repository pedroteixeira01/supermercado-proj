from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.core import security
from app.db import models
from app.db.repository import RoleRepository, UserRepository, get_role_repo, get_user_repo

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
    user_repo: UserRepository = Depends(get_user_repo),
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    return [_user_out(u) for u in user_repo.get_all()]


@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(
    *,
    user_repo: UserRepository = Depends(get_user_repo),
    role_repo: RoleRepository = Depends(get_role_repo),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    if user_repo.get_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user_role = role_repo.get_by_name("user")
    user = user_repo.create(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        role_id=user_role.id if user_role else None,
    )
    return _user_out(user)
