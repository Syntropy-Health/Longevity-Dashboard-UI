#!/usr/bin/env python
"""Database migration utility for Longevity Clinic.

Combines schema export and data dump into a complete migration package.

Usage:
    python scripts/db_migrate.py export --output migrations/
    python scripts/db_migrate.py validate --target postgres
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_export(output_dir: str, include_data: bool = True) -> None:
    """Export schema and optionally data to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("Longevity Clinic - Database Migration Export")
    print("=" * 60)

    # Export schema
    schema_file = output_path / f"schema_{timestamp}.sql"
    print(f"\n📄 Exporting schema to {schema_file}...")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/export_schema.py",
            "--include-drop",
            "-o",
            str(schema_file),
        ],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    if result.returncode != 0:
        print(f"❌ Schema export failed: {result.stderr}")
        sys.exit(1)

    print(f"  ✓ Schema exported to {schema_file}")

    # Export data
    if include_data:
        data_file = output_path / f"data_{timestamp}.sql"
        print(f"\n📊 Exporting data to {data_file}...")

        result = subprocess.run(
            [sys.executable, "scripts/export_data.py", "-o", str(data_file)],
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        if result.returncode != 0:
            print(f"❌ Data export failed: {result.stderr}")
            sys.exit(1)

        print(f"  ✓ Data exported to {data_file}")

    # Create combined migration file
    combined_file = output_path / f"migration_{timestamp}.sql"
    print(f"\n📦 Creating combined migration file {combined_file}...")

    with open(combined_file, "w") as f:
        f.write(
            "-- ============================================================================\n"
        )
        f.write("-- Longevity Clinic - Complete Database Migration\n")
        f.write(f"-- Generated: {datetime.now().isoformat()}\n")
        f.write(
            "-- ============================================================================\n\n"
        )
        f.write("-- STEP 1: Create schema\n")
        f.write(f"\\i {schema_file.name}\n\n")
        if include_data:
            f.write("-- STEP 2: Load seed data\n")
            f.write(f"\\i {data_file.name}\n\n")
        f.write("-- Migration complete\n")

    print(f"  ✓ Combined migration file created: {combined_file}")

    # Create README
    readme_file = output_path / "README.md"
    with open(readme_file, "w") as f:
        f.write("# Database Migration Files\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Files\n\n")
        f.write(f"- `{schema_file.name}` - PostgreSQL schema (tables, indexes)\n")
        if include_data:
            f.write(f"- `{data_file.name}` - Seed data (INSERT statements)\n")
        f.write(f"- `{combined_file.name}` - Combined migration script\n\n")
        f.write("## Usage\n\n")
        f.write("### Option 1: Run combined migration\n")
        f.write("```bash\n")
        f.write(f"psql -U postgres -d longevity_clinic -f {combined_file.name}\n")
        f.write("```\n\n")
        f.write("### Option 2: Run schema and data separately\n")
        f.write("```bash\n")
        f.write(f"psql -U postgres -d longevity_clinic -f {schema_file.name}\n")
        if include_data:
            f.write(f"psql -U postgres -d longevity_clinic -f {data_file.name}\n")
        f.write("```\n\n")
        f.write("### Create database first\n")
        f.write("```bash\n")
        f.write("psql -U postgres -c 'CREATE DATABASE longevity_clinic;'\n")
        f.write("```\n")

    print("\n✅ Migration export complete!")
    print(f"   Output directory: {output_path.absolute()}")


def validate_schema(target: str) -> None:
    """Validate schema against target database type."""
    print(f"Validating schema for {target}...")

    # Get schema
    result = subprocess.run(
        [sys.executable, "scripts/export_schema.py"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    if result.returncode != 0:
        print(f"❌ Failed to get schema: {result.stderr}")
        sys.exit(1)

    schema = result.stdout

    # Basic validation
    issues = []

    if target == "postgres":
        # Check for SQLite-specific syntax
        if "AUTOINCREMENT" in schema.upper():
            issues.append("Found AUTOINCREMENT (should be SERIAL)")
        if "INTEGER PRIMARY KEY" in schema.upper() and "SERIAL" not in schema.upper():
            issues.append("Found INTEGER PRIMARY KEY without SERIAL conversion")
        if " DATETIME " in schema.upper():
            issues.append("Found DATETIME (should be TIMESTAMP)")

    if issues:
        print("❌ Schema validation issues found:")
        for issue in issues:
            print(f"   - {issue}")
        sys.exit(1)
    else:
        print("✅ Schema validation passed!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Database migration utility for Longevity Clinic"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export schema and data")
    export_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="migrations",
        help="Output directory (default: migrations/)",
    )
    export_parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Export schema only, skip data",
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate schema")
    validate_parser.add_argument(
        "--target",
        "-t",
        type=str,
        default="postgres",
        choices=["postgres", "mysql"],
        help="Target database type (default: postgres)",
    )

    args = parser.parse_args()

    if args.command == "export":
        run_export(args.output, include_data=not args.schema_only)
    elif args.command == "validate":
        validate_schema(args.target)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
