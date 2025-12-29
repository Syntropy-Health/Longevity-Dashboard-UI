import reflex as rx

from ...config import get_logger
from ...data import BiomarkerCategory
from ...data.schemas.state import Biomarker, BiomarkerDataPoint
from ...functions.db_utils import get_biomarker_panels_sync as get_biomarker_panels
from ...functions.patients.biomarkers import load_all_biomarker_data
from ...states.auth import AuthState

logger = get_logger("longevity_clinic.biomarker")


class BiomarkerState(rx.State):
    """State for patient biomarker and analytics data.

    Manages all patient health biomarker data including:
    - Biomarker list and selection
    - Appointments (upcoming schedule)
    - Analytics panels and report export

    Note: Treatments are now managed by TreatmentPortalState for better
    separation of concerns.

    All data is loaded from the database.
    Seed data with: python scripts/load_seed_data.py
    """

    biomarkers: list[Biomarker] = []
    selected_biomarker: Biomarker | None = None
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
        """Load biomarker data from database for authenticated user.

        Note: Requires seeded database. Run: python scripts/load_seed_data.py
        Note: Treatments are now loaded separately by TreatmentPortalState.
        """
        # Prevent duplicate loads
        async with self:
            if self._data_loaded:
                logger.debug("load_biomarkers: Data already loaded, skipping")
                return
            self.is_loading = True

            # Get patient_id from auth state (numeric id stored as string)
            auth_state = await self.get_state(AuthState)
            user_id_str = auth_state.user.get("id") if auth_state.user else None
            user_id = int(user_id_str) if user_id_str else None

        logger.info("load_biomarkers: Starting for user_id %s", user_id or "default")

        try:
            # Fetch data from database for specific patient
            # Convert user_id (int) to external_id format (e.g., 1 -> 'P001')
            external_id = f"P{user_id:03d}" if user_id else None
            data = await load_all_biomarker_data(patient_id=external_id)

            async with self:
                self.biomarkers = data["biomarkers"]
                # Note: treatments now in TreatmentPortalState
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
    def selected_biomarker_optimal_range(self) -> dict:
        """Get optimal range for selected biomarker."""
        if self.selected_biomarker:
            return {
                "min": self.selected_biomarker.get("optimal_min", 0),
                "max": self.selected_biomarker.get("optimal_max", 0),
            }
        return {"min": 0, "max": 0}

    @rx.var
    def highlighted_biomarkers(self) -> list[Biomarker]:
        """Get biomarkers that need attention (not optimal status or not stable trend).

        Filters for biomarkers where:
        - status is NOT 'Optimal' (could be 'Warning' or 'Critical')
        - OR trend is NOT 'stable' (could be 'up' or 'down')

        This provides a quick view of biomarkers requiring attention.
        Limited to 6 items for the overview display.
        """
        highlighted = [
            b
            for b in self.biomarkers
            if b.get("status", "").lower() != "optimal"
            or b.get("trend", "").lower() != "stable"
        ]
        return highlighted[:6]

    @rx.var
    def has_highlighted_biomarkers(self) -> bool:
        """Check if there are any biomarkers needing attention."""
        return len(self.highlighted_biomarkers) > 0

    @rx.var
    def highlighted_count(self) -> int:
        """Count of biomarkers needing attention."""
        return len(
            [
                b
                for b in self.biomarkers
                if b.get("status", "").lower() != "optimal"
                or b.get("trend", "").lower() != "stable"
            ]
        )

    # Analytics functionality
    @rx.var
    def biomarker_panels(self) -> list[BiomarkerCategory]:
        """Get biomarker panels for analytics view."""
        return get_biomarker_panels()

    @rx.var
    def biomarker_panels_limited(self) -> list[BiomarkerCategory]:
        """Get limited biomarker panels for compact display (max 4 categories)."""
        panels = get_biomarker_panels()
        return panels[:4] if len(panels) > 4 else panels

    @rx.var
    def has_more_panels(self) -> bool:
        """Check if there are more panels than the limited display."""
        panels = get_biomarker_panels()
        return len(panels) > 4

    @rx.var
    def total_panel_count(self) -> int:
        """Get total number of biomarker panels."""
        return len(get_biomarker_panels())

    @rx.var
    def all_panel_names(self) -> list[str]:
        """Get all biomarker panel category names for default accordion expansion.

        Returns:
            List of category names from all panels
        """
        return [panel["category"] for panel in get_biomarker_panels()]

    @rx.event
    def export_report(self):
        """Export biomarker analytics report as CSV."""
        if not self.biomarkers:
            return rx.toast("No biomarker data available to export.", duration=3000)

        # Build CSV content with headers
        lines = [
            "Biomarker Name,Category,Current Value,Unit,Status,Trend,Optimal Min,Optimal Max,Critical Min,Critical Max"
        ]

        for biomarker in self.biomarkers:
            line = ",".join(
                [
                    f'"{biomarker.get("name", "")}"',
                    f'"{biomarker.get("category", "")}"',
                    str(biomarker.get("current_value", "")),
                    f'"{biomarker.get("unit", "")}"',
                    f'"{biomarker.get("status", "")}"',
                    f'"{biomarker.get("trend", "")}"',
                    str(biomarker.get("optimal_min", "")),
                    str(biomarker.get("optimal_max", "")),
                    str(biomarker.get("critical_min", "")),
                    str(biomarker.get("critical_max", "")),
                ]
            )
            lines.append(line)

        csv_content = "\n".join(lines)

        return rx.download(
            data=csv_content,
            filename="biomarker_report.csv",
        )
