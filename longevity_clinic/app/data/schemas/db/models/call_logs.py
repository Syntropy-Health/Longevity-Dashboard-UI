"""Call log models for voice call tracking."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class CallLog(rx.Model, table=True):
    """Voice call log from the telephony system."""

    __tablename__ = "call_logs"

    id: int | None = Field(default=None, primary_key=True)
    call_id: str = Field(index=True, unique=True)  # External call ID from API
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    phone_number: str = Field(index=True)
    direction: str = Field(default="inbound")  # "inbound" | "outbound"
    duration_seconds: int = Field(default=0)
    started_at: datetime
    ended_at: datetime | None = None
    status: str = Field(default="completed")  # "completed" | "missed" | "voicemail"
    processed_to_metrics: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)


class CallTranscript(rx.Model, table=True):
    """Transcript of a voice call."""

    __tablename__ = "call_transcripts"

    id: int | None = Field(default=None, primary_key=True)
    call_log_id: int = Field(foreign_key="call_logs.id", index=True)
    call_id: str = Field(index=True)  # Denormalized for quick lookup
    raw_transcript: str  # Full transcript text
    speaker_labels: str | None = None  # JSON string of speaker segments
    language: str = Field(default="en")
    confidence_score: float | None = None
    created_at: datetime = Field(default_factory=utc_now)
