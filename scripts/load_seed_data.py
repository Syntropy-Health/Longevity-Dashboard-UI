#!/usr/bin/env python
"""Load seed data into the SQLite database.

Run this script to populate a fresh database with seed data:
    python scripts/load_seed_data.py

Or to reset and reload:
    python scripts/load_seed_data.py --reset

This script uses the modular seeding package at scripts/seeding/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize Reflex config to set up database URL
import rxconfig  # noqa: F401

from seeding import load_all_seed_data, SeedResult


def print_results(results: dict[str, SeedResult]) -> None:
    """Print summary of seeding results."""
    print("\n" + "=" * 60)
    print("Seed Data Loading Summary")
    print("=" * 60)

    total_loaded = 0
    total_skipped = 0

    for name, result in results.items():
        print(f"  {result}")
        total_loaded += result.loaded
        total_skipped += result.skipped

    print("-" * 60)
    print(f"  Total: {total_loaded} loaded, {total_skipped} skipped")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Load seed data into database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before loading (WARNING: destroys existing data)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Longevity Clinic - Seed Data Loader")
    print("=" * 60)

    if args.reset:
        print("\n⚠️  Resetting database (--reset flag)")

    results = load_all_seed_data(reset=args.reset)
    print_results(results)

    print("\n" + "=" * 60)
    print("✅ Seed data loaded successfully!")
    print("=" * 60)
    print("\nDatabase location: sqlite:///reflex.db")
    print("Run `reflex db migrate` if you haven't already to sync schema.")


if __name__ == "__main__":
    main()
