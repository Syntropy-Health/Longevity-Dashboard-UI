#!/usr/bin/env python
"""Export database data as PostgreSQL-compatible INSERT statements.

Dumps data from SQLite database to SQL INSERT statements for migration.

Usage:
    python scripts/export_data.py > data.sql
    python scripts/export_data.py --output schema/seed_data.sql
    python scripts/export_data.py --tables users,treatments
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize Reflex config to set up database URL
import reflex as rx
from sqlalchemy import inspect, text

import rxconfig  # noqa: F401


def format_value(value: Any) -> str:
    """Format a Python value as a PostgreSQL-compatible SQL literal."""
    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    if isinstance(value, (int, float, Decimal)):
        return str(value)

    if isinstance(value, datetime):
        return f"'{value.isoformat()}'"

    if isinstance(value, date):
        return f"'{value.isoformat()}'"

    if isinstance(value, (dict, list)):
        # Convert to JSON string
        json_str = json.dumps(value).replace("'", "''")
        return f"'{json_str}'"

    if isinstance(value, str):
        # Escape single quotes
        escaped = value.replace("'", "''")
        return f"'{escaped}'"

    if isinstance(value, bytes):
        # Convert to hex for PostgreSQL bytea
        hex_str = value.hex()
        return f"'\\x{hex_str}'"

    # Default: try to convert to string
    return f"'{value!s}'"


def get_table_data(engine, table_name: str) -> tuple[list[str], list[tuple]]:
    """Get column names and rows from a table."""
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name}"))
        rows = [tuple(row) for row in result.fetchall()]

    return columns, rows


def generate_insert_statements(
    table_name: str,
    columns: list[str],
    rows: list[tuple],
    batch_size: int = 100,
) -> list[str]:
    """Generate INSERT statements for a table."""
    if not rows:
        return [f"-- No data in {table_name}"]

    statements = []
    statements.append(f"-- Data for table: {table_name} ({len(rows)} rows)")

    # Generate batched INSERT statements
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]

        col_list = ", ".join(columns)
        values_list = []

        for row in batch:
            values = ", ".join(format_value(v) for v in row)
            values_list.append(f"    ({values})")

        stmt = f"INSERT INTO {table_name} ({col_list}) VALUES\n"
        stmt += ",\n".join(values_list)
        stmt += ";"

        statements.append(stmt)

    return statements


def export_data(
    tables: list[str] | None = None,
    exclude_tables: list[str] | None = None,
    batch_size: int = 100,
) -> str:
    """Export data from all or specified tables."""
    engine = rx.model.get_engine()
    inspector = inspect(engine)

    all_tables = inspector.get_table_names()

    # Filter tables
    if tables:
        all_tables = [t for t in all_tables if t in tables]

    if exclude_tables:
        all_tables = [t for t in all_tables if t not in exclude_tables]

    # Skip internal tables
    all_tables = [t for t in all_tables if not t.startswith("alembic")]

    lines = [
        "-- ============================================================================",
        "-- Longevity Clinic - Seed Data Export",
        "-- Generated from SQLite database",
        f"-- Export date: {datetime.now().isoformat()}",
        "-- ============================================================================",
        "",
        "-- Disable foreign key checks during import",
        "SET session_replication_role = replica;",
        "",
    ]

    for table_name in all_tables:
        columns, rows = get_table_data(engine, table_name)
        statements = generate_insert_statements(table_name, columns, rows, batch_size)
        lines.extend(statements)
        lines.append("")

    lines.extend(
        [
            "-- Re-enable foreign key checks",
            "SET session_replication_role = DEFAULT;",
            "",
            "-- Update sequences (for SERIAL columns)",
        ]
    )

    # Add sequence reset statements for tables with id columns
    for table_name in all_tables:
        columns, rows = get_table_data(engine, table_name)
        if "id" in columns and rows:
            lines.append(
                f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), "
                f"(SELECT COALESCE(MAX(id), 0) + 1 FROM {table_name}), false);"
            )

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export database data as PostgreSQL-compatible INSERT statements"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--tables",
        "-t",
        type=str,
        default=None,
        help="Comma-separated list of tables to export (default: all)",
    )
    parser.add_argument(
        "--exclude",
        "-x",
        type=str,
        default=None,
        help="Comma-separated list of tables to exclude",
    )
    parser.add_argument(
        "--batch-size",
        "-b",
        type=int,
        default=100,
        help="Number of rows per INSERT statement (default: 100)",
    )
    args = parser.parse_args()

    tables = args.tables.split(",") if args.tables else None
    exclude_tables = args.exclude.split(",") if args.exclude else None

    data_sql = export_data(
        tables=tables,
        exclude_tables=exclude_tables,
        batch_size=args.batch_size,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(data_sql)
        print(f"✓ Data exported to {args.output}", file=sys.stderr)
    else:
        print(data_sql)


if __name__ == "__main__":
    main()
