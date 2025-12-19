"""Conditions tab component for patient portal."""

import reflex as rx
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def condition_card(condition) -> rx.Component:
    """Condition card.

    Args:
        condition: Condition instance from PatientDashboardState
    """
    status_styles = {
        "active": "bg-amber-500/10 text-amber-300 border-amber-500/20",
        "managed": "bg-teal-500/10 text-teal-300 border-teal-500/20",
        "resolved": "bg-slate-500/10 text-slate-300 border-slate-500/20",
    }
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("heart-pulse", class_name="w-5 h-5 text-rose-400"),
                class_name="w-12 h-12 rounded-xl bg-rose-500/10 flex items-center justify-center mr-4 border border-rose-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    condition.name,
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.p(
                    rx.text("ICD-10: ", condition.icd_code),
                    class_name="text-xs text-slate-400",
                ),
                rx.el.p(
                    rx.text("Diagnosed: ", condition.diagnosed_date),
                    class_name="text-xs text-slate-400 mt-1",
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.span(
                condition.status.capitalize(),
                class_name=rx.match(
                    condition.status,
                    (
                        "active",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['active']}",
                    ),
                    (
                        "managed",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['managed']}",
                    ),
                    (
                        "resolved",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['resolved']}",
                    ),
                    f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['active']}",
                ),
            ),
            rx.el.p(
                condition.severity.capitalize(),
                class_name="text-xs text-slate-400 mt-2",
            ),
            class_name="flex flex-col items-end",
        ),
        on_click=lambda: HealthDashboardState.open_condition_modal(condition),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def conditions_tab() -> rx.Component:
    """Conditions tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Health Conditions", class_name="text-xl font-bold text-white mb-2"
            ),
            rx.el.p(
                "Track and manage your health conditions.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Filter buttons
        rx.el.div(
            rx.el.button(
                rx.fragment("All (", HealthDashboardState.conditions.length(), ")"),
                on_click=lambda: HealthDashboardState.set_conditions_filter("all"),
                class_name=rx.cond(
                    HealthDashboardState.conditions_filter == "all",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Active ({HealthDashboardState.active_conditions_count})",
                on_click=lambda: HealthDashboardState.set_conditions_filter("active"),
                class_name=rx.cond(
                    HealthDashboardState.conditions_filter == "active",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-amber-500/20 text-amber-300 border border-amber-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Managed ({HealthDashboardState.managed_conditions_count})",
                on_click=lambda: HealthDashboardState.set_conditions_filter("managed"),
                class_name=rx.cond(
                    HealthDashboardState.conditions_filter == "managed",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Resolved ({HealthDashboardState.resolved_conditions_count})",
                on_click=lambda: HealthDashboardState.set_conditions_filter("resolved"),
                class_name=rx.cond(
                    HealthDashboardState.conditions_filter == "resolved",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-slate-500/20 text-slate-300 border border-slate-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Conditions List
        rx.el.div(
            rx.foreach(HealthDashboardState.filtered_conditions, condition_card),
            class_name="space-y-4",
        ),
    )
