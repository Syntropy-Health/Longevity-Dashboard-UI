"""add_category_id_fk_to_treatment

Revision ID: 095019143d02
Revises: cad6a4530272
Create Date: 2025-12-28 19:16:04.565735

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "095019143d02"
down_revision: str | Sequence[str] | None = "cad6a4530272"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add category_id column to treatments table
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.add_column(sa.Column("category_id", sa.Integer(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_treatments_category_id"), ["category_id"], unique=False
        )

    # Data migration: populate category_id from category string
    # Map category names to treatment_categories.id
    op.execute(
        """
        UPDATE treatments
        SET category_id = (
            SELECT tc.id FROM treatment_categories tc
            WHERE tc.name = treatments.category
        )
        WHERE EXISTS (
            SELECT 1 FROM treatment_categories tc
            WHERE tc.name = treatments.category
        )
    """
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_treatments_category_id"))
        batch_op.drop_column("category_id")

    # ### end Alembic commands ###

    # ### end Alembic commands ###
