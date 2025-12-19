"""Patient analytics main page."""

import reflex as rx
from ....components.layout import authenticated_layout
from ....states import BiomarkerState
from ....styles.constants import GlassStyles
from .components import category_section


def analytics_page() -> rx.Component:
    """Patient biomarker analytics page."""
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Biomarker Analytics",
                        class_name=f"text-4xl {GlassStyles.HEADING}",
                    ),
                    rx.el.p(
                        "Comprehensive health intelligence report",
                        class_name=f"{GlassStyles.SUBHEADING} mt-2 text-lg",
                    ),
                ),
                rx.el.button(
                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                    "Export Report",
                    on_click=BiomarkerState.export_report,
                    class_name=f"{GlassStyles.BUTTON_SECONDARY} flex items-center",
                ),
                class_name="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-16 gap-4",
            ),
            rx.foreach(BiomarkerState.biomarker_panels, category_section),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )
