"""Appointment seed data for the Longevity Clinic.

Contains:
- Appointment seed data (full appointments)
- Portal appointments (patient-facing view)
- Treatment types and providers
"""

from __future__ import annotations

from typing import List


# =============================================================================
# Full Appointment Seed Data
# =============================================================================

APPOINTMENTS_SEED: List[dict] = [
    {
        "id": "APT001",
        "title": "NAD+ IV Therapy",
        "description": "Initial NAD+ infusion session - 4 hour treatment",
        "date": "2025-01-16",
        "time": "09:00",
        "duration_minutes": 240,
        "treatment_type": "IV Therapy",
        "patient_id": "P001",
        "patient_name": "Sarah Chen",
        "provider": "Dr. Johnson",
        "status": "confirmed",
        "notes": "First session, monitor for any reactions",
    },
    {
        "id": "APT002",
        "title": "Hyperbaric Oxygen Session",
        "description": "Standard HBOT treatment - 90 minutes at 1.5 ATA",
        "date": "2025-01-16",
        "time": "14:00",
        "duration_minutes": 90,
        "treatment_type": "HBOT",
        "patient_id": "P002",
        "patient_name": "Marcus Williams",
        "provider": "Dr. Chen",
        "status": "scheduled",
        "notes": "",
    },
    {
        "id": "APT003",
        "title": "Biomarker Assessment",
        "description": "Comprehensive longevity panel and consultation",
        "date": "2025-01-17",
        "time": "10:30",
        "duration_minutes": 60,
        "treatment_type": "Assessment",
        "patient_id": "P003",
        "patient_name": "Elena Rodriguez",
        "provider": "Dr. Patel",
        "status": "confirmed",
        "notes": "Follow-up from previous treatment cycle",
    },
    {
        "id": "APT004",
        "title": "Stem Cell Consultation",
        "description": "Initial consultation for stem cell therapy options",
        "date": "2025-01-18",
        "time": "11:00",
        "duration_minutes": 45,
        "treatment_type": "Consultation",
        "patient_id": "P004",
        "patient_name": "James Park",
        "provider": "Dr. Johnson",
        "status": "scheduled",
        "notes": "New patient referral",
    },
    {
        "id": "APT005",
        "title": "Peptide Therapy Follow-up",
        "description": "3-month progress review for BPC-157/TB-500 protocol",
        "date": "2025-01-20",
        "time": "15:30",
        "duration_minutes": 30,
        "treatment_type": "Follow-up",
        "patient_id": "P001",
        "patient_name": "Sarah Chen",
        "provider": "Dr. Chen",
        "status": "scheduled",
        "notes": "Review healing progress",
    },
]


# =============================================================================
# Portal Appointment Seed Data (patient-facing view)
# =============================================================================

PORTAL_APPOINTMENTS_SEED: List[dict] = [
    {
        "id": "a1",
        "title": "IV Therapy Session",
        "date": "Today",
        "time": "2:00 PM",
        "type": "Treatment",
        "provider": "Nurse Jackie",
    },
    {
        "id": "a2",
        "title": "Physician Consultation",
        "date": "Oct 24",
        "time": "10:30 AM",
        "type": "Consultation",
        "provider": "Dr. Administrator",
    },
    {
        "id": "a3",
        "title": "Blood Panel Draw",
        "date": "Nov 01",
        "time": "8:15 AM",
        "type": "Lab Work",
        "provider": "Lab Tech",
    },
]


# =============================================================================
# Treatment Types and Providers
# =============================================================================

TREATMENT_TYPES: List[str] = [
    "NAD+ IV Therapy",
    "Hyperbaric Oxygen (HBOT)",
    "Stem Cell Therapy",
    "Peptide Therapy",
    "Ozone Therapy",
    "Biomarker Assessment",
    "Consultation",
    "Follow-up",
    "Lab Work",
    "Other",
]

PROVIDERS: List[str] = [
    "Dr. Johnson",
    "Dr. Chen",
    "Dr. Patel",
    "Dr. Williams",
]


__all__ = [
    "APPOINTMENTS_SEED",
    "PORTAL_APPOINTMENTS_SEED",
    "TREATMENT_TYPES",
    "PROVIDERS",
]
