from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.db import models
from app.db.repository import OrderRepository, ProductRepository, get_order_repo, get_product_repo

router = APIRouter()


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    order_repo: OrderRepository = Depends(get_order_repo),
    product_repo: ProductRepository = Depends(get_product_repo),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    total_amount = 0.0
    items = []

    for item in order_in.items:
        product = product_repo.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )
        total_amount += product.price * item.quantity
        items.append(
            models.OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
        )

    return order_repo.create(current_user.id, total_amount, items)
