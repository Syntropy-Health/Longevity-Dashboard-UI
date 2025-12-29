"""drop_category_string_from_treatments

Revision ID: 41e851475f81
Revises: 095019143d02
Create Date: 2025-12-28 22:30:26.225402

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41e851475f81"
down_revision: str | Sequence[str] | None = "095019143d02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Drop the redundant category string column from treatments table.

    The category_id FK was added in previous migration (095019143d02).
    Now we remove the denormalized category string field.
    """
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.drop_column("category")


def downgrade() -> None:
    """Re-add category string column with default value."""
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "category", sa.VARCHAR(), nullable=False, server_default="General"
            )
        )
