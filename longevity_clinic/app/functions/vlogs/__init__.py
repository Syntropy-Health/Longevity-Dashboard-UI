"""VlogsAgent - Modular call logs processing.

Handles fetching and processing call logs with configurable LLM parsing.
Implements CDC (Change Data Capture) pattern for syncing to database.
"""

from .agent import VlogsAgent
from .db import reset_all_processed_to_metrics_sync

__all__ = ["VlogsAgent", "reset_all_processed_to_metrics_sync"]
