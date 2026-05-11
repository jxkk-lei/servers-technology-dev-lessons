"""add description to products

Revision ID: 20260511_0002
Revises: 20260511_0001
Create Date: 2026-05-11 22:23:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260511_0002"
down_revision: Union[str, None] = "20260511_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.String(length=255),
            nullable=False,
            server_default="No description yet",
        ),
    )


def downgrade() -> None:
    op.drop_column("products", "description")
