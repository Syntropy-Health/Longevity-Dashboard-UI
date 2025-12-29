"""Add missing FK constraints

Revision ID: f1a2b3c4d5e6
Revises: 7d72310139c0
Create Date: 2025-12-29 03:00:00.000000

This migration adds the missing foreign key constraints that were
defined in the models but not properly created in earlier migrations.
Uses batch mode for SQLite compatibility.
"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "7d72310139c0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add missing FK constraints using batch mode."""
    from alembic import context

    # Detect database type
    bind = context.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"

    # Appointments table: add FKs for patient_user_id, provider_user_id, treatment_id
    # SQLite and PostgreSQL have different FK naming conventions
    if is_sqlite:
        naming_convention = {
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        }
        with op.batch_alter_table(
            "appointments", schema=None, naming_convention=naming_convention
        ) as batch_op:
            # Drop old unnamed FK (user_id → users) - naming convention resolves the name
            batch_op.drop_constraint(
                "fk_appointments_user_id_users", type_="foreignkey"
            )
            # Create new FKs with explicit names
            batch_op.create_foreign_key(
                "fk_appointments_patient_user_id_users",
                "users",
                ["patient_user_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_appointments_provider_user_id_users",
                "users",
                ["provider_user_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_appointments_treatment_id_treatments",
                "treatments",
                ["treatment_id"],
                ["id"],
            )
    else:
        # PostgreSQL - use standard ALTER TABLE
        with op.batch_alter_table("appointments", schema=None) as batch_op:
            # Drop old FK (PostgreSQL naming convention)
            batch_op.drop_constraint("appointments_user_id_fkey", type_="foreignkey")
            # Create new FKs
            batch_op.create_foreign_key(
                "fk_appointments_patient_user_id_users",
                "users",
                ["patient_user_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_appointments_provider_user_id_users",
                "users",
                ["provider_user_id"],
                ["id"],
            )
            batch_op.create_foreign_key(
                "fk_appointments_treatment_id_treatments",
                "treatments",
                ["treatment_id"],
                ["id"],
            )

    # Treatments table: add FK for category_id
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_treatments_category_id_treatment_categories",
            "treatment_categories",
            ["category_id"],
            ["id"],
        )


def downgrade() -> None:
    """Remove the FK constraints added in upgrade."""
    with op.batch_alter_table("treatments", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_treatments_category_id_treatment_categories", type_="foreignkey"
        )

    with op.batch_alter_table("appointments", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_appointments_treatment_id_treatments", type_="foreignkey"
        )
        batch_op.drop_constraint(
            "fk_appointments_provider_user_id_users", type_="foreignkey"
        )
        batch_op.drop_constraint(
            "fk_appointments_patient_user_id_users", type_="foreignkey"
        )
        # Restore old FK
        batch_op.create_foreign_key(
            "fk_appointments_user_id_users", "users", ["user_id"], ["id"]
        )
