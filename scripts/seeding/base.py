"""Base utilities for database seeding.

Common functionality shared across all seed loaders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import reflex as rx
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


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n📥 {title}...")
