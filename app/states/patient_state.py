import reflex as rx
from app.models import Patient
from app.states.global_state import GlobalState


class PatientState(rx.State):
    patient_data: Patient = Patient()
    has_completed_intake: bool = False

    @rx.event
    def submit_intake(self, form_data: dict):
        """
        Save the patient intake form data.
        """
        self.patient_data = Patient(name=GlobalState.user_name, **form_data)
        self.has_completed_intake = True
        return rx.toast("Intake form submitted successfully. Profile updated.")