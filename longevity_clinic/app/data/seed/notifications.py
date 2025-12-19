"""Notification seed data for the Longevity Clinic.

Contains admin and patient notification seed data for database initialization.
"""

from __future__ import annotations

from typing import List


# =============================================================================
# Admin Notifications Seed Data
# =============================================================================

ADMIN_NOTIFICATIONS_SEED: List[dict] = [
    {
        "id": "1",
        "title": "New Patient Registration",
        "message": "Sarah Chen has completed registration and requires initial assessment scheduling.",
        "type": "info",
        "is_read": False,
        "created_at": "2025-01-15T09:30:00",
        "recipient_role": "admin",
        "patient_id": "P001",
    },
    {
        "id": "2",
        "title": "Lab Results Ready",
        "message": "Comprehensive metabolic panel results for Marcus Williams are now available for review.",
        "type": "lab",
        "is_read": False,
        "created_at": "2025-01-15T08:45:00",
        "recipient_role": "admin",
        "patient_id": "P002",
    },
    {
        "id": "3",
        "title": "Treatment Protocol Update Required",
        "message": "NMN + Resveratrol protocol needs adjustment based on latest research findings.",
        "type": "treatment",
        "is_read": True,
        "created_at": "2025-01-14T16:20:00",
        "recipient_role": "admin",
        "patient_id": None,
    },
    {
        "id": "4",
        "title": "Appointment Rescheduling Request",
        "message": "Elena Rodriguez requested to reschedule tomorrow's hyperbaric oxygen session.",
        "type": "appointment",
        "is_read": False,
        "created_at": "2025-01-15T07:00:00",
        "recipient_role": "admin",
        "patient_id": "P003",
    },
    {
        "id": "5",
        "title": "Critical: Low Inventory Alert",
        "message": "NAD+ IV therapy supplies are running low. Reorder recommended within 48 hours.",
        "type": "warning",
        "is_read": False,
        "created_at": "2025-01-15T06:00:00",
        "recipient_role": "admin",
        "patient_id": None,
    },
    {
        "id": "6",
        "title": "Monthly Report Generated",
        "message": "December 2024 clinical efficiency report is ready for download.",
        "type": "success",
        "is_read": True,
        "created_at": "2025-01-01T00:00:00",
        "recipient_role": "admin",
        "patient_id": None,
    },
]


# =============================================================================
# Patient Notifications Seed Data
# =============================================================================

PATIENT_NOTIFICATIONS_SEED: List[dict] = [
    {
        "id": "101",
        "title": "Upcoming Appointment Reminder",
        "message": "Your NAD+ IV Therapy session is scheduled for tomorrow at 10:00 AM.",
        "type": "appointment",
        "is_read": False,
        "created_at": "2025-01-15T09:00:00",
        "recipient_role": "patient",
        "patient_id": "current",
    },
    {
        "id": "102",
        "title": "Lab Results Available",
        "message": "Your comprehensive metabolic panel results are now ready. Click to view detailed analysis.",
        "type": "lab",
        "is_read": False,
        "created_at": "2025-01-14T14:30:00",
        "recipient_role": "patient",
        "patient_id": "current",
    },
    {
        "id": "103",
        "title": "Treatment Plan Updated",
        "message": "Dr. Johnson has updated your longevity protocol. Review the changes in your treatment plan.",
        "type": "treatment",
        "is_read": True,
        "created_at": "2025-01-13T11:00:00",
        "recipient_role": "patient",
        "patient_id": "current",
    },
    {
        "id": "104",
        "title": "Biomarker Improvement",
        "message": "Great news! Your telomere length has improved by 8% since your last assessment.",
        "type": "success",
        "is_read": True,
        "created_at": "2025-01-10T15:45:00",
        "recipient_role": "patient",
        "patient_id": "current",
    },
    {
        "id": "105",
        "title": "Supplement Reminder",
        "message": "Don't forget to take your NMN and Resveratrol supplements with breakfast.",
        "type": "info",
        "is_read": True,
        "created_at": "2025-01-15T07:00:00",
        "recipient_role": "patient",
        "patient_id": "current",
    },
]


__all__ = [
    "ADMIN_NOTIFICATIONS_SEED",
    "PATIENT_NOTIFICATIONS_SEED",
]
