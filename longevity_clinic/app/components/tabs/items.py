"""Item/row components for patient portal tabs.

Reusable item components for lists and timelines.
"""

import reflex as rx

from ...states import SymptomState
from ...styles.constants import GlassStyles
from ..indicators import (
    severity_bar,
    severity_comparison,
    trend_badge,
)


def symptom_log_item(log) -> rx.Component:
    """Symptom log item with severity progress bar.

    Args:
        log: SymptomEntry instance from SymptomState
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
        class_name="flex items-start justify-between py-3 border-b border-white/5 last:border-0 cursor-pointer hover:bg-white/5 px-2 -mx-2 rounded-lg transition-colors",
        on_click=lambda: SymptomState.open_symptom_log_modal(log),
    )


def symptom_trend_item(trend) -> rx.Component:
    """Symptom trend item component using indicator components.

    Args:
        trend: SymptomTrend instance from SymptomState
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
