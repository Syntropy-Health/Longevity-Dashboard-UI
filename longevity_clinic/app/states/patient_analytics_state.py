import reflex as rx

from ..data import BiomarkerCategory, get_biomarker_panels


class PatientAnalyticsState(rx.State):
    active_tab: str = "Overview"

    @rx.var
    def biomarker_panels(self) -> list[BiomarkerCategory]:
        return get_biomarker_panels()

    @rx.event
    def export_report(self):
        return rx.toast("Analytics report downloaded successfully.", duration=3000)
