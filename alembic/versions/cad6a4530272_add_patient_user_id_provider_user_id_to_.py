"""Add patient_user_id provider_user_id to appointments

Revision ID: cad6a4530272
Revises: a553ec7f0ddc
Create Date: 2025-12-28 14:43:39.169954

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cad6a4530272"
down_revision: str | Sequence[str] | None = "a553ec7f0ddc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns for normalized user relationships
    with op.batch_alter_table("appointments", schema=None) as batch_op:
        # New FK columns
        batch_op.add_column(sa.Column("patient_user_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("provider_user_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("treatment_id", sa.Integer(), nullable=True))
        # New appointment fields
        batch_op.add_column(
            sa.Column("location", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "is_virtual",
                sa.Boolean(),
                server_default=sa.text("FALSE"),
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column("meeting_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
        )
        # Indexes
        batch_op.create_index(
            batch_op.f("ix_appointments_patient_user_id"),
            ["patient_user_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_appointments_provider_user_id"),
            ["provider_user_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_appointments_treatment_id"), ["treatment_id"], unique=False
        )
        # Note: Not creating FK constraints for SQLite compatibility
        # FK constraints will be enforced at application level

    # Migrate data: copy user_id to patient_user_id for existing rows
    op.execute(
        "UPDATE appointments SET patient_user_id = user_id WHERE user_id IS NOT NULL"
    )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("appointments", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_appointments_treatment_id"))
        batch_op.drop_index(batch_op.f("ix_appointments_provider_user_id"))
        batch_op.drop_index(batch_op.f("ix_appointments_patient_user_id"))
        batch_op.drop_column("meeting_url")
        batch_op.drop_column("is_virtual")
        batch_op.drop_column("location")
        batch_op.drop_column("treatment_id")
        batch_op.drop_column("provider_user_id")
        batch_op.drop_column("patient_user_id")
