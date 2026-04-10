"""Seed data

Revision ID: d72df378d3e5
Revises: 1e0b724e2bf8
Create Date: 2026-04-09 20:40:45.142307

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d72df378d3e5"
down_revision: Union[str, Sequence[str], None] = "1e0b724e2bf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy import Float, Integer, String
from sqlalchemy.sql import column, table


def upgrade() -> None:
    categories = table(
        "categories",
        column("id", Integer),
        column("name", String),
        column("description", String),
    )
    op.bulk_insert(
        categories,
        [
            {
                "id": 1,
                "name": "Hortifruti",
                "description": "Frutas, verduras e legumes frescos",
            },
            {"id": 2, "name": "Açougue", "description": "Carnes de primeira e segunda"},
            {"id": 3, "name": "Padaria", "description": "Pães, bolos e doces"},
            {
                "id": 4,
                "name": "Bebidas",
                "description": "Sucos, refrigerantes, águas e alcoólicos",
            },
        ],
    )

    products = table(
        "products",
        column("id", Integer),
        column("name", String),
        column("description", String),
        column("price", Float),
        column("image_url", String),
        column("category_id", Integer),
    )
    op.bulk_insert(
        products,
        [
            {
                "id": 1,
                "name": "Maçã Fuji",
                "description": "Maçã fresca e crocante (kg)",
                "price": 8.99,
                "image_url": "images/maca.jpg",
                "category_id": 1,
            },
            {
                "id": 2,
                "name": "Alface Crespa",
                "description": "Pé de alface fresco",
                "price": 3.50,
                "image_url": "images/alface.jpg",
                "category_id": 1,
            },
            {
                "id": 3,
                "name": "Picanha Bovina",
                "description": "Picanha de primeira linha (kg)",
                "price": 79.90,
                "image_url": "images/picanha.jpg",
                "category_id": 2,
            },
            {
                "id": 4,
                "name": "Pão Francês",
                "description": "Pão quentinho saindo do forno (kg)",
                "price": 16.90,
                "image_url": "images/pao.jpg",
                "category_id": 3,
            },
            {
                "id": 5,
                "name": "Refrigerante Cola 2L",
                "description": "Garrafa de 2 litros gelada",
                "price": 8.50,
                "image_url": "images/refrigerante.jpg",
                "category_id": 4,
            },
            {
                "id": 6,
                "name": "Suco de Laranja Natural 1L",
                "description": "Suco 100% fruta",
                "price": 12.00,
                "image_url": "images/suco.jpg",
                "category_id": 4,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM products WHERE id IN (1, 2, 3, 4, 5, 6)")
    op.execute("DELETE FROM categories WHERE id IN (1, 2, 3, 4)")
