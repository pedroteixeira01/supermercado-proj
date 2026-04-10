"""Seed roles and assign admin role to admin user

Revision ID: f9e8d7c6b5a4
Revises: b8c42a220268
Create Date: 2026-04-09 21:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table

from alembic import op

revision: str = "f9e8d7c6b5a4"
down_revision: Union[str, Sequence[str], None] = "b8c42a220268"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    roles = table(
        "roles",
        column("id", Integer),
        column("name", String),
    )
    op.bulk_insert(
        roles,
        [
            {"id": 1, "name": "user"},
            {"id": 2, "name": "admin"},
        ],
    )
    op.execute("UPDATE users SET role_id = 2 WHERE id = 1")


def downgrade() -> None:
    op.execute("UPDATE users SET role_id = NULL WHERE id = 1")
    op.execute("DELETE FROM roles WHERE id IN (1, 2)")
