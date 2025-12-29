"""Card components for patient portal tabs.

Reusable card components for displaying health data entities.
Uses TAB_CARD_THEMES for standardized theming across cards.
"""

from typing import Any, Callable

import reflex as rx

from ...states import ConditionState, DataSourceState, MedicationState, SymptomState
from ...styles.constants import GlassStyles, TAB_CARD_THEMES
from ..indicators import trend_text


def health_card(
    *,
    icon: str,
    title: rx.Var | str,
    subtitle: rx.Var | str | None = None,
    meta: rx.Var | str | None = None,
    right_content: rx.Component | None = None,
    theme: str = "food",
    on_click: Callable[[], Any] | None = None,
    icon_size: str = "w-5 h-5",
    container_size: str = "w-10 h-10",
) -> rx.Component:
    """Generic health card with standardized theming.

    Args:
        icon: Lucide icon name
        title: Card title
        subtitle: Optional subtitle text
        meta: Optional metadata text (smaller, muted)
        right_content: Optional component on the right side
        theme: Theme key from TAB_CARD_THEMES (food, medication, symptom, condition, etc.)
        on_click: Optional click handler to make card interactive
        icon_size: Size classes for icon
        container_size: Size classes for icon container
    """
    theme_config = TAB_CARD_THEMES.get(theme, TAB_CARD_THEMES["food"])

    card_class = (
        f"{GlassStyles.CARD_INTERACTIVE} flex items-center justify-between py-3"
        if on_click
        else f"{GlassStyles.PANEL} p-4 flex items-center justify-between"
    )

    left_content = rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"{icon_size} {theme_config['icon_color']}"),
            class_name=f"{container_size} rounded-xl {theme_config['icon_bg']} flex items-center justify-center mr-3 border {theme_config['icon_border']}",
        ),
        rx.el.div(
            rx.el.h4(title, class_name="text-sm font-semibold text-white mb-0.5"),
            rx.cond(
                subtitle is not None,
                rx.el.p(subtitle, class_name="text-xs text-slate-300"),
                rx.fragment(),
            ),
            rx.cond(
                meta is not None,
                rx.el.p(meta, class_name="text-[10px] text-slate-400 mt-0.5"),
                rx.fragment(),
            ),
        ),
        class_name="flex items-center flex-1",
    )

    card_props = {"class_name": card_class}
    if on_click:
        card_props["on_click"] = on_click

    return rx.el.div(
        left_content,
        right_content if right_content else rx.fragment(),
        **card_props,
    )


def medication_entry_card(log) -> rx.Component:
    """Medication Entry card (what patient took).

    Args:
        log: MedicationEntry instance (Pydantic model from state)
    """
    right = rx.el.div(
        rx.el.span(
            rx.cond(
                log.taken_at != "",
                rx.moment(log.taken_at, format="MMM D, h:mm A"),
                "UNKNOWN",
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
    )
    return health_card(
        icon="clipboard-check",
        title=log.name,
        subtitle=log.dosage,
        theme="food",  # teal for taken medications
        right_content=right,
        on_click=lambda: MedicationState.select_medication_entry(log),
    )


def medication_subscription_card(med) -> rx.Component:
    """Medication subscription card (prescription).

    Args:
        med: Prescription instance from MedicationState (rx.Var in foreach context)
    """
    right = rx.el.div(
        rx.el.div(
            rx.el.span(
                "Adherence",
                class_name="text-[9px] text-slate-400 uppercase tracking-wider",
            ),
            rx.el.span(
                rx.text(med.adherence_rate.to(int), "%"),
                class_name=rx.cond(
                    med.adherence_rate >= 90,
                    "text-base font-bold text-teal-400",
                    "text-base font-bold text-amber-400",
                ),
            ),
            class_name="text-right",
        ),
        rx.el.span(
            med.status.upper(),
            class_name=rx.cond(
                med.status == "active",
                "mt-1 inline-block px-2 py-0.5 rounded text-[9px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                "mt-1 inline-block px-2 py-0.5 rounded text-[9px] font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20",
            ),
        ),
        class_name="flex flex-col items-end",
    )
    return health_card(
        icon="pill",
        title=med.name,
        subtitle=med.dosage,
        meta=med.frequency,
        theme="medication",
        right_content=right,
        on_click=lambda: MedicationState.open_prescription_modal(med),
    )


def food_entry_card(entry) -> rx.Component:
    """Food entry card.

    Args:
        entry: FoodEntry instance from FoodState
    """
    from ...states import FoodState

    right = rx.el.div(
        rx.el.span(entry.calories, class_name="text-lg font-bold text-white"),
        rx.el.span(" kcal", class_name="text-xs text-slate-400 ml-1"),
        class_name="flex items-baseline",
    )
    return health_card(
        icon="utensils",
        title=entry.name,
        subtitle=rx.text(entry.time, " • ", entry.meal_type.capitalize()),
        theme="food",
        right_content=right,
        on_click=lambda: FoodState.select_food_entry(entry),
        icon_size="w-4 h-4",
    )


def condition_card(condition) -> rx.Component:
    """Condition card.

    Args:
        condition: Condition instance from ConditionState
    """
    status_styles = {
        "active": "bg-amber-500/10 text-amber-300 border-amber-500/20",
        "managed": "bg-teal-500/10 text-teal-300 border-teal-500/20",
        "resolved": "bg-slate-500/10 text-slate-300 border-slate-500/20",
    }
    right = rx.el.div(
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
    )
    return health_card(
        icon="heart-pulse",
        title=condition.name,
        subtitle=rx.text("ICD-10: ", condition.icd_code),
        meta=rx.text("Diagnosed: ", condition.diagnosed_date),
        theme="condition",
        right_content=right,
        on_click=lambda: ConditionState.open_condition_modal(condition),
        container_size="w-12 h-12",
    )


def symptom_card(symptom) -> rx.Component:
    """Symptom card.

    Args:
        symptom: Symptom instance from SymptomState
    """
    right = rx.el.div(
        rx.el.div(
            trend_text(symptom.trend),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Log",
            on_click=lambda: SymptomState.open_symptom_modal(symptom),
            class_name="mt-2 px-3 py-1 text-xs font-medium bg-white/5 hover:bg-white/10 text-slate-300 rounded-lg border border-white/10 transition-all",
        ),
        class_name="flex flex-col items-end",
    )
    return health_card(
        icon="thermometer",
        title=symptom.name,
        subtitle=rx.text("Severity: ", symptom.severity.capitalize()),
        meta=rx.text("Frequency: ", symptom.frequency),
        theme="symptom",
        right_content=right,
        on_click=lambda: SymptomState.open_symptom_modal(symptom),
        container_size="w-12 h-12",
    )


def symptom_log_card(log) -> rx.Component:
    """Symptom log entry card.

    Args:
        log: SymptomEntry instance from SymptomState
    """
    right = rx.el.div(
        rx.el.div(
            rx.el.span(log.severity, class_name="text-lg font-bold text-white"),
            rx.el.span("/10", class_name="text-xs text-slate-400 ml-0.5"),
            class_name="flex items-baseline",
        ),
        rx.el.span(
            log.timestamp,
            class_name="text-[10px] text-slate-500 mt-1 block",
        ),
        class_name="text-right",
    )
    return health_card(
        icon="file-text",
        title=log.symptom_name,
        subtitle=rx.cond(
            log.notes != "",
            log.notes,
            "No notes",
        ),
        theme="symptom",
        right_content=right,
        on_click=lambda: SymptomState.open_symptom_log_modal(log),
    )


def medication_notification_card(notification: dict) -> rx.Component:
    """Medication notification card (formerly reminder).

    Args:
        notification: dict with medication notification data
    """
    from ...states import NotificationState

    right = rx.el.div(
        rx.cond(
            notification.get("completed", False),
            rx.el.div(
                rx.icon("circle-check", class_name="w-5 h-5 text-teal-400"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon("circle", class_name="w-5 h-5 text-slate-500"),
                class_name="flex items-center cursor-pointer hover:text-teal-400 transition-colors",
            ),
        ),
    )
    return health_card(
        icon="pill",
        title=notification.get("title", ""),
        subtitle=notification.get("message", ""),
        meta=notification.get("time", ""),
        theme="medication",
        right_content=right,
        on_click=lambda: NotificationState.toggle_medication_completed(
            notification.get("id", "")
        ),
    )


def data_source_card(source) -> rx.Component:
    """Data source card with device image and connection toggle.

    Args:
        source: DataSource instance from DataSourceState
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
                on_click=lambda: DataSourceState.toggle_data_source_connection(
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
