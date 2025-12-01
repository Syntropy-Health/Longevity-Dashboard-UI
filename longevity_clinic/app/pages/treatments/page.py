"""Treatments main page."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...components.page_components import page_header
from ...states.treatment_state import TreatmentState
from .components import protocol_card, protocol_filters
from .modals import treatment_editor_modal, assignment_modal


def treatments_page() -> rx.Component:
    """Treatment protocols management page."""
    return authenticated_layout(
        rx.el.div(
            page_header(
                "Treatment Protocols",
                button_text="Create Protocol",
                button_icon="plus",
                button_onclick=TreatmentState.open_add_modal,
            ),
            protocol_filters(),
            rx.el.div(
                rx.foreach(TreatmentState.filtered_protocols, protocol_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            treatment_editor_modal(),
            assignment_modal(),
        )
    )
