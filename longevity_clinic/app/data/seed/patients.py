"""Patient seed data for the Longevity Clinic.

Contains:
- DemoPatientSeed dataclass for patient definitions
- Primary demo user (derived from config)
- Secondary demo patients
- Helper functions for patient lookups
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Import Patient type from schemas
from ..schemas.state import Patient


@dataclass
class DemoPatientSeed:
    """Seed data for a demo patient.

    This dataclass provides complete patient information for database seeding.
    The primary demo user (Sarah Chen) is derived from DemoUserConfig in config.py.
    """

    external_id: str
    name: str
    email: str
    phone: str | None = None
    age: int = 35
    gender: str = "Female"
    status: str = "Active"
    biomarker_score: int = 85
    medical_history: str = ""
    is_primary: bool = False  # True for the main demo user

    @classmethod
    def from_demo_config(cls) -> DemoPatientSeed:
        """Create primary demo patient from DemoUserConfig."""
        from ...config import current_config

        cfg = current_config.demo_user
        return cls(
            external_id="P001",
            name=cfg.full_name,
            email=cfg.email,
            phone=cfg.phone,
            age=34,
            gender="Female",
            status="Active",
            biomarker_score=88,
            medical_history="Type 2 Diabetes (managed), Hypertension (mild), Vitamin D Deficiency",
            is_primary=True,
        )

    def to_user_dict(self) -> dict[str, Any]:
        """Convert to dict for User model creation."""
        return {
            "id": self.external_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    def to_patient_state_dict(self) -> dict[str, Any]:
        """Convert to dict for DEMO_PATIENTS_STATE format."""
        return {
            "id": self.external_id,
            "full_name": self.name,
            "email": self.email,
            "phone": self.phone or "",
            "age": self.age,
            "gender": self.gender,
            "last_visit": "2025-01-10",
            "status": self.status,
            "biomarker_score": self.biomarker_score,
            "medical_history": self.medical_history,
            "next_appointment": "2025-01-20",
            "assigned_treatments": [],
        }


def _get_primary_demo_patient() -> DemoPatientSeed:
    """Get the primary demo patient (lazy-loaded to avoid circular imports)."""
    return DemoPatientSeed.from_demo_config()


def _get_demo_phone_number() -> str:
    """Get the demo phone number from config."""
    from ...config import current_config

    return current_config.demo_user.phone


# =============================================================================
# Secondary Demo Patients
# =============================================================================

SECONDARY_DEMO_PATIENTS: list[DemoPatientSeed] = [
    DemoPatientSeed(
        external_id="P002",
        name="Marcus Williams",
        email="marcus.w@example.com",
        phone="+15551234567",
        age=45,
        gender="Male",
        status="Active",
        biomarker_score=78,
        medical_history="High Cholesterol",
    ),
    DemoPatientSeed(
        external_id="P003",
        name="Elena Rodriguez",
        email="elena.r@example.com",
        phone="+15559876543",
        age=38,
        gender="Female",
        status="Active",
        biomarker_score=92,
        medical_history="None",
    ),
    DemoPatientSeed(
        external_id="P004",
        name="James Miller",
        email="james.m@example.com",
        phone="+15554567890",
        age=52,
        gender="Male",
        status="Active",
        biomarker_score=68,
        medical_history="Type 2 Diabetes Pre-cursor",
    ),
    DemoPatientSeed(
        external_id="P005",
        name="Emily Wong",
        email="emily.w@example.com",
        phone="+15552223333",
        age=29,
        gender="Female",
        status="Onboarding",
        biomarker_score=0,
        medical_history="Anemia",
    ),
]


def get_all_demo_patients() -> list[DemoPatientSeed]:
    """Get all demo patients (primary + secondary)."""
    return [_get_primary_demo_patient(), *SECONDARY_DEMO_PATIENTS]


def get_phone_to_patient_seed() -> dict[str, str]:
    """Build phone-to-patient name mapping from all demo patients."""
    mapping = {}
    for patient in get_all_demo_patients():
        if patient.phone:
            mapping[patient.phone] = patient.name
    return mapping


# =============================================================================
# Computed/Legacy Exports
# =============================================================================

# Phone to patient mapping - computed from demo patients
PHONE_TO_PATIENT_SEED: dict[str, str] = get_phone_to_patient_seed()

# Demo patients list (basic format)
DEMO_PATIENTS: list[dict[str, Any]] = [
    p.to_user_dict() for p in get_all_demo_patients()
]

# Demo phone number for API calls (primary user's phone)
DEMO_PHONE_NUMBER: str = _get_demo_phone_number()


def _build_demo_patients_state() -> list[Patient]:
    """Build DEMO_PATIENTS_STATE from DemoPatientSeed objects."""
    return [p.to_patient_state_dict() for p in get_all_demo_patients()]


DEMO_PATIENTS_STATE: list[Patient] = _build_demo_patients_state()


__all__ = [
    "DEMO_PATIENTS",
    "DEMO_PATIENTS_STATE",
    "DEMO_PHONE_NUMBER",
    "PHONE_TO_PATIENT_SEED",
    "SECONDARY_DEMO_PATIENTS",
    "DemoPatientSeed",
    "get_all_demo_patients",
    "get_phone_to_patient_seed",
]
