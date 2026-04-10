from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.db import models
from app.db.repository import ProductRepository, get_product_repo

router = APIRouter()


@router.get("/categories")
def read_categories(
    product_repo: ProductRepository = Depends(get_product_repo),
) -> Any:
    return [{"id": c.id, "name": c.name} for c in product_repo.get_categories()]


@router.get("/", response_model=List[schemas.Product])
def read_products(
    product_repo: ProductRepository = Depends(get_product_repo),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return [schemas.Product.from_orm(p) for p in product_repo.get_all(skip, limit)]


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    product_repo: ProductRepository = Depends(get_product_repo),
) -> Any:
    product = product_repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product.from_orm(product)


@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    product_repo: ProductRepository = Depends(get_product_repo),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    return schemas.Product.from_orm(product_repo.create(product_in.model_dump()))
