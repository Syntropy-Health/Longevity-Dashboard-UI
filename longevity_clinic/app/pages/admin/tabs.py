"""Admin dashboard tab content."""

import reflex as rx
from ...styles import GlassStyles
from ...components.charts import (
    overview_trend_chart,
    treatment_distribution_chart,
    biomarker_improvement_chart,
)
from .components import (
    stat_card,
    efficiency_stat_card,
    chart_card,
    efficiency_chart_placeholder,
)


def overview_tab() -> rx.Component:
    """Overview dashboard tab content."""
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
            chart_card("Treatment Protocol Distribution", treatment_distribution_chart()),
            chart_card("Avg. Biomarker Improvements", biomarker_improvement_chart()),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )


def efficiency_tab() -> rx.Component:
    """Clinical efficiency dashboard tab content."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h2(
                "Clinical Operational Efficiency",
                class_name=f"text-xl {GlassStyles.HEADING_LIGHT}",
            ),
            rx.el.p(
                "Monitor and optimize clinic performance metrics",
                class_name=GlassStyles.SUBHEADING_LIGHT,
            ),
            class_name="mb-6",
        ),
        
        # Key metrics row
        rx.el.div(
            efficiency_stat_card(
                "Patient Throughput",
                "24.5",
                "patients/day this week",
                "users",
                "teal"
            ),
            efficiency_stat_card(
                "Avg Wait Time",
                "12 min",
                "8% improvement from last week",
                "clock",
                "blue"
            ),
            efficiency_stat_card(
                "Room Utilization",
                "87%",
                "across all treatment rooms",
                "door-open",
                "purple"
            ),
            efficiency_stat_card(
                "Staff Efficiency",
                "94%",
                "appointments on schedule",
                "user-check",
                "emerald"
            ),
            efficiency_stat_card(
                "Treatment Completion",
                "96.2%",
                "protocols completed successfully",
                "circle-check",
                "teal"
            ),
            efficiency_stat_card(
                "Revenue/Hour",
                "$847",
                "+12% from last month",
                "dollar-sign",
                "amber"
            ),
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8",
        ),
        
        # Charts row
        rx.el.div(
            efficiency_chart_placeholder(
                "Daily Patient Flow",
                "Appointment volume and wait times throughout the day"
            ),
            efficiency_chart_placeholder(
                "Treatment Room Utilization",
                "Room occupancy rates by time slot"
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
        ),
        
        # Provider Performance
        rx.el.div(
            rx.el.div(
                rx.el.h3("Provider Performance", class_name="text-lg font-bold text-gray-800 mb-4"),
                rx.el.div(
                    rx.foreach(
                        [
                            {"name": "Dr. Johnson", "patients": 156, "efficiency": 98},
                            {"name": "Dr. Chen", "patients": 142, "efficiency": 95},
                            {"name": "Dr. Patel", "patients": 138, "efficiency": 97},
                            {"name": "Dr. Williams", "patients": 128, "efficiency": 92},
                        ],
                        lambda p: rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span("D", class_name="text-sm font-bold text-teal-600"),
                                    class_name="w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center",
                                ),
                                rx.el.div(
                                    rx.el.p(p["name"], class_name="font-medium text-gray-900"),
                                    rx.el.p(
                                        f"{p['patients']} patients this month",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="ml-3",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        class_name="h-2 rounded-full bg-teal-500",
                                        style={"width": f"{p['efficiency']}%"},
                                    ),
                                    class_name="flex-1 h-2 bg-gray-200 rounded-full mr-3",
                                ),
                                rx.el.span(
                                    f"{p['efficiency']}%",
                                    class_name="text-sm font-medium text-gray-700",
                                ),
                                class_name="flex items-center w-32",
                            ),
                            class_name="flex items-center justify-between py-3",
                        ),
                    ),
                    class_name="divide-y divide-gray-100",
                ),
                class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
            ),
            rx.el.div(
                rx.el.h3("Treatment Completion Rates", class_name="text-lg font-bold text-gray-800 mb-4"),
                rx.el.div(
                    rx.foreach(
                        [
                            {"treatment": "NAD+ IV Therapy", "rate": 98, "color": "teal"},
                            {"treatment": "HBOT Sessions", "rate": 95, "color": "blue"},
                            {"treatment": "Stem Cell", "rate": 92, "color": "purple"},
                            {"treatment": "Peptide Therapy", "rate": 97, "color": "emerald"},
                        ],
                        lambda t: rx.el.div(
                            rx.el.div(
                                rx.el.p(t["treatment"], class_name="font-medium text-gray-900"),
                                rx.el.div(
                                    rx.el.div(
                                        class_name=f"h-3 rounded-full bg-{t['color']}-500",
                                        style={"width": f"{t['rate']}%"},
                                    ),
                                    class_name="flex-1 h-3 bg-gray-200 rounded-full mt-2",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.span(
                                f"{t['rate']}%",
                                class_name="text-lg font-bold text-gray-800 ml-4",
                            ),
                            class_name="flex items-center py-3",
                        ),
                    ),
                    class_name="divide-y divide-gray-100",
                ),
                class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
    )
