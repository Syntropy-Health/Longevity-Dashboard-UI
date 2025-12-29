"""Check-in model for patient check-ins."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class CheckIn(rx.Model, table=True):
    """Patient check-in record (manual, voice, or from call).

    Consolidates check-in data with LLM-processing metadata.
    Health entries (medications, food, symptoms) link back to this table.
    """

    __tablename__ = "checkins"

    id: int | None = Field(default=None, primary_key=True)
    checkin_id: str = Field(index=True, unique=True)  # External ID like "CHK-001"
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: int | None = Field(default=None, foreign_key="call_logs.id")

    # Check-in content
    patient_name: str
    checkin_type: str = Field(default="manual")  # "manual" | "voice" | "call"
    summary: str
    raw_content: str | None = None  # Original text/transcript

    # Health data (from LLM extraction)
    health_topics: str | None = None  # JSON array
    sentiment: str = Field(default="UNKNOWN")  # unknown | positive | neutral | negative
    mood: str = Field(default="UNKNOWN")  # unknown when not determined
    energy_level: int | None = None  # 1-10 (None is fine - numeric)
    urgency_level: str = Field(default="routine")  # "routine" | "follow_up" | "urgent"

    # Processing metadata
    is_processed: bool = Field(default=False)
    llm_model: str | None = None
    processed_at: datetime | None = None

    # Status tracking
    status: str = Field(
        default="pending"
    )  # "pending" | "reviewed" | "flagged" | "archived"
    provider_reviewed: bool = Field(default=False)
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None

    # Timestamps
    timestamp: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
