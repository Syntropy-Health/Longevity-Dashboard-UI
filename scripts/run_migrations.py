#!/usr/bin/env python
"""Run Alembic migrations against any environment.

This script provides a clean interface for running database migrations
against local SQLite, Supabase PostgreSQL, or any other database.

Usage:
    # Run migrations against local SQLite (default)
    python scripts/run_migrations.py

    # Run migrations against test/Supabase environment
    APP_ENV=test python scripts/run_migrations.py

    # Run migrations with explicit database URL
    REFLEX_DB_URL=postgresql://... python scripts/run_migrations.py

    # Check current migration status
    python scripts/run_migrations.py --status

    # Generate new migration from model changes
    python scripts/run_migrations.py --autogenerate -m "add new column"

    # Downgrade one revision
    python scripts/run_migrations.py --downgrade -1

Best Practices for Production Migrations:
1. Always test migrations locally first with --status
2. For new tables, generate migration with --autogenerate
3. Review generated migration files before applying
4. Use --sql to preview SQL without executing
5. Keep migrations small and focused
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Add project root to path before imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_environment():
    """Load environment variables from .env files."""
    try:
        from dotenv import load_dotenv

        envs_path = project_root / "envs"
        app_env = os.getenv("APP_ENV", "dev").lower()

        print(f"🔧 Environment: {app_env}")

        # Load in order: base → env-specific → secrets
        for env_file in [
            envs_path / ".env.base",
            envs_path / f".env.{app_env}",
            envs_path / ".env.secrets",
        ]:
            if env_file.exists():
                load_dotenv(env_file, override=True)
                print(f"  ✓ Loaded: {env_file.name}")
    except ImportError:
        print("⚠️  python-dotenv not installed, using environment variables only")


def get_alembic_config():
    """Get Alembic configuration."""
    from alembic.config import Config

    alembic_ini = project_root / "alembic.ini"
    if not alembic_ini.exists():
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini}")

    return Config(str(alembic_ini))


def show_status():
    """Show current migration status."""
    from alembic import command

    config = get_alembic_config()
    print("\n📋 Current Migration Status:")
    print("-" * 40)
    command.current(config, verbose=True)
    print()
    command.history(config, verbose=True)


def run_upgrade(revision: str = "head", sql_only: bool = False):
    """Run upgrade migrations."""
    from alembic import command

    config = get_alembic_config()

    if sql_only:
        print(f"\n📝 SQL Preview for upgrade to {revision}:")
        print("-" * 40)
        command.upgrade(config, revision, sql=True)
    else:
        print(f"\n🚀 Running upgrade to {revision}...")
        command.upgrade(config, revision)
        print("✅ Upgrade complete")


def run_downgrade(revision: str = "-1", sql_only: bool = False):
    """Run downgrade migrations."""
    from alembic import command

    config = get_alembic_config()

    if sql_only:
        print(f"\n📝 SQL Preview for downgrade to {revision}:")
        print("-" * 40)
        command.downgrade(config, revision, sql=True)
    else:
        print(f"\n⬇️  Running downgrade to {revision}...")
        command.downgrade(config, revision)
        print("✅ Downgrade complete")


def generate_migration(message: str, autogenerate: bool = True):
    """Generate a new migration revision."""
    from alembic import command

    config = get_alembic_config()

    print(f"\n📝 Generating new migration: {message}")
    command.revision(config, message=message, autogenerate=autogenerate)
    print("✅ Migration generated - review before applying")


def stamp_head():
    """Mark all migrations as applied without running them.

    Use this when database schema already matches models but
    alembic_version table is missing or outdated.
    """
    from alembic import command

    config = get_alembic_config()

    print("\n🏷️  Stamping database as current...")
    command.stamp(config, "head")
    print("✅ Database stamped at head")


def main():
    parser = argparse.ArgumentParser(
        description="Run Alembic migrations for Longevity Clinic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--status",
        "-s",
        action="store_true",
        help="Show current migration status and history",
    )
    parser.add_argument(
        "--upgrade",
        "-u",
        nargs="?",
        const="head",
        metavar="REVISION",
        help="Run upgrade to REVISION (default: head)",
    )
    parser.add_argument(
        "--downgrade",
        "-d",
        nargs="?",
        const="-1",
        metavar="REVISION",
        help="Run downgrade to REVISION (default: -1)",
    )
    parser.add_argument(
        "--autogenerate",
        "-a",
        action="store_true",
        help="Generate new migration from model changes",
    )
    parser.add_argument(
        "--message",
        "-m",
        default="auto migration",
        help="Message for new migration (use with --autogenerate)",
    )
    parser.add_argument(
        "--sql", action="store_true", help="Output SQL instead of running migrations"
    )
    parser.add_argument(
        "--stamp-head",
        action="store_true",
        help="Mark current schema as up-to-date without running migrations",
    )
    parser.add_argument(
        "--env", choices=["dev", "test", "prod"], help="Override APP_ENV environment"
    )

    args = parser.parse_args()

    # Set environment if specified
    if args.env:
        os.environ["APP_ENV"] = args.env

    # Load environment
    load_environment()

    # Show database URL (masked)
    db_url = os.getenv("REFLEX_DB_URL", "sqlite:///reflex.db")
    if "@" in db_url:
        masked = db_url.split("@")[1]
        print(f"🗄️  Database: ...@{masked}")
    else:
        print(f"🗄️  Database: {db_url}")

    try:
        # Execute requested action
        if args.status:
            show_status()
        elif args.stamp_head:
            stamp_head()
        elif args.autogenerate:
            generate_migration(args.message, autogenerate=True)
        elif args.downgrade:
            run_downgrade(args.downgrade, sql_only=args.sql)
        elif args.upgrade:
            run_upgrade(args.upgrade, sql_only=args.sql)
        else:
            # Default: upgrade to head
            run_upgrade("head", sql_only=args.sql)
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
