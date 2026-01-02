#!/usr/bin/env python
"""Fix PostgreSQL sequence drift after seeding.

Run this if you see errors like:
    duplicate key value violates unique constraint "users_pkey"
    Key (id)=(2) already exists.

Usage:
    uv run python scripts/fix_sequences.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize Reflex config
from seeding.base import get_engine, reset_sequences

import rxconfig  # noqa: F401


def main():
    print("=" * 60)
    print("PostgreSQL Sequence Fix")
    print("=" * 60)

    engine = get_engine()
    print(f"\nDatabase: {engine.url}")

    reset_sequences(engine)

    print("\n✅ Sequences reset successfully!")
    print("   New user registrations should now work.")


if __name__ == "__main__":
    main()
