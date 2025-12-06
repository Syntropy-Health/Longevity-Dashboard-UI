"""Symptoms tab component for patient portal."""

import reflex as rx
from ....states.patient_dashboard_state import PatientDashboardState
from ....styles.constants import GlassStyles


def symptom_card(symptom: dict) -> rx.Component:
    """Symptom card."""
    trend_icon = {
        "improving": ("trending-down", "text-teal-400"),
        "stable": ("minus", "text-slate-400"),
        "worsening": ("trending-up", "text-red-400"),
    }
    icon_name, icon_class = trend_icon.get(
        symptom.get("trend", "stable"), ("minus", "text-slate-400")
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    symptom["name"],
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.p(
                    f"Severity: {symptom['severity'].capitalize()}",
                    class_name="text-sm text-slate-300",
                ),
                rx.el.p(
                    f"Frequency: {symptom['frequency']}",
                    class_name="text-xs text-slate-400 mt-1",
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name=f"w-4 h-4 {icon_class} mr-1"),
                rx.el.span(
                    symptom["trend"].capitalize(), class_name=f"text-xs {icon_class}"
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Log",
                on_click=lambda: PatientDashboardState.open_symptom_modal(symptom),
                class_name="mt-2 px-3 py-1 text-xs font-medium bg-white/5 hover:bg-white/10 text-slate-300 rounded-lg border border-white/10 transition-all",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def symptom_log_item(log: dict) -> rx.Component:
    """Symptom log item."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(log["timestamp"], class_name="text-xs text-teal-400 font-medium"),
            rx.el.p(log["symptom_name"], class_name="text-sm font-semibold text-white"),
            rx.el.p(log["notes"], class_name="text-xs text-slate-400 mt-1"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.span(
                f"Severity: {log['severity']}/10",
                class_name="text-xs text-slate-300 bg-slate-700/50 px-2 py-1 rounded",
            ),
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


def symptom_trend_item(trend: dict) -> rx.Component:
    """Symptom trend item component."""
    trend_styles = {
        "improving": ("trending-down", "text-teal-400", "bg-teal-500/10", "Improving"),
        "worsening": ("trending-up", "text-red-400", "bg-red-500/10", "Worsening"),
        "stable": ("minus", "text-slate-400", "bg-slate-500/10", "Stable"),
    }
    icon_name, icon_color, bg_color, label = trend_styles.get(
        trend.get("trend", "stable"),
        ("minus", "text-slate-400", "bg-slate-500/10", "Stable"),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    trend["symptom_name"],
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.div(
                    rx.el.span("Current: ", class_name="text-xs text-slate-400"),
                    rx.el.span(
                        f"{trend['current_severity']}/10",
                        class_name="text-sm text-white font-medium",
                    ),
                    rx.el.span(
                        " vs Previous: ", class_name="text-xs text-slate-400 ml-2"
                    ),
                    rx.el.span(
                        f"{trend['previous_severity']}/10",
                        class_name="text-sm text-slate-300",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.p(trend["period"], class_name="text-xs text-slate-500 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name=f"w-4 h-4 {icon_color} mr-1"),
                rx.el.span(label, class_name=f"text-xs font-medium {icon_color}"),
                class_name=f"flex items-center px-3 py-1 rounded-full {bg_color}",
            ),
            rx.cond(
                trend["change_percent"] > 0,
                rx.el.p(
                    f"{trend['change_percent']:.0f}%",
                    class_name=f"text-xs {icon_color} mt-1 text-right",
                ),
                rx.fragment(),
            ),
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
                on_click=lambda: PatientDashboardState.set_symptoms_filter("timeline"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "timeline",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Symptoms",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("symptoms"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "symptoms",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Reminders",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("reminders"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "reminders",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Trends",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("trends"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "trends",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Content based on filter
        rx.cond(
            PatientDashboardState.symptoms_filter == "timeline",
            rx.el.div(
                rx.el.h3(
                    "Recent Symptom Logs",
                    class_name="text-lg font-semibold text-white mb-4",
                ),
                rx.el.div(
                    rx.foreach(PatientDashboardState.symptom_logs, symptom_log_item),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
            ),
            rx.cond(
                PatientDashboardState.symptoms_filter == "symptoms",
                rx.el.div(
                    rx.foreach(PatientDashboardState.symptoms, symptom_card),
                    class_name="space-y-4",
                ),
                rx.cond(
                    PatientDashboardState.symptoms_filter == "reminders",
                    rx.el.div(
                        rx.el.h3(
                            "Today's Reminders",
                            class_name="text-lg font-semibold text-white mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(PatientDashboardState.reminders, reminder_item),
                            class_name="space-y-0",
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
                        rx.el.div(
                            rx.foreach(
                                PatientDashboardState.symptom_trends, symptom_trend_item
                            ),
                            class_name="space-y-0",
                        ),
                    ),
                ),
            ),
        ),
    )
