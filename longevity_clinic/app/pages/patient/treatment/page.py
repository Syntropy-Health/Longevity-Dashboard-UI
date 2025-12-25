"""Patient treatment search main page."""

import reflex as rx

from ....components.collapsible import collapsible_container
from ....components.layout import authenticated_layout
from ....components.shared.treatment import protocol_filters
from ....states import TreatmentSearchState
from ....styles.constants import GlassStyles
from .components import treatment_category_section
from .modals import treatment_details_modal


def treatment_search_page() -> rx.Component:
    """Treatment search page for patients with collapsible categories."""
    return authenticated_layout(
        rx.el.div(
            # Page header
            rx.el.div(
                rx.el.h1(
                    "Treatment Library",
                    class_name=f"text-3xl font-light {GlassStyles.HEADING_LIGHT} tracking-tight",
                ),
                rx.el.p(
                    "Explore and request specialized longevity treatments",
                    class_name=f"{GlassStyles.SUBHEADING_LIGHT} mt-1 text-lg font-light",
                ),
                class_name="mb-8",
            ),
            # Filters
            protocol_filters(
                search_placeholder="Search treatments...",
                on_search_change=TreatmentSearchState.set_search_query,
                on_category_change=TreatmentSearchState.set_category_filter,
            ),
            # Collapsible treatment sections by category - expanded by default
            collapsible_container(
                [
                    rx.foreach(
                        TreatmentSearchState.treatments_by_category,
                        treatment_category_section,
                    )
                ],
                default_expanded=TreatmentSearchState.all_category_names,
            ),
            treatment_details_modal(),
        )
    )
