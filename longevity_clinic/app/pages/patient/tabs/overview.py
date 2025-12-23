"""Overview tab component for patient portal."""

import reflex as rx

from ....states import AppointmentState, BiomarkerState
from ....styles.constants import GlassStyles
from ..components import (
    appointment_item,
    biomarker_card,
    biomarker_detail_panel,
    static_metric_card,
    treatment_card,
)


def overview_tab() -> rx.Component:
    """Overview tab with key metrics and biomarkers."""
    return rx.el.div(
        # Key Metrics Grid
        rx.el.div(
            rx.el.h2(
                "Health Metrics", class_name="text-lg font-semibold text-white mb-4"
            ),
            rx.el.div(
                static_metric_card(
                    "Nutrition Score", "82", "/100", "apple", "up", "+5 this week"
                ),
                static_metric_card(
                    "Med Adherence", "94", "%", "pill", "stable", "Consistent"
                ),
                static_metric_card(
                    "Active Conditions", "3", "", "heart-pulse", "down", "-1 resolved"
                ),
                static_metric_card(
                    "Symptom Score", "Low", "", "thermometer", "down", "Improving"
                ),
                static_metric_card(
                    "Data Sources", "6", "connected", "link", "stable", "All synced"
                ),
                static_metric_card(
                    "Check-ins", "5", "this week", "mic", "up", "+2 vs last week"
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8",
            ),
        ),
        # Biomarker Intelligence - Shows biomarkers needing attention
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Biomarker Intelligence",
                    class_name="text-lg font-semibold text-white",
                ),
                rx.cond(
                    BiomarkerState.highlighted_count > 0,
                    rx.el.span(
                        rx.text(BiomarkerState.highlighted_count, " need attention"),
                        class_name="text-xs font-medium text-amber-400 bg-amber-500/10 px-2 py-1 rounded-full border border-amber-500/20",
                    ),
                    rx.el.span(
                        "All optimal",
                        class_name="text-xs font-medium text-teal-400 bg-teal-500/10 px-2 py-1 rounded-full border border-teal-500/20",
                    ),
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.cond(
                BiomarkerState.has_highlighted_biomarkers,
                # Show highlighted (non-optimal/non-stable) biomarkers
                rx.el.div(
                    rx.foreach(BiomarkerState.highlighted_biomarkers, biomarker_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-6",
                ),
                # Fallback: show first 6 biomarkers if all are optimal
                rx.el.div(
                    rx.foreach(BiomarkerState.biomarkers[:6], biomarker_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-6",
                ),
            ),
            biomarker_detail_panel(),
            class_name="mb-10",
        ),
        # Active Protocols and Schedule
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Active Protocols",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(BiomarkerState.my_treatments, treatment_card),
                        class_name="space-y-3",
                    ),
                    class_name="col-span-1 lg:col-span-2",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Upcoming Schedule",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppointmentState.portal_appointments,
                            appointment_item,
                        ),
                        rx.el.a(
                            "View Full Calendar",
                            href="/appointments",
                            class_name="block w-full mt-4 py-2 text-sm text-center text-teal-400 font-medium hover:text-teal-300 border border-teal-500/30 rounded-xl hover:bg-teal-500/10 transition-colors",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-5",
                    ),
                    class_name="col-span-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
        ),
    )
