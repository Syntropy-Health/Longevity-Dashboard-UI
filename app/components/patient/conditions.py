import reflex as rx
from app.states.condition_state import ConditionState
from app.schemas.condition import Condition
from app.enums import ConditionStatus, ConditionSeverity
from app.styles.glass_styles import GlassStyles


def condition_status_badge(status: ConditionStatus) -> rx.Component:
    color_map = {
        ConditionStatus.ACTIVE: "bg-red-500/10 text-red-400 border-red-500/20",
        ConditionStatus.MANAGED: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        ConditionStatus.RESOLVED: "bg-green-500/10 text-green-400 border-green-500/20",
        ConditionStatus.ARCHIVED: "bg-slate-500/10 text-slate-400 border-slate-500/20",
    }
    return rx.el.span(
        status,
        class_name=f"px-2.5 py-1 rounded-full text-xs font-medium border {color_map.get(status, '')}",
    )


def severity_dot(severity: ConditionSeverity) -> rx.Component:
    color_map = {
        ConditionSeverity.MILD: "bg-green-400",
        ConditionSeverity.MODERATE: "bg-yellow-400",
        ConditionSeverity.SEVERE: "bg-red-400",
    }
    return rx.el.div(
        rx.el.div(
            class_name=f"w-2 h-2 rounded-full {color_map.get(severity, 'bg-slate-400')} mr-2"
        ),
        rx.el.span(severity, class_name="text-xs text-slate-400"),
        class_name="flex items-center",
    )


def condition_card(condition: Condition) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(condition.icon, class_name="w-8 h-8 text-white mb-4"),
                class_name="p-3 rounded-xl bg-white/5 w-fit mb-4",
            ),
            rx.el.div(
                condition_status_badge(condition.status),
                rx.el.a(
                    rx.icon(
                        "external-link",
                        class_name="w-4 h-4 text-slate-500 hover:text-white transition-colors",
                    ),
                    class_name="ml-2 cursor-pointer",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.h3(condition.name, class_name="text-lg font-bold text-white mb-1"),
        rx.el.p(
            condition.description, class_name="text-sm text-slate-400 mb-4 line-clamp-2"
        ),
        rx.el.div(
            severity_dot(condition.severity),
            rx.el.div(
                rx.icon("clock", class_name="w-3 h-3 text-slate-500 mr-1"),
                rx.el.span(
                    f"Updated {condition.last_updated}",
                    class_name="text-xs text-slate-500",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center pt-4 border-t border-white/5",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE}",
    )


def conditions_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Your Conditions", class_name="text-2xl font-bold text-white"),
            rx.el.button(
                "+ Add Condition",
                on_click=ConditionState.add_condition,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["All", "Active", "Managed", "Resolved"],
                    lambda status: rx.el.button(
                        status,
                        on_click=lambda: ConditionState.set_filter(status),
                        class_name=rx.cond(
                            ConditionState.filter_status == status,
                            "px-4 py-2 rounded-lg text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
                            "px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all",
                        ),
                    ),
                ),
                class_name="flex gap-2 mb-6 bg-white/5 p-1 rounded-xl w-fit",
            )
        ),
        rx.el.div(
            rx.foreach(ConditionState.filtered_conditions, condition_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="animate-in fade-in duration-500",
    )