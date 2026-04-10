"""Seed admin user

Revision ID: b8c42a220268
Revises: d72df378d3e5
Create Date: 2026-04-09 20:50:45.142307

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.sql import column, table

from alembic import op
from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = "b8c42a220268"
down_revision: Union[str, Sequence[str], None] = "d72df378d3e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users = table(
        "users",
        column("id", Integer),
        column("email", String),
        column("hashed_password", String),
        column("is_active", Boolean),
    )
    op.bulk_insert(
        users,
        [
            {
                "id": 1,
                "email": "admin@superviva.com",
                "hashed_password": get_password_hash("admin123"),
                "is_active": True,
            }
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE id = 1")
