"""Admin dashboard overview tab with patient trends, treatment distribution, and biomarker charts."""

import reflex as rx

from ....styles import GlassStyles
from ..components import stat_card, chart_card
from .charts import (
    overview_trend_chart,
    treatment_distribution_chart,
    biomarker_improvement_chart,
)


def overview_tab() -> rx.Component:
    """Overview dashboard tab content.

    Displays key clinic metrics and charts:
    - Total patients, active protocols, appointments today, avg duration
    - Patient growth trends chart
    - Treatment protocol distribution chart
    - Average biomarker improvements chart
    """
    return rx.el.div(
        # Stats row
        rx.el.div(
            stat_card("Total Patients", "1,284", "+12%", True, "users"),
            stat_card("Active Protocols", "42", "+4%", True, "activity"),
            stat_card("Appointments Today", "18", "-2%", False, "calendar"),
            stat_card("Avg. Appt. Duration", "45min", "+8%", True, "clock"),
            class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8",
        ),
        # Charts row
        rx.el.div(
            chart_card("Patient Growth Trends", overview_trend_chart()),
            chart_card(
                "Treatment Protocol Distribution", treatment_distribution_chart()
            ),
            chart_card("Avg. Biomarker Improvements", biomarker_improvement_chart()),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )
