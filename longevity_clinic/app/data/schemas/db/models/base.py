"""Base utilities for database models."""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)
