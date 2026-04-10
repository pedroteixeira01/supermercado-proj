from typing import Any, Optional

from pydantic import BaseModel

from app.db.models import Product as ProductModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


class Product(ProductBase):
    id: int
    category: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj: Any) -> "Product":
        if isinstance(obj, ProductModel):
            category_name = obj.category.name if obj.category else None
            return cls(
                id=obj.id,
                name=obj.name,
                description=obj.description,
                price=obj.price,
                image_url=obj.image_url,
                category=category_name,
            )
        return super().from_orm(obj)
