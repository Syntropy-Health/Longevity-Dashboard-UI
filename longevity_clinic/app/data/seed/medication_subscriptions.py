"""Medication subscription seed data for demo patients.

Contains prescribed medications for patients, primarily for Sarah Chen
(derived from DemoUserConfig).
"""

from __future__ import annotations

from datetime import datetime, timedelta

from ..schemas.llm import PatientTreatmentModel as Prescription

# =============================================================================
# Medication Subscription Seed Data for Sarah Chen (Demo Patient)
# =============================================================================

# Get current date for relative dates
_NOW = datetime.now()
_SIX_MONTHS_AGO = _NOW - timedelta(days=180)
_ONE_YEAR_AGO = _NOW - timedelta(days=365)
_TWO_YEARS_AGO = _NOW - timedelta(days=730)


prescriptions_SEED: list[Prescription] = [
    {
        "id": "MSUB001",
        "name": "Metformin",
        "dosage": "500mg",
        "frequency": "Twice daily with meals",
        "instructions": "Take with breakfast and dinner. Monitor blood sugar levels.",
        "status": "active",
        "adherence_rate": 96.0,
        "prescriber": "Dr. Sarah Johnson",
    },
    {
        "id": "MSUB002",
        "name": "Lisinopril",
        "dosage": "10mg",
        "frequency": "Once daily in morning",
        "instructions": "Take first thing in the morning on an empty stomach.",
        "status": "active",
        "adherence_rate": 92.0,
        "prescriber": "Dr. Michael Chen",
    },
    {
        "id": "MSUB003",
        "name": "Vitamin D3",
        "dosage": "5000 IU",
        "frequency": "Once daily with food",
        "instructions": "Take with a meal containing fat for better absorption.",
        "status": "active",
        "adherence_rate": 88.0,
        "prescriber": "Dr. Emily Davis",
    },
    {
        "id": "MSUB004",
        "name": "Omega-3 Fish Oil",
        "dosage": "1200mg",
        "frequency": "Twice daily",
        "instructions": "Take with meals to reduce fishy aftertaste.",
        "status": "active",
        "adherence_rate": 85.0,
        "prescriber": "Dr. Emily Davis",
    },
    {
        "id": "MSUB005",
        "name": "Magnesium Glycinate",
        "dosage": "400mg",
        "frequency": "Once daily at bedtime",
        "instructions": "Take before bed to promote relaxation and sleep.",
        "status": "active",
        "adherence_rate": 90.0,
        "prescriber": "Dr. Emily Davis",
    },
    {
        "id": "MSUB006",
        "name": "CoQ10",
        "dosage": "100mg",
        "frequency": "Once daily with food",
        "instructions": "Take with a fatty meal for optimal absorption.",
        "status": "active",
        "adherence_rate": 82.0,
        "prescriber": "Dr. Michael Chen",
    },
    {
        "id": "MSUB007",
        "name": "Atorvastatin",
        "dosage": "20mg",
        "frequency": "Once daily at bedtime",
        "instructions": "Take at the same time each night. Avoid grapefruit.",
        "status": "paused",
        "adherence_rate": 78.0,
        "prescriber": "Dr. Sarah Johnson",
    },
]


# =============================================================================
# Database Seed Format (for scripts/load_seed_data.py)
# =============================================================================


def get_prescriptions_for_user(user_id: int) -> list[dict]:
    """Get medication subscription seed data formatted for database insertion.

    Args:
        user_id: The database user ID to associate with subscriptions

    Returns:
        List of dicts ready for Prescription.model_validate()
    """
    return [
        {
            "user_id": user_id,
            "name": sub["name"],
            "dosage": sub["dosage"],
            "frequency": sub["frequency"],
            "instructions": sub["instructions"],
            "prescriber": sub["prescriber"],
            "status": sub["status"],
            "adherence_rate": sub["adherence_rate"],
            "source": "seed",
        }
        for sub in prescriptions_SEED
    ]


__all__ = [
    "get_prescriptions_for_user",
    "prescriptions_SEED",
]
