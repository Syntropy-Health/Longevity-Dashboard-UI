"""Treatment page components."""

import reflex as rx

from ....components.shared.treatment import (
    protocol_filters as shared_protocol_filters,
    treatment_card as shared_treatment_card,
)
from ....data import TREATMENT_CATEGORIES
from ....states import TreatmentProtocol, TreatmentState


def protocol_card(protocol: TreatmentProtocol) -> rx.Component:
    """Treatment protocol card component for admin view.

    Uses the shared treatment_card with Edit/Assign button layout.
    """
    return shared_treatment_card(
        protocol=protocol,
        on_primary_click=lambda: TreatmentState.open_assign_modal(protocol),
        on_secondary_click=lambda: TreatmentState.open_edit_modal(protocol),
        primary_label="Assign",
        secondary_label="Edit",
        show_frequency=True,
        compact=True,
    )


def protocol_filters() -> rx.Component:
    """Protocol filter controls."""
    return shared_protocol_filters(
        search_placeholder="Search protocols...",
        on_search_change=TreatmentState.set_search_query,
        on_category_change=TreatmentState.set_category_filter,
        categories=TREATMENT_CATEGORIES,
    )
