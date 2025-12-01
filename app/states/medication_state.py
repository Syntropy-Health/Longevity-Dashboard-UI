import reflex as rx
from app.schemas.medication import Medication


class MedicationState(rx.State):
    medications: list[Medication] = [
        Medication(
            id="med1",
            name="Metformin",
            dosage="500mg",
            frequency="Daily",
            efficacy_rating=8,
            next_refill="2024-03-15",
            adherence_score=95,
        ),
        Medication(
            id="med2",
            name="Vitamin D3",
            dosage="5000 IU",
            frequency="Daily",
            efficacy_rating=9,
            next_refill="2024-04-01",
            adherence_score=100,
        ),
    ]
    overall_efficacy_score: int = 88

    @rx.event
    def mark_taken(self, med_id: str):
        return rx.toast("Medication marked as taken.")