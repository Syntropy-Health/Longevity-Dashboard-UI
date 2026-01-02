"""Base utilities for database seeding.

Common functionality shared across all seed loaders.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import reflex as rx
from sqlalchemy import text
from sqlmodel import SQLModel


@dataclass
class SeedResult:
    """Result from a seed loading operation."""

    name: str
    loaded: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
    id_map: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return self.loaded + self.skipped

    def __str__(self) -> str:
        status = "✓" if not self.errors else "⚠"
        return f"{status} {self.name}: {self.loaded} loaded, {self.skipped} skipped"


def get_engine():
    """Get SQLAlchemy engine from Reflex."""
    return rx.model.get_engine()


def create_tables(engine) -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)
    print("✓ Created database tables")


def drop_tables(engine) -> None:
    """Drop all database tables."""
    SQLModel.metadata.drop_all(engine)
    print("✓ Dropped existing tables")


def reset_sequences(engine) -> None:
    """Reset database sequences to max(id) + 1 for all tables with serial PKs.

    This fixes sequence drift that occurs when data is seeded/migrated
    with explicit IDs, causing INSERT conflicts on new records.

    Supports both PostgreSQL and SQLite.
    """
    db_type = str(engine.url)

    if "postgresql" in db_type:
        _reset_postgres_sequences(engine)
    elif "sqlite" in db_type:
        _reset_sqlite_sequences(engine)
    else:
        print(f"  ⏭ Skipped sequence reset (unsupported: {db_type})")


def _reset_postgres_sequences(engine) -> None:
    """Reset PostgreSQL sequences."""
    # Tables with auto-increment id columns
    tables_with_sequences = [
        "users",
        "call_logs",
        "call_transcripts",
        "checkins",
        "notifications",
        "appointments",
        "treatments",
        "patient_treatments",
        "biomarker_definitions",
        "biomarker_readings",
        "biomarker_aggregates",
        "medication_entries",
        "food_log_entries",
        "symptom_entries",
        "condition_entries",
        "symptom_trend_entries",
        "data_sources",
        "daily_metrics",
        "patient_visits",
        "provider_metrics",
        "treatment_protocol_metrics",
        "treatment_categories",
        "treatment_statuses",
        "biomarker_categories",
        "checkin_types",
        "urgency_levels",
    ]

    with engine.connect() as conn:
        reset_count = 0
        for table in tables_with_sequences:
            try:
                # Check if table exists
                result = conn.execute(
                    text(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')"
                    )
                )
                if not result.scalar():
                    continue

                # Reset sequence to max(id) + 1
                conn.execute(
                    text(
                        f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM {table}"
                    )
                )
                reset_count += 1
            except Exception:
                pass

        conn.commit()
        print(f"✓ Reset {reset_count} PostgreSQL sequences")


def _reset_sqlite_sequences(engine) -> None:
    """Reset SQLite sequences via sqlite_sequence table.

    For tables using AUTOINCREMENT, SQLite tracks the sequence in sqlite_sequence.
    For tables without AUTOINCREMENT (default), SQLite uses max(rowid)+1 automatically,
    but we can still ensure sqlite_sequence is correct if it exists.
    """
    tables = [
        "users",
        "call_logs",
        "call_transcripts",
        "checkins",
        "notifications",
        "appointments",
        "treatments",
        "patient_treatments",
        "biomarker_definitions",
        "biomarker_readings",
        "biomarker_aggregates",
        "medication_entries",
        "food_log_entries",
        "symptom_entries",
        "condition_entries",
        "symptom_trend_entries",
        "data_sources",
    ]

    with engine.connect() as conn:
        reset_count = 0
        for table in tables:
            try:
                # Get max id from table
                result = conn.execute(text(f"SELECT MAX(id) FROM {table}"))
                max_id = result.scalar() or 0

                # Update or insert into sqlite_sequence
                conn.execute(
                    text(
                        f"INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('{table}', {max_id})"
                    )
                )
                reset_count += 1
            except Exception:
                # Table doesn't exist or no sqlite_sequence
                pass

        conn.commit()
        print(f"✓ Reset {reset_count} SQLite sequences")


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n📥 {title}...")
