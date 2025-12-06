import reflex as rx
from typing import Optional

from ..data.state_schemas import BiomarkerDataPoint, Biomarker
from ..data.demo import (
    DEMO_PORTAL_BIOMARKERS,
    DEMO_PORTAL_TREATMENTS,
    DEMO_PORTAL_APPOINTMENTS,
)

from ..config import get_logger

logger = get_logger("longevity_clinic.biomarker_state")


class PatientBiomarkerState(rx.State):
    biomarkers: list[Biomarker] = DEMO_PORTAL_BIOMARKERS
    selected_biomarker: Optional[Biomarker] = None
    my_treatments: list[dict] = DEMO_PORTAL_TREATMENTS
    upcoming_appointments: list[dict] = DEMO_PORTAL_APPOINTMENTS

    @rx.event
    def select_biomarker(self, biomarker: Biomarker):
        self.selected_biomarker = biomarker

    @rx.event
    def clear_selected_biomarker(self):
        self.selected_biomarker = None

    @rx.event
    def load_biomarkers(self):
        """Load biomarker data - placeholder for API call."""
        print("[DEBUG] load_biomarkers: CALLED", flush=True)
        logger.info("load_biomarkers: Called")
        pass

    @rx.var
    def selected_biomarker_history(self) -> list[BiomarkerDataPoint]:
        if self.selected_biomarker:
            return self.selected_biomarker["history"]
        return []

    @rx.var
    def selected_biomarker_name(self) -> str:
        return self.selected_biomarker["name"] if self.selected_biomarker else ""

    @rx.var
    def selected_biomarker_optimal_range(self) -> dict:
        if self.selected_biomarker:
            return {
                "min": self.selected_biomarker["optimal_min"],
                "max": self.selected_biomarker["optimal_max"],
            }
        return {"min": 0, "max": 0}
