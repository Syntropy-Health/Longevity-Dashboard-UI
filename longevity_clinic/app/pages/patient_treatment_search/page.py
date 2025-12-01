"""Patient treatment search main page."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...states.treatment_search_state import TreatmentSearchState
from ...config import current_config
from .components import treatment_card
from .modals import treatment_details_modal


def treatment_search_page() -> rx.Component:
    """Treatment search page for patients."""
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Treatment Library",
                    class_name="text-3xl font-light text-gray-900 tracking-tight",
                ),
                rx.el.p(
                    "Explore and request specialized longevity treatments",
                    class_name="text-gray-500 mt-1 text-lg font-light",
                ),
                class_name="mb-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-gray-400 absolute left-4 top-3.5",
                    ),
                    rx.el.input(
                        placeholder="Search treatments...",
                        on_change=TreatmentSearchState.set_search_query,
                        class_name=f"pl-12 w-full py-3 {current_config.glass_input_style} text-sm font-medium",
                    ),
                    class_name="relative flex-1 max-w-md",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="All"),
                    rx.el.option("IV Therapy", value="IV Therapy"),
                    rx.el.option("Cryotherapy", value="Cryotherapy"),
                    rx.el.option("Supplements", value="Supplements"),
                    rx.el.option("Hormone Therapy", value="Hormone Therapy"),
                    rx.el.option("Physical Therapy", value="Physical Therapy"),
                    rx.el.option("Spa Services", value="Spa Services"),
                    on_change=TreatmentSearchState.set_category_filter,
                    class_name=f"py-3 px-6 {current_config.glass_input_style} cursor-pointer text-sm font-medium text-gray-700",
                ),
                class_name="flex gap-4 mb-10 flex-wrap items-center",
            ),
            rx.el.div(
                rx.foreach(TreatmentSearchState.filtered_treatments, treatment_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
            ),
            treatment_details_modal(),
        )
    )
