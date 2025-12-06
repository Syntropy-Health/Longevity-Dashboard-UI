"""Admin-specific functions for state operations."""

# Re-export shared fetch_call_logs for admin use (no phone filter = all logs)
from ..utils import fetch_call_logs

__all__ = [
    "fetch_call_logs",
]
