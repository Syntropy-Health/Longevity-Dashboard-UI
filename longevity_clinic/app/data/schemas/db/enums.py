"""
Enum/choice tables for referential integrity.

These rx.Model tables store valid choices for fields like treatment categories,
biomarker categories, check-in types, etc. They provide:
1. Database-level referential integrity
2. Single source of truth for valid values
3. Ability to add/modify choices without code changes

Usage:
    from longevity_clinic.app.data.schemas.db import TreatmentCategory, CheckInType
"""

from datetime import UTC, datetime

import reflex as rx
from sqlmodel import Field


def utc_now() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)


class TreatmentCategory(rx.Model, table=True):
    """Valid treatment categories (e.g., IV Therapy, Cryotherapy).

    Reference table for Treatment.category field.
    """

    __tablename__ = "treatment_categories"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "IV_THERAPY"
    name: str = Field(index=True)  # e.g., "IV Therapy"
    description: str = Field(default="")
    color: str = Field(default="#3B82F6")  # Tailwind blue-500
    icon: str = Field(default="activity")  # Lucide icon name
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class TreatmentStatus(rx.Model, table=True):
    """Valid treatment statuses (e.g., Active, Completed, Paused).

    Reference table for Treatment.status and PatientTreatment.status fields.
    """

    __tablename__ = "treatment_statuses"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "ACTIVE"
    name: str = Field(index=True)  # e.g., "Active"
    description: str = Field(default="")
    color: str = Field(default="#10B981")  # Tailwind green-500
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerCategory(rx.Model, table=True):
    """Valid biomarker categories (e.g., Metabolic, Inflammation).

    Reference table for BiomarkerDefinition.category field.
    """

    __tablename__ = "biomarker_categories"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "METABOLIC"
    name: str = Field(index=True)  # e.g., "Metabolic Panel"
    description: str = Field(default="")
    color: str = Field(default="#8B5CF6")  # Tailwind violet-500
    icon: str = Field(default="activity")
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class CheckInType(rx.Model, table=True):
    """Valid check-in types (e.g., manual, voice, call).

    Reference table for CheckIn.checkin_type field.
    """

    __tablename__ = "checkin_types"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "VOICE"
    name: str = Field(index=True)  # e.g., "Voice Check-in"
    description: str = Field(default="")
    icon: str = Field(default="message-circle")
    sort_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class UrgencyLevel(rx.Model, table=True):
    """Valid urgency levels (e.g., routine, follow_up, urgent).

    Reference table for CheckIn.urgency_level field.
    """

    __tablename__ = "urgency_levels"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "URGENT"
    name: str = Field(index=True)  # e.g., "Urgent"
    description: str = Field(default="")
    color: str = Field(default="#EF4444")  # Tailwind red-500
    priority: int = Field(default=0)  # Higher = more urgent
    sla_hours: int | None = Field(default=None)  # Response time SLA
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


__all__ = [
    "BiomarkerCategory",
    "CheckInType",
    "TreatmentCategory",
    "TreatmentStatus",
    "UrgencyLevel",
]
