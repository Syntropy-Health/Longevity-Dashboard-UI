"""Biomarker database operations."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.model import BiomarkerDefinition, BiomarkerReading
from longevity_clinic.app.functions.utils import generate_biomarker_history

logger = get_logger("longevity_clinic.db_utils.biomarkers")


# =============================================================================
# Biomarker Panel Functions (for UI display)
# =============================================================================


def get_biomarker_panels_sync(user_id: int | None = None) -> list[dict[str, Any]]:
    """Get biomarker panels for display, grouped by category.

    Args:
        user_id: Optional user ID to get specific patient's readings.
                 If None, uses reference values from definitions.

    Returns:
        List of BiomarkerCategory dicts with format:
        [{"category": "...", "metrics": [{"name": ..., "value": ..., ...}]}]
    """
    try:
        with rx.session() as session:
            definitions = session.exec(
                select(BiomarkerDefinition).order_by(BiomarkerDefinition.category)
            ).all()

            if not definitions:
                logger.warning("No biomarker definitions found in database")
                return []

            # Group by category
            categories: dict[str, list[dict[str, Any]]] = {}

            for defn in definitions:
                category = defn.category

                # Get latest reading for this biomarker if user specified
                value = None
                status = "Optimal"
                if user_id:
                    reading = session.exec(
                        select(BiomarkerReading)
                        .where(BiomarkerReading.user_id == user_id)
                        .where(BiomarkerReading.biomarker_id == defn.id)
                        .order_by(BiomarkerReading.measured_at.desc())
                        .limit(1)
                    ).first()

                    if reading:
                        value = reading.value
                        status = reading.status.capitalize()

                # Use optimal midpoint as default if no reading
                if value is None:
                    value = (defn.optimal_min + defn.optimal_max) / 2

                # Build reference range string
                reference_range = f"{defn.optimal_min}-{defn.optimal_max}"

                # Generate history based on value
                volatility = value * 0.05  # 5% volatility

                metric = {
                    "name": defn.name,
                    "value": round(value, 2),
                    "unit": defn.unit,
                    "status": status,
                    "reference_range": reference_range,
                    "history": generate_biomarker_history(value, volatility),
                }

                if category not in categories:
                    categories[category] = []
                categories[category].append(metric)

            # Convert to list format
            return [
                {"category": cat, "metrics": metrics}
                for cat, metrics in categories.items()
            ]

    except Exception as e:
        logger.error("Failed to get biomarker panels: %s", e)
        return []


def get_biomarker_definitions_sync(
    category: str | None = None,
) -> list[dict[str, Any]]:
    """Get all biomarker definitions from database."""
    try:
        with rx.session() as session:
            query = select(BiomarkerDefinition).order_by(BiomarkerDefinition.name)

            if category:
                query = query.where(BiomarkerDefinition.category == category)

            definitions = session.exec(query).all()

            return [
                {
                    "id": d.id,
                    "name": d.name,
                    "short_name": d.short_name,
                    "category": d.category,
                    "unit": d.unit,
                    "min_normal": d.min_normal,
                    "max_normal": d.max_normal,
                    "optimal_min": d.optimal_min,
                    "optimal_max": d.optimal_max,
                    "description": d.description or "",
                    "clinical_significance": d.clinical_significance or "",
                }
                for d in definitions
            ]
    except Exception as e:
        logger.error("Failed to get biomarker definitions: %s", e)
        return []


def get_biomarker_definition_by_name_sync(
    name: str,
) -> dict[str, Any] | None:
    """Get biomarker definition by name."""
    try:
        with rx.session() as session:
            definition = session.exec(
                select(BiomarkerDefinition).where(BiomarkerDefinition.name == name)
            ).first()

            if not definition:
                # Try short_name
                definition = session.exec(
                    select(BiomarkerDefinition).where(
                        BiomarkerDefinition.short_name == name
                    )
                ).first()

            if not definition:
                return None

            return {
                "id": definition.id,
                "name": definition.name,
                "short_name": definition.short_name,
                "category": definition.category,
                "unit": definition.unit,
                "min_normal": definition.min_normal,
                "max_normal": definition.max_normal,
                "optimal_min": definition.optimal_min,
                "optimal_max": definition.optimal_max,
                "description": definition.description or "",
                "clinical_significance": definition.clinical_significance or "",
            }
    except Exception as e:
        logger.error("Failed to get biomarker definition %s: %s", name, e)
        return None


def get_patient_biomarkers_sync(
    user_id: int,
    biomarker_name: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Get biomarker readings for a patient."""
    try:
        with rx.session() as session:
            query = (
                select(BiomarkerReading, BiomarkerDefinition)
                .join(
                    BiomarkerDefinition,
                    BiomarkerReading.biomarker_id == BiomarkerDefinition.id,
                )
                .where(BiomarkerReading.user_id == user_id)
                .order_by(BiomarkerReading.reading_date.desc())
                .limit(limit)
            )

            if biomarker_name:
                query = query.where(
                    (BiomarkerDefinition.name == biomarker_name)
                    | (BiomarkerDefinition.short_name == biomarker_name)
                )

            results = session.exec(query).all()

            return [
                {
                    "id": reading.id,
                    "biomarker_name": definition.name,
                    "short_name": definition.short_name,
                    "category": definition.category,
                    "value": reading.value,
                    "unit": definition.unit,
                    "reading_date": (
                        reading.reading_date.isoformat() if reading.reading_date else ""
                    ),
                    "source": reading.source or "manual",
                    "notes": reading.notes or "",
                    "min_normal": definition.min_normal,
                    "max_normal": definition.max_normal,
                    "optimal_min": definition.optimal_min,
                    "optimal_max": definition.optimal_max,
                }
                for reading, definition in results
            ]
    except Exception as e:
        logger.error("Failed to get biomarkers for user %s: %s", user_id, e)
        return []


def get_latest_biomarkers_sync(
    user_id: int,
) -> dict[str, dict[str, Any]]:
    """Get latest reading for each biomarker for a user."""
    try:
        with rx.session() as session:
            # Get all biomarker definitions
            definitions = session.exec(select(BiomarkerDefinition)).all()

            latest_readings: dict[str, dict[str, Any]] = {}

            for definition in definitions:
                reading = session.exec(
                    select(BiomarkerReading)
                    .where(BiomarkerReading.user_id == user_id)
                    .where(BiomarkerReading.biomarker_id == definition.id)
                    .order_by(BiomarkerReading.reading_date.desc())
                    .limit(1)
                ).first()

                if reading:
                    latest_readings[definition.short_name] = {
                        "value": reading.value,
                        "unit": definition.unit,
                        "date": (
                            reading.reading_date.isoformat()
                            if reading.reading_date
                            else ""
                        ),
                        "name": definition.name,
                        "category": definition.category,
                        "min_normal": definition.min_normal,
                        "max_normal": definition.max_normal,
                        "optimal_min": definition.optimal_min,
                        "optimal_max": definition.optimal_max,
                    }

            return latest_readings
    except Exception as e:
        logger.error("Failed to get latest biomarkers for user %s: %s", user_id, e)
        return {}


def create_biomarker_reading_sync(
    user_id: int,
    biomarker_id: int,
    value: float,
    reading_date: datetime | None = None,
    source: str = "manual",
    notes: str | None = None,
) -> dict[str, Any] | None:
    """Create a biomarker reading."""
    try:
        with rx.session() as session:
            reading = BiomarkerReading(
                user_id=user_id,
                biomarker_id=biomarker_id,
                value=value,
                reading_date=reading_date or datetime.now(UTC),
                source=source,
                notes=notes,
            )
            session.add(reading)
            session.commit()
            session.refresh(reading)

            return {
                "id": reading.id,
                "biomarker_id": reading.biomarker_id,
                "value": reading.value,
                "date": (
                    reading.reading_date.isoformat() if reading.reading_date else ""
                ),
            }
    except Exception as e:
        logger.error("Failed to create biomarker reading: %s", e)
        return None


def get_biomarker_trends_sync(
    user_id: int,
    biomarker_name: str,
    days: int = 365,
) -> list[dict[str, Any]]:
    """Get biomarker readings over time for trend analysis."""
    try:
        from datetime import timedelta

        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        with rx.session() as session:
            definition = session.exec(
                select(BiomarkerDefinition).where(
                    (BiomarkerDefinition.name == biomarker_name)
                    | (BiomarkerDefinition.short_name == biomarker_name)
                )
            ).first()

            if not definition:
                logger.warning("Biomarker definition not found: %s", biomarker_name)
                return []

            readings = session.exec(
                select(BiomarkerReading)
                .where(BiomarkerReading.user_id == user_id)
                .where(BiomarkerReading.biomarker_id == definition.id)
                .where(BiomarkerReading.reading_date >= cutoff_date)
                .order_by(BiomarkerReading.reading_date.asc())
            ).all()

            return [
                {
                    "date": r.reading_date.isoformat() if r.reading_date else "",
                    "value": r.value,
                    "source": r.source or "manual",
                }
                for r in readings
            ]
    except Exception as e:
        logger.error("Failed to get biomarker trends for %s: %s", biomarker_name, e)
        return []
