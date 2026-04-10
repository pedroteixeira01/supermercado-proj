from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.db import models
from app.db.repository import UserRepository, get_user_repo

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    user_repo: UserRepository = Depends(get_user_repo),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = user_repo.get_by_email(form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.UserMe)
def read_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return schemas.UserMe(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role.name if current_user.role else None,
    )
