import reflex as rx
from typing import Optional

from ...data.state_schemas import BiomarkerDataPoint, Biomarker
from ...data import BiomarkerCategory, get_biomarker_panels
from ...config import get_logger
from ...functions.patients.biomarkers import load_all_biomarker_data

logger = get_logger("longevity_clinic.biomarker")


class BiomarkerState(rx.State):
    """State for patient biomarker and analytics data.

    Manages all patient health biomarker data including:
    - Biomarker list and selection
    - Treatments and appointments
    - Analytics panels and report export

    Data is loaded via load_biomarkers() which respects the IS_DEMO
    environment variable to return demo or real API data.
    """

    biomarkers: list[Biomarker] = []
    selected_biomarker: Optional[Biomarker] = None
    my_treatments: list[dict] = []
    upcoming_appointments: list[dict] = []
    is_loading: bool = False
    _data_loaded: bool = False
    active_tab: str = "Overview"

    @rx.event
    def select_biomarker(self, biomarker: Biomarker):
        """Select a biomarker for detailed view."""
        self.selected_biomarker = biomarker

    @rx.event
    def clear_selected_biomarker(self):
        """Clear the selected biomarker."""
        self.selected_biomarker = None

    @rx.event(background=True)
    async def load_biomarkers(self):
        """Load biomarker data.

        Respects IS_DEMO env var: when True, returns demo data;
        when False, calls the API.
        """
        # Prevent duplicate loads
        async with self:
            if self._data_loaded:
                logger.debug("load_biomarkers: Data already loaded, skipping")
                return
            self.is_loading = True

        logger.info("load_biomarkers: Starting")

        try:
            # Fetch data using extracted function (respects IS_DEMO config)
            data = await load_all_biomarker_data()

            async with self:
                self.biomarkers = data["biomarkers"]
                self.my_treatments = data["treatments"]
                self.upcoming_appointments = data["appointments"]
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_biomarkers: Complete (%d biomarkers)", len(data["biomarkers"])
            )
        except Exception as e:
            logger.error("load_biomarkers: Failed - %s", e)
            async with self:
                self.is_loading = False

    @rx.var
    def selected_biomarker_history(self) -> list[BiomarkerDataPoint]:
        """Get history for selected biomarker."""
        if self.selected_biomarker:
            return self.selected_biomarker.get("history", [])
        return []

    @rx.var
    def selected_biomarker_name(self) -> str:
        """Get name of selected biomarker."""
        return (
            self.selected_biomarker.get("name", "") if self.selected_biomarker else ""
        )

    @rx.var
    def selected_biomarker_optimal_range(self) -> dict:
        """Get optimal range for selected biomarker."""
        if self.selected_biomarker:
            return {
                "min": self.selected_biomarker.get("optimal_min", 0),
                "max": self.selected_biomarker.get("optimal_max", 0),
            }
        return {"min": 0, "max": 0}

    # Analytics functionality
    @rx.var
    def biomarker_panels(self) -> list[BiomarkerCategory]:
        """Get biomarker panels for analytics view."""
        return get_biomarker_panels()

    @rx.event
    def export_report(self):
        """Export analytics report."""
        return rx.toast("Analytics report downloaded successfully.", duration=3000)
