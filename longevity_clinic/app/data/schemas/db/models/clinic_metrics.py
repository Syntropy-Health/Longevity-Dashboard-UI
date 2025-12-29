"""Clinic metrics models for admin dashboard charts."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class PatientVisit(rx.Model, table=True):
    """Patient visit record for tracking clinic trends."""

    __tablename__ = "patient_visits"

    id: int | None = Field(default=None, primary_key=True)
    period: str = Field(index=True)  # e.g., "Jan", "Feb", "2025-01", etc.
    period_type: str = Field(default="month")  # "day" | "week" | "month" | "quarter"
    active_patients: int = Field(default=0)
    new_patients: int = Field(default=0)
    total_visits: int = Field(default=0)
    notes: str | None = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class TreatmentProtocolMetric(rx.Model, table=True):
    """Treatment protocol metrics for admin dashboard charts."""

    __tablename__ = "treatment_protocol_metrics"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(default="general")
    active_count: int = Field(default=0)
    completed_count: int = Field(default=0)
    success_rate: float = Field(default=0.0)
    avg_duration_days: int = Field(default=0)
    notes: str | None = None
    updated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerAggregate(rx.Model, table=True):
    """Aggregated biomarker scores for trend tracking."""

    __tablename__ = "biomarker_aggregates"

    id: int | None = Field(default=None, primary_key=True)
    period: str = Field(index=True)
    period_type: str = Field(default="week")
    avg_score: float = Field(default=0.0)
    patient_count: int = Field(default=0)
    improvement_pct: float = Field(default=0.0)
    notes: str | None = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class ClinicDailyMetrics(rx.Model, table=True):
    """Daily clinic operational metrics."""

    __tablename__ = "clinic_daily_metrics"

    id: int | None = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    hour: int | None = None

    # Patient flow
    scheduled_appointments: int = Field(default=0)
    walkin_appointments: int = Field(default=0)
    completed_appointments: int = Field(default=0)
    no_shows: int = Field(default=0)

    # Efficiency metrics
    avg_wait_time_minutes: float = Field(default=0.0)
    avg_appointment_duration_minutes: float = Field(default=0.0)
    patient_throughput: float = Field(default=0.0)

    # Room utilization
    room_id: str | None = None
    room_occupancy_pct: float = Field(default=0.0)
    treatments_completed: int = Field(default=0)

    created_at: datetime = Field(default_factory=utc_now)


class ProviderMetrics(rx.Model, table=True):
    """Provider performance metrics."""

    __tablename__ = "provider_metrics"

    id: int | None = Field(default=None, primary_key=True)
    provider_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    provider_name: str = Field(index=True)
    period: str = Field(index=True)
    period_type: str = Field(default="month")

    # Performance metrics
    patient_count: int = Field(default=0)
    efficiency_score: float = Field(default=0.0)
    on_time_rate: float = Field(default=0.0)
    avg_rating: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)
