"""Card components for patient portal tabs.

Reusable card components for displaying health data entities.
"""

import reflex as rx

from ...states import HealthDashboardState
from ...styles.constants import GlassStyles
from ..indicators import trend_text


def medication_log_card(log) -> rx.Component:
    """Medication log card (what patient took).

    Args:
        log: MedicationEntry instance
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("clipboard-check", class_name="w-5 h-5 text-teal-400"),
                class_name="w-10 h-10 rounded-lg bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    log.name, class_name="text-sm font-semibold text-white mb-0.5"
                ),
                rx.el.p(log.dosage, class_name="text-xs text-slate-300"),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(
                rx.cond(
                    log.taken_at,
                    rx.moment(log.taken_at, format="MMM D, h:mm A"),
                    "Unknown",
                ),
                class_name="text-xs text-slate-400",
            ),
            rx.cond(
                log.notes != "",
                rx.el.span(
                    log.notes,
                    class_name="text-[10px] text-slate-500 mt-1 block truncate max-w-[120px]",
                ),
                rx.fragment(),
            ),
            class_name="text-right",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between items-center py-3",
    )


def medication_subscription_card(med) -> rx.Component:
    """Medication subscription card (prescription).

    Args:
        med: MedicationSubscription instance from HealthDashboardState
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-5 h-5 text-purple-400"),
                class_name="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center mr-3 border border-purple-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    med.name, class_name="text-sm font-semibold text-white mb-0.5"
                ),
                rx.el.p(med.dosage, class_name="text-xs text-slate-300"),
                rx.el.p(med.frequency, class_name="text-[10px] text-slate-400 mt-0.5"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Adherence",
                    class_name="text-[9px] text-slate-400 uppercase tracking-wider",
                ),
                rx.el.span(
                    rx.text(f"{med.adherence_rate:.0f}%"),
                    class_name=rx.cond(
                        med.adherence_rate >= 90,
                        "text-base font-bold text-teal-400",
                        "text-base font-bold text-amber-400",
                    ),
                ),
                class_name="text-right",
            ),
            rx.el.span(
                med.status.capitalize(),
                class_name=rx.cond(
                    med.status == "active",
                    "mt-1 inline-block px-2 py-0.5 rounded text-[9px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                    "mt-1 inline-block px-2 py-0.5 rounded text-[9px] font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20",
                ),
            ),
            class_name="flex flex-col items-end",
        ),
        on_click=lambda: HealthDashboardState.open_medication_modal(med),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between py-3",
    )


def food_entry_card(entry) -> rx.Component:
    """Food entry card.

    Args:
        entry: FoodEntry instance from HealthDashboardState
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("utensils", class_name="w-4 h-4 text-teal-400"),
                class_name="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(entry.name, class_name="text-sm font-semibold text-white"),
                rx.el.p(
                    rx.text(entry.time, " • ", entry.meal_type.capitalize()),
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(entry.calories, class_name="text-lg font-bold text-white"),
            rx.el.span(" kcal", class_name="text-xs text-slate-400 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between hover:bg-white/10 transition-all cursor-pointer",
    )


def condition_card(condition) -> rx.Component:
    """Condition card.

    Args:
        condition: Condition instance from HealthDashboardState
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


def symptom_card(symptom) -> rx.Component:
    """Symptom card.

    Args:
        symptom: Symptom instance from HealthDashboardState
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


def data_source_card(source) -> rx.Component:
    """Data source card with device image and connection toggle.

    Args:
        source: DataSource instance from HealthDashboardState
    """
    return rx.el.div(
        rx.el.div(
            # Device image/icon
            rx.el.div(
                rx.el.img(
                    src=source.image,
                    class_name="w-10 h-10 object-contain",
                ),
                class_name=rx.cond(
                    source.connected,
                    "w-14 h-14 rounded-xl bg-teal-500/10 flex items-center justify-center mr-4 border border-teal-500/20",
                    "w-14 h-14 rounded-xl bg-slate-500/10 flex items-center justify-center mr-4 border border-slate-500/20 opacity-60",
                ),
            ),
            rx.el.div(
                rx.el.h4(
                    source.name,
                    class_name=rx.cond(
                        source.connected,
                        "text-base font-semibold text-white mb-1",
                        "text-base font-semibold text-slate-400 mb-1",
                    ),
                ),
                rx.el.p(source.type.capitalize(), class_name="text-xs text-slate-400"),
                rx.el.p(
                    rx.fragment("Last sync: ", source.last_sync),
                    class_name=rx.cond(
                        source.connected,
                        "text-xs text-slate-400 mt-1",
                        "text-xs text-slate-500 mt-1",
                    ),
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            # Connection toggle switch
            rx.el.button(
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            source.connected,
                            "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                            "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                        ),
                    ),
                    class_name=rx.cond(
                        source.connected,
                        "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                        "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                    ),
                ),
                on_click=lambda: HealthDashboardState.toggle_data_source_connection(
                    source.id
                ),
                class_name="focus:outline-none",
            ),
            rx.el.span(
                rx.cond(source.connected, "Connected", "Disconnected"),
                class_name=rx.cond(
                    source.connected,
                    "text-xs text-teal-400 mt-2",
                    "text-xs text-slate-500 mt-2",
                ),
            ),
            class_name="flex flex-col items-center",
        ),
        class_name=rx.cond(
            source.connected,
            f"{GlassStyles.CARD_INTERACTIVE} flex justify-between items-center",
            "group relative overflow-hidden rounded-2xl p-6 bg-white/3 border border-white/5 backdrop-blur-md transition-all duration-300 flex justify-between items-center opacity-80",
        ),
    )
