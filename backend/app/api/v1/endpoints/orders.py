from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.db import models
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order for the current logged in user.
    """
    total_amount = 0.0
    items_to_create = []

    for item in order_in.items:
        product = (
            db.query(models.Product)
            .filter(models.Product.id == item.product_id)
            .first()
        )
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )

        unit_price = product.price
        total_amount += unit_price * item.quantity

        items_to_create.append(
            models.OrderItem(
                product_id=product.id, quantity=item.quantity, unit_price=unit_price
            )
        )

    order = models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="completed",
    )
    db.add(order)
    db.flush()

    for item in items_to_create:
        item.order_id = order.id
        db.add(item)

    db.commit()
    db.refresh(order)
    return order
