#!/usr/bin/env python
"""Reset PostgreSQL database and re-run all migrations.

This script is designed for resetting a remote PostgreSQL database (like Supabase)
to match the local migration trajectory. It will:
1. Drop all existing tables (CASCADE)
2. Remove alembic_version tracking
3. Re-run all migrations from scratch

WARNING: This will DELETE ALL DATA in the target database.

Usage:
    # Dry run - show what would be dropped
    APP_ENV=test python scripts/reset_postgres.py --dry-run

    # Actually reset the database
    APP_ENV=test python scripts/reset_postgres.py --confirm

Best Practice:
- Always run with --dry-run first to review what will be dropped
- Backup important data before running
- After reset, re-seed the database with scripts/load_seed_data.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_environment():
    """Load environment variables from .env files."""
    try:
        from dotenv import load_dotenv

        envs_path = project_root / "envs"
        app_env = os.getenv("APP_ENV", "dev").lower()

        print(f"🔧 Environment: {app_env}")

        for env_file in [
            envs_path / ".env.base",
            envs_path / f".env.{app_env}",
            envs_path / ".env.secrets",
        ]:
            if env_file.exists():
                load_dotenv(env_file, override=True)
                print(f"  ✓ Loaded: {env_file.name}")
    except ImportError:
        print("⚠️  python-dotenv not installed")


def get_db_info():
    """Get database URL and mask it for display."""
    db_url = os.getenv("REFLEX_DB_URL")
    if not db_url:
        print("❌ REFLEX_DB_URL not set")
        sys.exit(1)

    # Safety check - don't allow SQLite reset with this script
    if db_url.startswith("sqlite"):
        print("❌ This script is for PostgreSQL only. Use 'rm reflex.db' for SQLite.")
        sys.exit(1)

    # Mask password for display
    if "@" in db_url:
        masked = f"...@{db_url.split('@')[1]}"
    else:
        masked = db_url

    return db_url, masked


def list_tables(engine):
    """List all tables in the database."""
    from sqlalchemy import inspect

    inspector = inspect(engine)
    return inspector.get_table_names()


def drop_all_tables(engine, dry_run: bool = True):
    """Drop all tables in the database."""
    from sqlalchemy import text

    tables = list_tables(engine)

    if not tables:
        print("✓ No tables to drop")
        return

    print(f"\n📋 Tables to drop ({len(tables)}):")
    for t in sorted(tables):
        print(f"  - {t}")

    if dry_run:
        print("\n⚠️  DRY RUN - no changes made")
        return

    print("\n🗑️  Dropping tables...")

    with engine.connect() as conn:
        # Disable foreign key checks and drop all tables
        conn.execute(text("SET session_replication_role = 'replica';"))

        for table in tables:
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                print(f"  ✓ Dropped: {table}")
            except Exception as e:
                print(f"  ✗ Failed to drop {table}: {e}")

        conn.execute(text("SET session_replication_role = 'origin';"))
        conn.commit()

    print("✅ All tables dropped")


def run_migrations():
    """Run all migrations from scratch."""
    from alembic import command
    from alembic.config import Config

    alembic_ini = project_root / "alembic.ini"
    config = Config(str(alembic_ini))

    print("\n🚀 Running migrations from scratch...")
    command.upgrade(config, "head")
    print("✅ Migrations complete")


def main():
    parser = argparse.ArgumentParser(
        description="Reset PostgreSQL database and re-run migrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be dropped without making changes",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Actually drop tables and reset the database",
    )
    parser.add_argument(
        "--skip-migrations",
        action="store_true",
        help="Only drop tables, don't run migrations",
    )

    args = parser.parse_args()

    if not args.dry_run and not args.confirm:
        print("❌ Must specify either --dry-run or --confirm")
        print("   Use --dry-run to preview changes")
        print("   Use --confirm to actually reset the database")
        sys.exit(1)

    # Load environment
    load_environment()

    # Get database URL
    db_url, masked_url = get_db_info()
    print(f"\n🗄️  Database: {masked_url}")

    # Create engine
    from sqlalchemy import create_engine

    engine = create_engine(db_url)

    # Show current state
    tables = list_tables(engine)
    print(f"\n📊 Current state: {len(tables)} tables")

    if args.dry_run:
        drop_all_tables(engine, dry_run=True)
        print("\n💡 To actually reset, run with --confirm")
    else:
        # Final confirmation
        print("\n" + "=" * 50)
        print("⚠️  WARNING: This will DELETE ALL DATA")
        print("=" * 50)

        confirm = input("\nType 'RESET' to confirm: ")
        if confirm != "RESET":
            print("❌ Cancelled")
            sys.exit(1)

        # Drop all tables
        drop_all_tables(engine, dry_run=False)

        # Run migrations
        if not args.skip_migrations:
            run_migrations()

        print("\n" + "=" * 50)
        print("✅ Database reset complete")
        print("=" * 50)
        print("\n💡 Next steps:")
        print("   1. Re-seed data: uv run python scripts/load_seed_data.py")
        print(
            "   2. Verify: APP_ENV=test uv run python scripts/run_migrations.py --status"
        )


if __name__ == "__main__":
    main()
