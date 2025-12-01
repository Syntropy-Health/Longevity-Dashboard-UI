import reflex as rx
from app.schemas.symptom import Symptom


class SymptomState(rx.State):
    symptoms: list[Symptom] = [
        Symptom(
            id="sym1",
            name="Headache",
            severity=4,
            timestamp="Today, 10:00 AM",
            notes="Mild throbbing after coffee",
        ),
        Symptom(
            id="sym2",
            name="Fatigue",
            severity=6,
            timestamp="Yesterday, 3:00 PM",
            notes="Post-lunch slump",
        ),
    ]
    view_mode: str = "Timeline"
    filter_options: list[str] = ["Timeline", "Symptoms", "Reminders", "Trends"]

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode

    @rx.event
    def log_symptom(self):
        return rx.toast("Symptom logging coming soon.")