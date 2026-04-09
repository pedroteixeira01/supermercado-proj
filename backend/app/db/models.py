from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="user")


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    employees = relationship("Employee", back_populates="store")
    inventories = relationship("Inventory", back_populates="store")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store", back_populates="employees")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    products = relationship("Product", back_populates="category")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_email = Column(String)
    products = relationship("Product", back_populates="supplier")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    promotions = relationship(
        "Promotion", secondary="promotion_products", back_populates="products"
    )


class PromotionProduct(Base):
    __tablename__ = "promotion_products"
    promotion_id = Column(Integer, ForeignKey("promotions.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)


class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    discount_percentage = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    products = relationship(
        "Product", secondary="promotion_products", back_populates="promotions"
    )


class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    quantity = Column(Integer, default=0)
    product = relationship("Product", back_populates="inventories")
    store = relationship("Store", back_populates="inventories")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    published_at = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String, nullable=True)


class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
