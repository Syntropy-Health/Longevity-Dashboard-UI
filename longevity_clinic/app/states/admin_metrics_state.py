"""Admin metrics state for clinic dashboard charts.

Manages loading and caching of clinic-wide metrics from the database
for admin dashboard visualizations.
"""

import asyncio
from typing import TypedDict

import reflex as rx
from sqlmodel import select

from ..config import get_logger
from ..data.schemas.db import (
    BiomarkerAggregate,
    ClinicDailyMetrics,
    PatientVisit,
    ProviderMetrics,
    TreatmentProtocolMetric,
)

logger = get_logger("longevity_clinic.admin_metrics_state")


# TypedDicts for chart data (required for rx.foreach)
class TrendDataPoint(TypedDict):
    name: str
    active: int
    new: int


class TreatmentDataPoint(TypedDict):
    name: str
    count: int


class BiomarkerDataPoint(TypedDict):
    name: str
    score: int


class DailyFlowDataPoint(TypedDict):
    time: str
    appointments: int
    walkins: int
    waitTime: int


class RoomUtilizationDataPoint(TypedDict):
    room: str
    occupancy: int
    treatments: int


class ProviderMetricPoint(TypedDict):
    name: str
    patients: int
    efficiency: int


class TreatmentCompletionPoint(TypedDict):
    treatment: str
    rate: int
    color: str


# Default demo data for charts (fallback when DB is empty)
DEFAULT_TREND_DATA: list[TrendDataPoint] = [
    {"name": "Jan", "active": 120, "new": 15},
    {"name": "Feb", "active": 132, "new": 18},
    {"name": "Mar", "active": 145, "new": 20},
    {"name": "Apr", "active": 160, "new": 25},
    {"name": "May", "active": 178, "new": 22},
    {"name": "Jun", "active": 195, "new": 30},
]

DEFAULT_TREATMENT_DATA: list[TreatmentDataPoint] = [
    {"name": "IV Therapy", "count": 45},
    {"name": "Cryo", "count": 30},
    {"name": "Supplements", "count": 85},
    {"name": "Hormone", "count": 25},
    {"name": "Physio", "count": 15},
]

DEFAULT_BIOMARKER_DATA: list[BiomarkerDataPoint] = [
    {"name": "Wk 1", "score": 65},
    {"name": "Wk 4", "score": 72},
    {"name": "Wk 8", "score": 78},
    {"name": "Wk 12", "score": 82},
    {"name": "Wk 16", "score": 88},
]

DEFAULT_DAILY_FLOW_DATA: list[DailyFlowDataPoint] = [
    {"time": "8 AM", "appointments": 4, "walkins": 1, "waitTime": 8},
    {"time": "9 AM", "appointments": 7, "walkins": 2, "waitTime": 12},
    {"time": "10 AM", "appointments": 9, "walkins": 3, "waitTime": 18},
    {"time": "11 AM", "appointments": 8, "walkins": 2, "waitTime": 15},
    {"time": "12 PM", "appointments": 5, "walkins": 1, "waitTime": 10},
    {"time": "1 PM", "appointments": 6, "walkins": 2, "waitTime": 11},
    {"time": "2 PM", "appointments": 8, "walkins": 3, "waitTime": 14},
    {"time": "3 PM", "appointments": 9, "walkins": 2, "waitTime": 16},
    {"time": "4 PM", "appointments": 7, "walkins": 1, "waitTime": 12},
    {"time": "5 PM", "appointments": 4, "walkins": 1, "waitTime": 6},
]

DEFAULT_ROOM_UTILIZATION_DATA: list[RoomUtilizationDataPoint] = [
    {"room": "Room 1", "occupancy": 92, "treatments": 18},
    {"room": "Room 2", "occupancy": 87, "treatments": 16},
    {"room": "Room 3", "occupancy": 78, "treatments": 14},
    {"room": "Room 4", "occupancy": 85, "treatments": 15},
    {"room": "Room 5", "occupancy": 95, "treatments": 19},
    {"room": "Room 6", "occupancy": 72, "treatments": 12},
]

DEFAULT_PROVIDER_METRICS: list[ProviderMetricPoint] = [
    {"name": "Dr. Johnson", "patients": 156, "efficiency": 98},
    {"name": "Dr. Chen", "patients": 142, "efficiency": 95},
    {"name": "Dr. Patel", "patients": 138, "efficiency": 97},
    {"name": "Dr. Williams", "patients": 128, "efficiency": 92},
]

DEFAULT_TREATMENT_COMPLETION: list[TreatmentCompletionPoint] = [
    {"treatment": "NAD+ IV Therapy", "rate": 98, "color": "teal"},
    {"treatment": "HBOT Sessions", "rate": 95, "color": "blue"},
    {"treatment": "Stem Cell", "rate": 92, "color": "purple"},
    {"treatment": "Peptide Therapy", "rate": 97, "color": "emerald"},
]


def _fetch_trend_data_sync() -> list[TrendDataPoint]:
    """Fetch patient visit trend data from DB (sync)."""
    with rx.session() as session:
        visits = session.exec(
            select(PatientVisit)
            .where(PatientVisit.period_type == "month")
            .order_by(PatientVisit.recorded_at)
            .limit(12)
        ).all()

        if not visits:
            return DEFAULT_TREND_DATA

        return [
            {
                "name": v.period,
                "active": v.active_patients,
                "new": v.new_patients,
            }
            for v in visits
        ]


def _fetch_treatment_data_sync() -> list[TreatmentDataPoint]:
    """Fetch treatment protocol distribution from DB (sync)."""
    with rx.session() as session:
        protocols = session.exec(
            select(TreatmentProtocolMetric)
            .order_by(TreatmentProtocolMetric.active_count.desc())
            .limit(10)
        ).all()

        if not protocols:
            return DEFAULT_TREATMENT_DATA

        return [
            {
                "name": p.name,
                "count": p.active_count,
            }
            for p in protocols
        ]


def _fetch_biomarker_data_sync() -> list[BiomarkerDataPoint]:
    """Fetch biomarker aggregate data from DB (sync)."""
    with rx.session() as session:
        aggregates = session.exec(
            select(BiomarkerAggregate).order_by(BiomarkerAggregate.recorded_at).limit(6)
        ).all()

        if not aggregates:
            return DEFAULT_BIOMARKER_DATA

        return [
            {
                "name": b.period,
                "score": int(b.avg_score),
            }
            for b in aggregates
        ]


def _fetch_daily_flow_data_sync() -> list[DailyFlowDataPoint]:
    """Fetch daily patient flow data from DB (sync)."""
    with rx.session() as session:
        # Get today's hourly metrics
        metrics = session.exec(
            select(ClinicDailyMetrics)
            .where(ClinicDailyMetrics.hour.isnot(None))
            .order_by(ClinicDailyMetrics.hour)
            .limit(12)
        ).all()

        if not metrics:
            return DEFAULT_DAILY_FLOW_DATA

        hour_labels = {
            8: "8 AM",
            9: "9 AM",
            10: "10 AM",
            11: "11 AM",
            12: "12 PM",
            13: "1 PM",
            14: "2 PM",
            15: "3 PM",
            16: "4 PM",
            17: "5 PM",
            18: "6 PM",
        }

        return [
            {
                "time": hour_labels.get(m.hour, f"{m.hour}:00"),
                "appointments": m.scheduled_appointments,
                "walkins": m.walkin_appointments,
                "waitTime": int(m.avg_wait_time_minutes),
            }
            for m in metrics
        ]


def _fetch_room_utilization_sync() -> list[RoomUtilizationDataPoint]:
    """Fetch room utilization data from DB (sync)."""
    with rx.session() as session:
        metrics = session.exec(
            select(ClinicDailyMetrics)
            .where(ClinicDailyMetrics.room_id.isnot(None))
            .order_by(ClinicDailyMetrics.room_id)
            .limit(8)
        ).all()

        if not metrics:
            return DEFAULT_ROOM_UTILIZATION_DATA

        return [
            {
                "room": m.room_id,
                "occupancy": int(m.room_occupancy_pct),
                "treatments": m.treatments_completed,
            }
            for m in metrics
        ]


def _fetch_provider_metrics_sync() -> list[ProviderMetricPoint]:
    """Fetch provider performance metrics from DB (sync)."""
    with rx.session() as session:
        providers = session.exec(
            select(ProviderMetrics)
            .order_by(ProviderMetrics.patient_count.desc())
            .limit(6)
        ).all()

        if not providers:
            return DEFAULT_PROVIDER_METRICS

        return [
            {
                "name": p.provider_name,
                "patients": p.patient_count,
                "efficiency": int(p.efficiency_score),
            }
            for p in providers
        ]


class AdminMetricsState(rx.State):
    """State for admin dashboard metrics and charts.

    Loads clinic-wide metrics from the database and provides
    reactive data for chart components.
    """

    # Chart data with proper TypedDict types for rx.foreach
    trend_data: list[TrendDataPoint] = []
    treatment_data: list[TreatmentDataPoint] = []
    biomarker_data: list[BiomarkerDataPoint] = []
    daily_flow_data: list[DailyFlowDataPoint] = []
    room_utilization_data: list[RoomUtilizationDataPoint] = []
    provider_metrics: list[ProviderMetricPoint] = []
    treatment_completion_rates: list[TreatmentCompletionPoint] = []

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False

    @rx.event(background=True)
    async def load_metrics(self):
        """Load all admin dashboard metrics from database."""
        async with self:
            if self._data_loaded:
                logger.debug("load_metrics: Data already loaded, skipping")
                return
            self.is_loading = True

        logger.info("load_metrics: Starting")

        try:
            # Run all DB queries in parallel using thread pool
            (
                trend_data,
                treatment_data,
                biomarker_data,
                daily_flow,
                room_util,
                providers,
            ) = await asyncio.gather(
                asyncio.to_thread(_fetch_trend_data_sync),
                asyncio.to_thread(_fetch_treatment_data_sync),
                asyncio.to_thread(_fetch_biomarker_data_sync),
                asyncio.to_thread(_fetch_daily_flow_data_sync),
                asyncio.to_thread(_fetch_room_utilization_sync),
                asyncio.to_thread(_fetch_provider_metrics_sync),
            )

            async with self:
                self.trend_data = trend_data
                self.treatment_data = treatment_data
                self.biomarker_data = biomarker_data
                self.daily_flow_data = daily_flow
                self.room_utilization_data = room_util
                self.provider_metrics = providers
                # Treatment completion uses same default for now
                self.treatment_completion_rates = DEFAULT_TREATMENT_COMPLETION
                self.is_loading = False
                self._data_loaded = True

            logger.info("load_metrics: Complete")
        except Exception as e:
            logger.error("load_metrics: Failed - %s", e)
            async with self:
                # Fall back to defaults on error
                self.trend_data = DEFAULT_TREND_DATA
                self.treatment_data = DEFAULT_TREATMENT_DATA
                self.biomarker_data = DEFAULT_BIOMARKER_DATA
                self.daily_flow_data = DEFAULT_DAILY_FLOW_DATA
                self.room_utilization_data = DEFAULT_ROOM_UTILIZATION_DATA
                self.provider_metrics = DEFAULT_PROVIDER_METRICS
                self.treatment_completion_rates = DEFAULT_TREATMENT_COMPLETION
                self.is_loading = False
                self._data_loaded = True
