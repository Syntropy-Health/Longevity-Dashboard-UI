"""Symptoms tab component for patient portal."""

import reflex as rx

from ....components.indicators import (
    severity_bar,
    severity_comparison,
    trend_badge,
    trend_text,
)
from ....components.paginated_view import paginated_list
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def symptom_card(symptom) -> rx.Component:
    """Symptom card.

    Args:
        symptom: Symptom instance from PatientDashboardState
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    symptom.name,
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.p(
                    rx.text("Severity: ", symptom.severity.capitalize()),
                    class_name="text-sm text-slate-300",
                ),
                rx.el.p(
                    rx.text("Frequency: ", symptom.frequency),
                    class_name="text-xs text-slate-400 mt-1",
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                trend_text(symptom.trend),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Log",
                on_click=lambda: HealthDashboardState.open_symptom_modal(symptom),
                class_name="mt-2 px-3 py-1 text-xs font-medium bg-white/5 hover:bg-white/10 text-slate-300 rounded-lg border border-white/10 transition-all",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def symptom_log_item(log) -> rx.Component:
    """Symptom log item with severity progress bar.

    Args:
        log: SymptomEntry instance from PatientDashboardState
    """
    return rx.el.div(
        rx.el.div(
            rx.el.p(log.timestamp, class_name="text-xs text-teal-400 font-medium"),
            rx.el.p(log.symptom_name, class_name="text-sm font-semibold text-white"),
            rx.el.p(log.notes, class_name="text-xs text-slate-400 mt-1"),
            class_name="flex-1",
        ),
        rx.el.div(
            severity_bar(log.severity, max_value=10, show_label=True, size="sm"),
            class_name="w-20",
        ),
        class_name="flex items-start justify-between py-3 border-b border-white/5 last:border-0",
    )


def reminder_item(reminder: dict) -> rx.Component:
    """Reminder item component."""
    type_icons = {
        "medication": (
            "pill",
            "text-purple-400",
            "bg-purple-500/10",
            "border-purple-500/20",
        ),
        "appointment": (
            "calendar",
            "text-blue-400",
            "bg-blue-500/10",
            "border-blue-500/20",
        ),
        "checkup": (
            "activity",
            "text-teal-400",
            "bg-teal-500/10",
            "border-teal-500/20",
        ),
        "exercise": (
            "dumbbell",
            "text-orange-400",
            "bg-orange-500/10",
            "border-orange-500/20",
        ),
    }
    icon_name, icon_color, bg_color, border_color = type_icons.get(
        reminder.get("type", "checkup"),
        ("bell", "text-slate-400", "bg-slate-500/10", "border-slate-500/20"),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name=f"w-5 h-5 {icon_color}"),
                class_name=f"w-10 h-10 rounded-xl {bg_color} flex items-center justify-center mr-3 border {border_color}",
            ),
            rx.el.div(
                rx.el.h4(
                    reminder["title"], class_name="text-sm font-semibold text-white"
                ),
                rx.el.p(reminder["description"], class_name="text-xs text-slate-400"),
                rx.el.p(reminder["time"], class_name="text-xs text-teal-400 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.cond(
                reminder["completed"],
                rx.el.div(
                    rx.icon("circle-check", class_name="w-5 h-5 text-teal-400"),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon("circle", class_name="w-5 h-5 text-slate-500"),
                    class_name="flex items-center cursor-pointer hover:text-teal-400 transition-colors",
                ),
            ),
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex justify-between items-center mb-3",
    )


def symptom_trend_item(trend) -> rx.Component:
    """Symptom trend item component using indicator components.

    Args:
        trend: SymptomTrend instance from PatientDashboardState
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    trend.symptom_name,
                    class_name="text-base font-semibold text-white mb-1",
                ),
                severity_comparison(
                    current=trend.current_severity,
                    previous=trend.previous_severity,
                    max_value=10,
                ),
                rx.el.p(trend.period, class_name="text-xs text-slate-500 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            trend_badge(trend.trend),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex justify-between items-center mb-3",
    )


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
