"""Biomarker database operations."""

from __future__ import annotations

from typing import Any

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import BiomarkerDefinition, BiomarkerReading
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


def get_patient_biomarkers_sync(
    user_id: int | None = None,
    external_id: str | None = None,
    biomarker_name: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Get biomarkers with latest readings for a patient.

    Args:
        user_id: Database user ID
        external_id: External user ID (e.g., 'P001')
        biomarker_name: Optional filter by biomarker name
        limit: Maximum number of readings to return

    Returns:
        List of Biomarker dicts with current value and history
    """
    from .users import get_user_by_external_id_sync

    try:
        # Resolve user_id from external_id if needed
        if not user_id and external_id:
            user = get_user_by_external_id_sync(external_id)
            user_id = user.id if user else None

        if not user_id:
            logger.warning("get_patient_biomarkers_sync: No user_id provided")
            return []

        with rx.session() as session:
            # Get all definitions
            defs_query = select(BiomarkerDefinition)
            if biomarker_name:
                defs_query = defs_query.where(
                    (BiomarkerDefinition.name == biomarker_name)
                    | (BiomarkerDefinition.short_name == biomarker_name)
                )
            defs = session.exec(defs_query).all()

            result = []
            for d in defs:
                # Get readings for this biomarker, ordered by date
                readings = session.exec(
                    select(BiomarkerReading)
                    .where(
                        BiomarkerReading.user_id == user_id,
                        BiomarkerReading.biomarker_id == d.id,
                    )
                    .order_by(BiomarkerReading.measured_at.desc())
                    .limit(limit)
                ).all()

                if not readings:
                    continue

                latest = readings[0]
                # Build history from readings (last 6 for chart)
                history = [
                    {"date": r.measured_at.strftime("%b"), "value": r.value}
                    for r in reversed(readings[-6:])
                ]

                result.append(
                    {
                        "id": d.code,
                        "name": d.name,
                        "category": d.category,
                        "unit": d.unit,
                        "description": d.description or "",
                        "optimal_min": d.optimal_min,
                        "optimal_max": d.optimal_max,
                        "critical_min": d.critical_min,
                        "critical_max": d.critical_max,
                        "current_value": latest.value,
                        "status": (
                            latest.status.capitalize() if latest.status else "Optimal"
                        ),
                        "trend": latest.trend or "stable",
                        "history": history,
                    }
                )

            return result
    except Exception as e:
        logger.error("Failed to get biomarkers for user %s: %s", user_id, e)
        return []
