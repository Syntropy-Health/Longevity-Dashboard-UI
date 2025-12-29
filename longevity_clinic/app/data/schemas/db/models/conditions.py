"""Health condition and symptom trend models."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class Condition(rx.Model, table=True):
    """Health condition/diagnosis for a patient.

    Tracks medical conditions like diabetes, hypertension, etc.
    """

    __tablename__ = "conditions"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)

    # Condition details
    name: str = Field(index=True)
    icd_code: str = Field(default="")  # ICD-10 diagnosis code
    diagnosed_date: str = Field(default="")  # When diagnosed
    status: str = Field(default="active")  # active | managed | resolved
    severity: str = Field(default="mild")  # mild | moderate | severe

    # Treatment info
    treatments: str = Field(default="")  # Current treatments for this condition
    notes: str | None = None

    # Source tracking
    source: str = Field(default="manual")  # manual | seed | ehr
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class SymptomTrend(rx.Model, table=True):
    """Symptom trend tracking over time.

    Aggregates symptom severity changes for trend analysis.
    """

    __tablename__ = "symptom_trends"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)

    # Trend data
    symptom_name: str = Field(index=True)
    current_severity: int = Field(default=0)  # 0-10 scale
    previous_severity: int = Field(default=0)  # 0-10 scale
    trend: str = Field(default="stable")  # improving | worsening | stable
    change_percent: float = Field(default=0.0)
    period: str = Field(default="Last 7 days")  # Time period for comparison

    # Timestamps
    calculated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class DataSource(rx.Model, table=True):
    """Connected device or app data source.

    Tracks wearables, scales, CGMs, apps, and EHR integrations.
    """

    __tablename__ = "data_sources"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)

    # Source details
    name: str = Field(index=True)  # e.g., "Apple Watch Series 9"
    source_type: str = Field(default="wearable")  # wearable | scale | cgm | app | ehr
    status: str = Field(default="disconnected")  # connected | disconnected | error
    icon: str = Field(default="")  # Icon name for UI
    image: str = Field(default="")  # Image path for UI

    # Connection info
    connected: bool = Field(default=False)
    last_sync: str = Field(default="Never")  # Last sync time string
    external_id: str | None = None  # ID in external system

    # Timestamps
    connected_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
