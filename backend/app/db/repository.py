from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import models
from app.db.database import get_db


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[models.User]:
        return self.db.query(models.User).all()

    def get_by_id(self, user_id: int) -> models.User | None:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, email: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def create(self, email: str, hashed_password: str, role_id: int | None) -> models.User:
        user = models.User(
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            role_id=role_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> models.Role | None:
        return self.db.query(models.Role).filter(models.Role.name == name).first()


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Product]:
        return self.db.query(models.Product).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int) -> models.Product | None:
        return self.db.query(models.Product).filter(models.Product.id == product_id).first()

    def get_categories(self) -> list[models.Category]:
        return self.db.query(models.Category).all()

    def create(self, data: dict) -> models.Product:
        product = models.Product(**data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, user_id: int, total_amount: float, items: list[models.OrderItem]
    ) -> models.Order:
        order = models.Order(
            user_id=user_id,
            total_amount=total_amount,
            status="completed",
        )
        self.db.add(order)
        self.db.flush()
        for item in items:
            item.order_id = order.id
            self.db.add(item)
        self.db.commit()
        self.db.refresh(order)
        return order


# --- Dependency factories ---

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repo(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_product_repo(db: Session = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_order_repo(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)
