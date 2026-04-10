from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import models
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return [schemas.Product.from_orm(p) for p in products]


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Any:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product.from_orm(product)
