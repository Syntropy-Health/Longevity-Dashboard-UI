"""Patient analytics main page."""

import reflex as rx

from ....components.layout import authenticated_layout
from ....components.shared import collapsible_panels_container
from ....states import BiomarkerState
from ....styles.constants import GlassStyles


def analytics_page() -> rx.Component:
    """Patient biomarker analytics page with collapsible category panels."""
    return authenticated_layout(
        rx.el.div(
            # Header section
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Biomarker Analytics",
                        class_name=f"text-4xl {GlassStyles.HEADING}",
                    ),
                    rx.el.p(
                        "Click category panels to expand/collapse detailed metrics",
                        class_name=f"{GlassStyles.SUBHEADING} mt-2 text-lg",
                    ),
                ),
                rx.el.div(
                    # Panel count badge
                    rx.el.span(
                        BiomarkerState.total_panel_count,
                        class_name="text-sm font-semibold text-teal-300 mr-1",
                    ),
                    rx.el.span(
                        "panels",
                        class_name="text-sm text-slate-400 mr-4",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="w-4 h-4 mr-2"),
                        "Export Report",
                        on_click=BiomarkerState.export_report,
                        class_name=f"{GlassStyles.BUTTON_SECONDARY} flex items-center",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-10 gap-4",
            ),
            # Collapsible biomarker panels
            collapsible_panels_container(BiomarkerState.biomarker_panels),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )
