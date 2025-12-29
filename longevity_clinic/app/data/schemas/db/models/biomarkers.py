"""Biomarker models for health tracking."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class BiomarkerDefinition(rx.Model, table=True):
    """Biomarker definition catalog (reference data).

    Defines what biomarkers exist, their categories, units, and ranges.
    """

    __tablename__ = "biomarker_definitions"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g. "VITAMIN_D", "HS_CRP"
    name: str = Field(index=True)
    category: str = Field(index=True)  # Metabolic, Inflammation, Hormones, etc.
    unit: str
    description: str = Field(default="")

    # Reference ranges
    optimal_min: float = Field(default=0.0)
    optimal_max: float = Field(default=0.0)
    critical_min: float = Field(default=0.0)
    critical_max: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerReading(rx.Model, table=True):
    """Individual biomarker reading for a patient."""

    __tablename__ = "biomarker_readings"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    biomarker_id: int = Field(foreign_key="biomarker_definitions.id", index=True)

    value: float
    status: str = Field(default="optimal")  # optimal | warning | critical
    trend: str = Field(default="stable")  # up | down | stable

    # Source tracking
    source: str = Field(default="lab")  # lab | manual | device
    measured_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=utc_now)
