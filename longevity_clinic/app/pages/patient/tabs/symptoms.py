"""Symptoms tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.tabs import (
    reminder_item,
    symptom_card,
    symptom_log_item,
    symptom_trend_item,
)
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def symptoms_tab() -> rx.Component:
    """Symptoms tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Symptom Tracker", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Track and log your symptoms over time.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Sub-filters
        rx.el.div(
            rx.el.button(
                "Timeline",
                on_click=lambda: HealthDashboardState.set_symptoms_filter("timeline"),
                class_name=rx.cond(
                    HealthDashboardState.symptoms_filter == "timeline",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Symptoms",
                on_click=lambda: HealthDashboardState.set_symptoms_filter("symptoms"),
                class_name=rx.cond(
                    HealthDashboardState.symptoms_filter == "symptoms",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Reminders",
                on_click=lambda: HealthDashboardState.set_symptoms_filter("reminders"),
                class_name=rx.cond(
                    HealthDashboardState.symptoms_filter == "reminders",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Trends",
                on_click=lambda: HealthDashboardState.set_symptoms_filter("trends"),
                class_name=rx.cond(
                    HealthDashboardState.symptoms_filter == "trends",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Content based on filter
        rx.cond(
            HealthDashboardState.symptoms_filter == "timeline",
            rx.el.div(
                rx.el.h3(
                    "Recent Symptom Logs",
                    class_name="text-lg font-semibold text-white mb-4",
                ),
                rx.el.div(
                    paginated_list(
                        items=HealthDashboardState.symptom_logs_paginated,
                        item_renderer=symptom_log_item,
                        has_previous=HealthDashboardState.symptom_logs_has_previous,
                        has_next=HealthDashboardState.symptom_logs_has_next,
                        page_info=HealthDashboardState.symptom_logs_page_info,
                        showing_info=HealthDashboardState.symptom_logs_showing_info,
                        on_previous=HealthDashboardState.symptom_logs_previous_page,
                        on_next=HealthDashboardState.symptom_logs_next_page,
                        empty_icon="clipboard-list",
                        empty_message="No symptom logs yet",
                        empty_subtitle="Start logging symptoms to track them over time",
                        list_class="",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
            ),
            rx.cond(
                HealthDashboardState.symptoms_filter == "symptoms",
                paginated_list(
                    items=HealthDashboardState.symptoms_paginated,
                    item_renderer=symptom_card,
                    has_previous=HealthDashboardState.symptoms_has_previous,
                    has_next=HealthDashboardState.symptoms_has_next,
                    page_info=HealthDashboardState.symptoms_page_info,
                    showing_info=HealthDashboardState.symptoms_showing_info,
                    on_previous=HealthDashboardState.symptoms_previous_page,
                    on_next=HealthDashboardState.symptoms_next_page,
                    empty_icon="thermometer",
                    empty_message="No symptoms tracked",
                    empty_subtitle="Your tracked symptoms will appear here",
                    list_class="space-y-4",
                ),
                rx.cond(
                    HealthDashboardState.symptoms_filter == "reminders",
                    rx.el.div(
                        rx.el.h3(
                            "Today's Reminders",
                            class_name="text-lg font-semibold text-white mb-4",
                        ),
                        paginated_list(
                            items=HealthDashboardState.reminders_paginated,
                            item_renderer=reminder_item,
                            has_previous=HealthDashboardState.reminders_has_previous,
                            has_next=HealthDashboardState.reminders_has_next,
                            page_info=HealthDashboardState.reminders_page_info,
                            showing_info=HealthDashboardState.reminders_showing_info,
                            on_previous=HealthDashboardState.reminders_previous_page,
                            on_next=HealthDashboardState.reminders_next_page,
                            empty_icon="bell",
                            empty_message="No reminders",
                            empty_subtitle="Your reminders will appear here",
                            list_class="space-y-0",
                        ),
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Symptom Trends",
                            class_name="text-lg font-semibold text-white mb-4",
                        ),
                        rx.el.p(
                            "Track how your symptoms are changing over time.",
                            class_name="text-sm text-slate-400 mb-4",
                        ),
                        paginated_list(
                            items=HealthDashboardState.symptom_trends_paginated,
                            item_renderer=symptom_trend_item,
                            has_previous=HealthDashboardState.symptom_trends_has_previous,
                            has_next=HealthDashboardState.symptom_trends_has_next,
                            page_info=HealthDashboardState.symptom_trends_page_info,
                            showing_info=HealthDashboardState.symptom_trends_showing_info,
                            on_previous=HealthDashboardState.symptom_trends_previous_page,
                            on_next=HealthDashboardState.symptom_trends_next_page,
                            empty_icon="trending-up",
                            empty_message="No trend data",
                            empty_subtitle="Symptom trends will appear as you log more data",
                            list_class="space-y-0",
                        ),
                    ),
                ),
            ),
        ),
    )
