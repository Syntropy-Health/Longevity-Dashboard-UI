#!/usr/bin/env python
"""Export database schema to PostgreSQL-compatible SQL.

Converts SQLite schema to PostgreSQL format for migration to test/prod databases.

Usage:
    python scripts/export_schema.py > schema.sql
    python scripts/export_schema.py --output schema/postgres_schema.sql
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize Reflex config to set up database URL
import reflex as rx
from sqlalchemy import inspect

import rxconfig  # noqa: F401

# SQLite to PostgreSQL type mappings
TYPE_MAPPINGS = {
    "INTEGER": "INTEGER",
    "BIGINT": "BIGINT",
    "SMALLINT": "SMALLINT",
    "REAL": "REAL",
    "FLOAT": "DOUBLE PRECISION",
    "DOUBLE": "DOUBLE PRECISION",
    "NUMERIC": "NUMERIC",
    "DECIMAL": "DECIMAL",
    "VARCHAR": "VARCHAR",
    "CHAR": "CHAR",
    "TEXT": "TEXT",
    "BLOB": "BYTEA",
    "BOOLEAN": "BOOLEAN",
    "DATE": "DATE",
    "TIME": "TIME",
    "DATETIME": "TIMESTAMP",
    "TIMESTAMP": "TIMESTAMP",
    "JSON": "JSONB",
}


def convert_sqlite_type(sqlite_type: str) -> str:
    """Convert SQLite type to PostgreSQL type."""
    # Handle VARCHAR(n)
    match = re.match(r"(\w+)\((\d+)\)", sqlite_type.upper())
    if match:
        base_type, size = match.groups()
        pg_type = TYPE_MAPPINGS.get(base_type, base_type)
        return f"{pg_type}({size})"

    return TYPE_MAPPINGS.get(sqlite_type.upper(), sqlite_type)


def convert_create_table(sqlite_ddl: str) -> str:
    """Convert SQLite CREATE TABLE to PostgreSQL format."""
    # Replace AUTOINCREMENT with SERIAL
    ddl = re.sub(
        r"INTEGER PRIMARY KEY AUTOINCREMENT",
        "SERIAL PRIMARY KEY",
        sqlite_ddl,
        flags=re.IGNORECASE,
    )

    # Replace INTEGER PRIMARY KEY (without AUTOINCREMENT)
    ddl = re.sub(
        r"INTEGER PRIMARY KEY(?!\s+AUTOINCREMENT)",
        "SERIAL PRIMARY KEY",
        ddl,
        flags=re.IGNORECASE,
    )

    # Convert DATETIME to TIMESTAMP
    ddl = re.sub(r"\bDATETIME\b", "TIMESTAMP", ddl, flags=re.IGNORECASE)

    # Convert BOOLEAN representation
    ddl = re.sub(r"\bINTEGER\b\s+DEFAULT\s+0\b", "BOOLEAN DEFAULT FALSE", ddl)
    ddl = re.sub(r"\bINTEGER\b\s+DEFAULT\s+1\b", "BOOLEAN DEFAULT TRUE", ddl)

    # Remove SQLite-specific syntax
    ddl = re.sub(r"IF NOT EXISTS\s+", "", ddl, flags=re.IGNORECASE)

    return ddl


def get_sqlite_schema() -> list[str]:
    """Get CREATE TABLE statements from SQLite database."""
    engine = rx.model.get_engine()
    inspector = inspect(engine)

    statements = []

    # Get all table names
    tables = inspector.get_table_names()

    for table_name in tables:
        # Skip SQLAlchemy internal tables
        if table_name.startswith("alembic"):
            continue

        # Get columns
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        fk_constraints = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)

        # Build CREATE TABLE statement
        col_defs = []
        for col in columns:
            col_def = f"    {col['name']} {convert_sqlite_type(str(col['type']))}"

            if not col.get("nullable", True):
                col_def += " NOT NULL"

            if col.get("default") is not None:
                default = col["default"]
                if isinstance(default, str) and "(" in default:
                    # Function call like CURRENT_TIMESTAMP
                    col_def += f" DEFAULT {default}"
                elif isinstance(default, bool):
                    col_def += f" DEFAULT {str(default).upper()}"
                elif isinstance(default, int | float):
                    col_def += f" DEFAULT {default}"
                else:
                    col_def += f" DEFAULT '{default}'"

            col_defs.append(col_def)

        # Add primary key constraint
        if pk_constraint and pk_constraint.get("constrained_columns"):
            pk_cols = pk_constraint["constrained_columns"]
            # Only add if not single column (already handled inline)
            if len(pk_cols) > 1:
                col_defs.append(f"    PRIMARY KEY ({', '.join(pk_cols)})")

        # Add foreign key constraints
        for fk in fk_constraints:
            ref_table = fk["referred_table"]
            local_cols = ", ".join(fk["constrained_columns"])
            ref_cols = ", ".join(fk["referred_columns"])
            col_defs.append(
                f"    FOREIGN KEY ({local_cols}) REFERENCES {ref_table}({ref_cols})"
            )

        create_stmt = f"CREATE TABLE {table_name} (\n" + ",\n".join(col_defs) + "\n);"
        statements.append(create_stmt)

        # Add index statements
        for idx in indexes:
            if idx.get("unique"):
                idx_stmt = f"CREATE UNIQUE INDEX {idx['name']} ON {table_name} ({', '.join(idx['column_names'])});"
            else:
                idx_stmt = f"CREATE INDEX {idx['name']} ON {table_name} ({', '.join(idx['column_names'])});"
            statements.append(idx_stmt)

    return statements


def generate_postgres_schema(include_drop: bool = False) -> str:
    """Generate PostgreSQL-compatible schema SQL."""
    lines = [
        "-- ============================================================================",
        "-- Longevity Clinic - PostgreSQL Schema",
        "-- Generated from SQLite database",
        "-- ============================================================================",
        "",
        "-- Enable UUID extension if needed",
        '-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
        "",
    ]

    statements = get_sqlite_schema()

    if include_drop:
        lines.append("-- Drop tables in reverse dependency order")
        tables = [s.split()[2] for s in statements if s.startswith("CREATE TABLE")]
        for table in reversed(tables):
            lines.append(f"DROP TABLE IF EXISTS {table} CASCADE;")
        lines.append("")

    lines.append("-- Create tables")
    lines.append("")

    for stmt in statements:
        # Convert any remaining SQLite-specific syntax
        stmt = convert_create_table(stmt)
        lines.append(stmt)
        lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export database schema to PostgreSQL-compatible SQL"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--include-drop",
        action="store_true",
        help="Include DROP TABLE statements",
    )
    args = parser.parse_args()

    schema_sql = generate_postgres_schema(include_drop=args.include_drop)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(schema_sql)
        print(f"✓ Schema exported to {args.output}")
    else:
        print(schema_sql)


if __name__ == "__main__":
    main()
