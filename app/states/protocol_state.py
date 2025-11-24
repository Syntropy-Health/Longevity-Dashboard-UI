import reflex as rx
from typing import Optional
import uuid
from datetime import datetime
from app.models import TreatmentProtocol, ProtocolRequest
from app.states.global_state import GlobalState
from app.enums import TreatmentCategory, TreatmentFrequency, TreatmentStatus


class ProtocolState(rx.State):
    protocols: list[TreatmentProtocol] = [
        TreatmentProtocol(
            id="p1",
            name="NAD+ Loading Phase",
            category=TreatmentCategory.IV_THERAPY,
            description="Intensive NAD+ therapy to restore cellular energy levels.",
            duration="4 Weeks",
            frequency=TreatmentFrequency.BI_WEEKLY,
            biomarker_targets=["NAD+", "Sirtuin Activity"],
            status=TreatmentStatus.ACTIVE,
        ),
        TreatmentProtocol(
            id="p2",
            name="Epithalon Cycle",
            category=TreatmentCategory.PEPTIDES,
            description="Telomere length restoration and circadian rhythm reset.",
            duration="10 Days",
            frequency=TreatmentFrequency.DAILY,
            biomarker_targets=["Biological Age", "Melatonin"],
            status=TreatmentStatus.ACTIVE,
        ),
        TreatmentProtocol(
            id="p3",
            name="Hyperbaric Oxygen 2.0",
            category=TreatmentCategory.HYPERBARIC,
            description="Deep tissue oxygenation for stem cell mobilization.",
            duration="20 Sessions",
            frequency=TreatmentFrequency.BI_WEEKLY,
            biomarker_targets=["Stem Cells", "Inflammation"],
            status=TreatmentStatus.ACTIVE,
        ),
    ]
    requests: list[ProtocolRequest] = []
    is_add_modal_open: bool = False
    is_request_modal_open: bool = False
    selected_protocol: Optional[TreatmentProtocol] = None
    request_reason: str = ""

    @rx.var
    def pending_requests(self) -> list[ProtocolRequest]:
        return [r for r in self.requests if r.status == "pending"]

    @rx.event
    def toggle_add_modal(self, is_open: bool):
        self.is_add_modal_open = is_open

    @rx.event
    def add_protocol(self, form_data: dict):
        new_protocol = TreatmentProtocol(
            id=str(uuid.uuid4())[:8],
            name=form_data.get("name", "New Protocol"),
            category=form_data.get("category", "other"),
            description=form_data.get("description", ""),
            duration=form_data.get("duration", ""),
            frequency=form_data.get("frequency", ""),
            biomarker_targets=form_data.get("biomarker_targets", "").split(","),
        )
        self.protocols.append(new_protocol)
        self.is_add_modal_open = False
        return rx.toast("Protocol created successfully.")

    @rx.event
    def delete_protocol(self, protocol_id: str):
        self.protocols = [p for p in self.protocols if p.id != protocol_id]
        return rx.toast("Protocol deleted.")

    @rx.event
    def open_request_modal(self, protocol: TreatmentProtocol):
        self.selected_protocol = protocol
        self.is_request_modal_open = True

    @rx.event
    def close_request_modal(self):
        self.is_request_modal_open = False
        self.selected_protocol = None

    @rx.event
    def handle_request_modal_open_change(self, is_open: bool):
        if not is_open:
            self.close_request_modal()

    @rx.event
    def handle_add_modal_open_change(self, is_open: bool):
        self.is_add_modal_open = is_open

    @rx.event
    def submit_request(self, form_data: dict):
        if not self.selected_protocol:
            return
        new_request = ProtocolRequest(
            id=str(uuid.uuid4())[:8],
            patient_name=GlobalState.user_name,
            protocol_id=self.selected_protocol.id,
            protocol_name=self.selected_protocol.name,
            status="pending",
            reason=form_data.get("reason", ""),
            date=datetime.now().strftime("%Y-%m-%d"),
        )
        self.requests.append(new_request)
        self.is_request_modal_open = False
        self.selected_protocol = None
        return rx.toast("Request submitted to clinic administration.")

    @rx.event
    def approve_request(self, request_id: str):
        for req in self.requests:
            if req.id == request_id:
                req.status = "approved"
        return rx.toast("Protocol request approved.")

    @rx.event
    def reject_request(self, request_id: str):
        for req in self.requests:
            if req.id == request_id:
                req.status = "rejected"
        return rx.toast("Protocol request rejected.")