#!/usr/bin/env python
"""Load seed data into the database.

Run this script to populate a fresh database with seed data:
    python scripts/load_seed_data.py

Or to reset and reload:
    python scripts/load_seed_data.py --reset

Seed only specific categories (without overwriting existing):
    python scripts/load_seed_data.py --only health,conditions
    python scripts/load_seed_data.py --only food,symptoms,data_sources

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
from seeding import (
    SeedResult,
    create_tables,
    get_engine,
    load_all_seed_data,
    load_conditions,
    load_data_sources,
    load_health_entries,
    load_symptom_trends,
    load_users,
)

import rxconfig  # noqa: F401

# Map category names to loader functions
CATEGORY_LOADERS = {
    "health": load_health_entries,  # medications, food, symptoms
    "food": load_health_entries,  # alias for health
    "conditions": load_conditions,
    "symptom_trends": load_symptom_trends,
    "data_sources": load_data_sources,
}

# Categories that require user_id_map
REQUIRES_USER_MAP = {"health", "food", "conditions", "symptom_trends", "data_sources"}


def print_results(results: dict[str, SeedResult]) -> None:
    """Print summary of seeding results."""
    print("\n" + "=" * 60)
    print("Seed Data Loading Summary")
    print("=" * 60)

    total_loaded = 0
    total_skipped = 0

    for _name, result in results.items():
        print(f"  {result}")
        total_loaded += result.loaded
        total_skipped += result.skipped

    print("-" * 60)
    print(f"  Total: {total_loaded} loaded, {total_skipped} skipped")


def load_selective_seed_data(categories: list[str]) -> dict[str, SeedResult]:
    """Load only specified seed categories without overwriting.

    Args:
        categories: List of category names to load

    Returns:
        Dict mapping loader name to SeedResult with counts.
    """
    from sqlmodel import Session

    results = {}
    engine = get_engine()

    # Ensure tables exist (no drop)
    create_tables(engine)

    with Session(engine) as session:
        # Check if any category needs user_id_map
        needs_user_map = any(cat in REQUIRES_USER_MAP for cat in categories)

        user_id_map = {}
        if needs_user_map:
            # Load users first to get ID mappings (or get existing)
            print("\n📥 Ensuring users exist...")
            user_result = load_users(session)
            user_id_map = user_result.id_map
            if user_result.loaded > 0:
                results["users"] = user_result

        # Load each requested category
        for category in categories:
            category = category.strip().lower()
            if category not in CATEGORY_LOADERS:
                print(f"  ⚠ Unknown category: {category}")
                continue

            loader = CATEGORY_LOADERS[category]
            # Use canonical name for deduplication
            canonical = "health" if category == "food" else category

            if canonical in results:
                continue  # Already loaded

            result = loader(session, user_id_map)
            results[canonical] = result

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Load seed data into database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before loading (WARNING: destroys existing data)",
    )
    parser.add_argument(
        "--only",
        type=str,
        help="Comma-separated list of categories to seed (health,conditions,symptom_trends,data_sources)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Longevity Clinic - Seed Data Loader")
    print("=" * 60)

    if args.reset and args.only:
        print("\n⚠️  Cannot use --reset with --only (selective mode doesn't reset)")
        sys.exit(1)

    if args.reset:
        print("\n⚠️  Resetting database (--reset flag)")
        results = load_all_seed_data(reset=args.reset)
    elif args.only:
        categories = [c.strip() for c in args.only.split(",")]
        print(f"\n📋 Selective seeding: {', '.join(categories)}")
        print("   (existing records will be skipped)")
        results = load_selective_seed_data(categories)
    else:
        results = load_all_seed_data(reset=False)

    print_results(results)

    print("\n" + "=" * 60)
    print("✅ Seed data loaded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
