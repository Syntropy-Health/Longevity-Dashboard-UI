"""Check-in seed data for the Longevity Clinic.

Contains patient check-in seed data for both patient and admin views.
"""

from __future__ import annotations

# Import CheckIn type from schemas
from ..schemas.state import CheckIn

# =============================================================================
# Patient Check-in Seed Data
# =============================================================================

CHECKIN_SEED_DATA: list[CheckIn] = [
    {
        "id": "1",
        "type": "voice",
        "summary": "Feeling good today, energy levels are up. Noticed some minor joint stiffness this morning but it went away after stretching.",
        "timestamp": "Today, 10:30 AM",
        "sentiment": "positive",
        "key_topics": ["energy", "joint stiffness", "exercise"],
        "provider_reviewed": False,
        "patient_name": "Sarah Chen",
    },
    {
        "id": "2",
        "type": "text",
        "summary": "Had a headache yesterday evening. Took some water and rested, felt better after an hour.",
        "timestamp": "Yesterday, 8:15 PM",
        "sentiment": "neutral",
        "key_topics": ["headache", "hydration"],
        "provider_reviewed": True,
        "patient_name": "Sarah Chen",
    },
    {
        "id": "3",
        "type": "voice",
        "summary": "Blood sugar has been stable this week. Following the new meal plan closely.",
        "timestamp": "2 days ago, 9:00 AM",
        "sentiment": "positive",
        "key_topics": ["blood sugar", "diet", "medication"],
        "provider_reviewed": True,
        "patient_name": "Sarah Chen",
    },
]


# =============================================================================
# Admin Check-in Seed Data (extended format with status)
# =============================================================================

ADMIN_CHECKINS_SEED: list[dict] = [
    {
        "id": "1",
        "patient_id": "P001",
        "patient_name": "Sarah Chen",
        "type": "voice",
        "summary": "Feeling good today, energy levels are up. Noticed some minor joint stiffness this morning but it went away after stretching.",
        "raw_transcript": "",
        "timestamp": "Today, 10:30 AM",
        "submitted_at": "2024-12-04T10:30:00",
        "sentiment": "positive",
        "key_topics": ["energy", "joint stiffness", "exercise"],
        "status": "pending",
        "provider_reviewed": False,
        "reviewed_by": "",
        "reviewed_at": "",
    },
    {
        "id": "2",
        "patient_id": "P001",
        "patient_name": "Sarah Chen",
        "type": "text",
        "summary": "Had a headache yesterday evening. Took some water and rested, felt better after an hour. Wondering if it's related to my new medication.",
        "raw_transcript": "",
        "timestamp": "Today, 9:15 AM",
        "submitted_at": "2024-12-04T09:15:00",
        "sentiment": "neutral",
        "key_topics": ["headache", "hydration", "medication"],
        "status": "pending",
        "provider_reviewed": False,
        "reviewed_by": "",
        "reviewed_at": "",
    },
    {
        "id": "3",
        "patient_id": "P001",
        "patient_name": "Sarah Chen",
        "type": "voice",
        "summary": "Blood sugar has been stable this week. Following the new meal plan closely. Feeling more energetic overall.",
        "raw_transcript": "",
        "timestamp": "Yesterday, 2:00 PM",
        "submitted_at": "2024-12-03T14:00:00",
        "sentiment": "positive",
        "key_topics": ["blood sugar", "diet", "medication"],
        "status": "reviewed",
        "provider_reviewed": True,
        "reviewed_by": "Dr. Chen",
        "reviewed_at": "2024-12-03T16:30:00",
    },
    {
        "id": "4",
        "patient_id": "P002",
        "patient_name": "Marcus Williams",
        "type": "text",
        "summary": "Experiencing chest discomfort after exercise. Not sure if related to new workout routine or something else.",
        "raw_transcript": "",
        "timestamp": "Yesterday, 11:00 AM",
        "submitted_at": "2024-12-03T11:00:00",
        "sentiment": "concerned",
        "key_topics": ["chest pain", "exercise", "symptoms"],
        "status": "flagged",
        "provider_reviewed": True,
        "reviewed_by": "Dr. Chen",
        "reviewed_at": "2024-12-03T12:00:00",
    },
    {
        "id": "5",
        "patient_id": "P005",
        "patient_name": "Emily Wong",
        "type": "voice",
        "summary": "Sleep quality has improved since starting the new supplement regimen. Getting about 7-8 hours consistently now.",
        "raw_transcript": "",
        "timestamp": "2 days ago, 8:00 AM",
        "submitted_at": "2024-12-02T08:00:00",
        "sentiment": "positive",
        "key_topics": ["sleep", "supplements"],
        "status": "reviewed",
        "provider_reviewed": True,
        "reviewed_by": "Dr. Smith",
        "reviewed_at": "2024-12-02T10:00:00",
    },
    {
        "id": "6",
        "patient_id": "P003",
        "patient_name": "Elena Rodriguez",
        "type": "voice",
        "summary": "Anxiety levels have been higher this week. Work stress is affecting my sleep and eating patterns.",
        "raw_transcript": "",
        "timestamp": "2 days ago, 4:30 PM",
        "submitted_at": "2024-12-02T16:30:00",
        "sentiment": "negative",
        "key_topics": ["anxiety", "stress", "sleep", "diet"],
        "status": "pending",
        "provider_reviewed": False,
        "reviewed_by": "",
        "reviewed_at": "",
    },
    {
        "id": "7",
        "patient_id": "P004",
        "patient_name": "James Miller",
        "type": "text",
        "summary": "Blood pressure readings have been slightly elevated. Taking medication as prescribed but monitoring closely.",
        "raw_transcript": "",
        "timestamp": "3 days ago, 9:00 AM",
        "submitted_at": "2024-12-01T09:00:00",
        "sentiment": "neutral",
        "key_topics": ["blood pressure", "medication"],
        "status": "reviewed",
        "provider_reviewed": True,
        "reviewed_by": "Dr. Chen",
        "reviewed_at": "2024-12-01T11:00:00",
    },
]


__all__ = [
    "ADMIN_CHECKINS_SEED",
    "CHECKIN_SEED_DATA",
]
