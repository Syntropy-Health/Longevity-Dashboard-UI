"""Item/row components for patient portal tabs.

Reusable item components for lists and timelines.
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ..indicators import (
    severity_bar,
    severity_comparison,
    trend_badge,
)


def symptom_log_item(log) -> rx.Component:
    """Symptom log item with severity progress bar.

    Args:
        log: SymptomEntry instance from HealthDashboardState
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


def symptom_trend_item(trend) -> rx.Component:
    """Symptom trend item component using indicator components.

    Args:
        trend: SymptomTrend instance from HealthDashboardState
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
