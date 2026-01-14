"""LangGraph checkpoint database models for persistent state management."""

from datetime import datetime
from typing import Optional

import reflex as rx
import sqlmodel


class Checkpoint(rx.Model, table=True):
    """LangGraph checkpoint for conversation state persistence."""

    id: str = sqlmodel.Field(primary_key=True)
    thread_id: str
    checkpoint_ns: str
    checkpoint_id: str
    parent_checkpoint_id: Optional[str] = sqlmodel.Field(
        default=None, foreign_key="checkpoint.id"
    )
    metadata_json: str = sqlmodel.Field(
        alias="metadata"
    )  # Store as JSON string, map to DB column 'metadata'
    channel_values: str  # JSON stored as string
    created_at: datetime


class CheckpointBlob(rx.Model, table=True):
    """Binary blob storage for checkpoint data."""

    id: str = sqlmodel.Field(primary_key=True)
    checkpoint_id: str = sqlmodel.Field(foreign_key="checkpoint.id")
    channel_name: str
    blob_data: bytes
    created_at: datetime


class CheckpointWrite(rx.Model, table=True):
    """Write operations for checkpoint channels."""

    id: str = sqlmodel.Field(primary_key=True)
    checkpoint_id: str = sqlmodel.Field(foreign_key="checkpoint.id")
    node_id: str
    channel_name: str
    value: str  # JSON stored as string
    created_at: datetime


class CheckpointMigration(rx.Model, table=True):
    """Migration tracking for checkpoint schema updates."""

    id: int = sqlmodel.Field(primary_key=True)
    migration_name: str
    applied_at: datetime
