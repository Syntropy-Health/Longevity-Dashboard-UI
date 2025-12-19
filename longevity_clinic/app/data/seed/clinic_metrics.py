"""Clinic metrics seed data for admin dashboard charts.

Contains:
- Patient visit trends
- Provider metrics
- Daily clinic metrics
- Biomarker aggregates
"""

from __future__ import annotations

from typing import List


# =============================================================================
# Patient Trend Seed Data (for line charts)
# =============================================================================

PATIENT_TREND_SEED: List[dict] = [
    {"name": "Jan", "active": 120, "new": 15},
    {"name": "Feb", "active": 132, "new": 18},
    {"name": "Mar", "active": 145, "new": 20},
    {"name": "Apr", "active": 160, "new": 25},
    {"name": "May", "active": 178, "new": 22},
    {"name": "Jun", "active": 195, "new": 30},
]


# =============================================================================
# Patient Visit Seed Data (for PatientVisit model)
# =============================================================================

PATIENT_VISIT_SEED: List[dict] = [
    {
        "period": "Jan",
        "period_type": "month",
        "active_patients": 120,
        "new_patients": 15,
        "total_visits": 180,
    },
    {
        "period": "Feb",
        "period_type": "month",
        "active_patients": 132,
        "new_patients": 18,
        "total_visits": 195,
    },
    {
        "period": "Mar",
        "period_type": "month",
        "active_patients": 145,
        "new_patients": 20,
        "total_visits": 218,
    },
    {
        "period": "Apr",
        "period_type": "month",
        "active_patients": 160,
        "new_patients": 25,
        "total_visits": 242,
    },
    {
        "period": "May",
        "period_type": "month",
        "active_patients": 178,
        "new_patients": 22,
        "total_visits": 268,
    },
    {
        "period": "Jun",
        "period_type": "month",
        "active_patients": 195,
        "new_patients": 30,
        "total_visits": 295,
    },
]


# =============================================================================
# Provider Metrics Seed Data
# =============================================================================

PROVIDER_METRICS_SEED: List[dict] = [
    {
        "provider_name": "Dr. Johnson",
        "period_type": "month",
        "patient_count": 156,
        "efficiency_score": 98.0,
        "on_time_rate": 96.0,
        "avg_rating": 4.9,
    },
    {
        "provider_name": "Dr. Chen",
        "period_type": "month",
        "patient_count": 142,
        "efficiency_score": 95.0,
        "on_time_rate": 94.0,
        "avg_rating": 4.8,
    },
    {
        "provider_name": "Dr. Patel",
        "period_type": "month",
        "patient_count": 138,
        "efficiency_score": 97.0,
        "on_time_rate": 95.0,
        "avg_rating": 4.7,
    },
    {
        "provider_name": "Dr. Williams",
        "period_type": "month",
        "patient_count": 128,
        "efficiency_score": 92.0,
        "on_time_rate": 90.0,
        "avg_rating": 4.6,
    },
]


# =============================================================================
# Daily Clinic Metrics Seed Data
# =============================================================================

# Hourly patient flow data
HOURLY_FLOW_SEED: List[dict] = [
    {
        "hour": 8,
        "scheduled_appointments": 4,
        "walkin_appointments": 1,
        "avg_wait_time_minutes": 8.0,
    },
    {
        "hour": 9,
        "scheduled_appointments": 7,
        "walkin_appointments": 2,
        "avg_wait_time_minutes": 12.0,
    },
    {
        "hour": 10,
        "scheduled_appointments": 9,
        "walkin_appointments": 3,
        "avg_wait_time_minutes": 18.0,
    },
    {
        "hour": 11,
        "scheduled_appointments": 8,
        "walkin_appointments": 2,
        "avg_wait_time_minutes": 15.0,
    },
    {
        "hour": 12,
        "scheduled_appointments": 5,
        "walkin_appointments": 1,
        "avg_wait_time_minutes": 10.0,
    },
    {
        "hour": 13,
        "scheduled_appointments": 6,
        "walkin_appointments": 2,
        "avg_wait_time_minutes": 11.0,
    },
    {
        "hour": 14,
        "scheduled_appointments": 8,
        "walkin_appointments": 3,
        "avg_wait_time_minutes": 14.0,
    },
    {
        "hour": 15,
        "scheduled_appointments": 9,
        "walkin_appointments": 2,
        "avg_wait_time_minutes": 16.0,
    },
    {
        "hour": 16,
        "scheduled_appointments": 7,
        "walkin_appointments": 1,
        "avg_wait_time_minutes": 12.0,
    },
    {
        "hour": 17,
        "scheduled_appointments": 4,
        "walkin_appointments": 1,
        "avg_wait_time_minutes": 6.0,
    },
]

# Room utilization data
ROOM_UTILIZATION_SEED: List[dict] = [
    {"room_id": "Room 1", "room_occupancy_pct": 92.0, "treatments_completed": 18},
    {"room_id": "Room 2", "room_occupancy_pct": 87.0, "treatments_completed": 16},
    {"room_id": "Room 3", "room_occupancy_pct": 78.0, "treatments_completed": 14},
    {"room_id": "Room 4", "room_occupancy_pct": 85.0, "treatments_completed": 15},
    {"room_id": "Room 5", "room_occupancy_pct": 95.0, "treatments_completed": 19},
    {"room_id": "Room 6", "room_occupancy_pct": 72.0, "treatments_completed": 12},
]

# Combined daily metrics
DAILY_METRICS_SEED: List[dict] = HOURLY_FLOW_SEED + ROOM_UTILIZATION_SEED


# =============================================================================
# Biomarker Aggregate Seed Data
# =============================================================================

BIOMARKER_AGGREGATE_SEED: List[dict] = [
    {
        "period": "Wk 1",
        "period_type": "week",
        "avg_score": 65.0,
        "patient_count": 45,
        "improvement_pct": 0.0,
    },
    {
        "period": "Wk 4",
        "period_type": "week",
        "avg_score": 72.0,
        "patient_count": 42,
        "improvement_pct": 10.8,
    },
    {
        "period": "Wk 8",
        "period_type": "week",
        "avg_score": 78.0,
        "patient_count": 40,
        "improvement_pct": 20.0,
    },
    {
        "period": "Wk 12",
        "period_type": "week",
        "avg_score": 82.0,
        "patient_count": 38,
        "improvement_pct": 26.2,
    },
    {
        "period": "Wk 16",
        "period_type": "week",
        "avg_score": 88.0,
        "patient_count": 36,
        "improvement_pct": 35.4,
    },
]


__all__ = [
    "PATIENT_TREND_SEED",
    "PATIENT_VISIT_SEED",
    "PROVIDER_METRICS_SEED",
    "HOURLY_FLOW_SEED",
    "ROOM_UTILIZATION_SEED",
    "DAILY_METRICS_SEED",
    "BIOMARKER_AGGREGATE_SEED",
]
