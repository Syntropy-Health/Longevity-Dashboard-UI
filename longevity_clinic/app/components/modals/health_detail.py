"""Health detail modal components for viewing entity details.

This module provides unified detail modals for health data entities:
- Food entries
- Medication entries (logs)
- Prescriptions (medication subscriptions)
- Symptoms
- Symptom logs (entries)

Design follows the pattern established in checkin_detail.py using
glassmorphism styles and consistent layout.
"""

import reflex as rx

from ...styles.constants import TAB_CARD_THEMES, GlassStyles


def _detail_row(
    label: str, value: rx.Var | str, highlight: bool = False
) -> rx.Component:
    """Single row in a detail grid.

    Args:
        label: Label text
        value: Value to display (can be rx.Var or string)
        highlight: Whether to highlight the value
    """
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
        ),
        rx.el.p(
            value,
            class_name=f"text-white {'font-semibold' if highlight else ''}",
        ),
    )


def _modal_header(
    title: str,
    icon: str,
    theme: str = "food",
) -> rx.Component:
    """Modal header with icon and title.

    Args:
        title: Modal title
        icon: Lucide icon name
        theme: Theme key from TAB_CARD_THEMES
    """
    theme_config = TAB_CARD_THEMES.get(theme, TAB_CARD_THEMES["food"])

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-6 h-6 {theme_config['icon_color']}"),
                class_name=f"w-12 h-12 rounded-xl {theme_config['icon_bg']} flex items-center justify-center mr-4 border {theme_config['icon_border']}",
            ),
            rx.radix.primitives.dialog.title(
                title,
                class_name="text-xl font-bold text-white",
            ),
            class_name="flex items-center",
        ),
        rx.radix.primitives.dialog.close(
            rx.el.button(
                rx.icon("x", class_name="w-5 h-5"),
                class_name="text-slate-400 hover:text-white transition-colors",
            ),
        ),
        class_name="flex items-center justify-between mb-6",
    )


def food_detail_modal(
    show_modal: rx.Var[bool],
    entry_name: rx.Var[str],
    entry_calories: rx.Var[int],
    entry_protein: rx.Var[float],
    entry_carbs: rx.Var[float],
    entry_fat: rx.Var[float],
    entry_time: rx.Var[str],
    entry_meal_type: rx.Var[str],
    on_close: rx.EventHandler,
) -> rx.Component:
    """Food entry detail modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        entry_name: Food name
        entry_calories: Calorie count
        entry_protein: Protein grams
        entry_carbs: Carb grams
        entry_fat: Fat grams
        entry_time: Time consumed
        entry_meal_type: Meal category
        on_close: Event handler to close modal

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    _modal_header("Food Entry", "utensils", "food"),
                    # Main info grid
                    rx.el.div(
                        _detail_row("Food Item", entry_name, highlight=True),
                        _detail_row("Time", entry_time),
                        _detail_row("Meal Type", entry_meal_type),
                        class_name=f"grid grid-cols-3 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Nutrition section
                    rx.el.div(
                        rx.el.p(
                            "Nutrition",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-3",
                        ),
                        rx.el.div(
                            # Calories - featured
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "flame", class_name="w-5 h-5 text-orange-400"
                                    ),
                                    class_name="w-10 h-10 rounded-lg bg-orange-500/10 flex items-center justify-center mr-3 border border-orange-500/20",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Calories", class_name="text-xs text-slate-400"
                                    ),
                                    rx.el.p(
                                        rx.text(entry_calories, " kcal"),
                                        class_name="text-2xl font-bold text-white",
                                    ),
                                ),
                                class_name="flex items-center",
                            ),
                            class_name="mb-4",
                        ),
                        # Macros grid
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Protein", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.p(
                                    rx.text(entry_protein, "g"),
                                    class_name="text-lg font-semibold text-teal-400",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Carbs", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.p(
                                    rx.text(entry_carbs, "g"),
                                    class_name="text-lg font-semibold text-blue-400",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Fat", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.p(
                                    rx.text(entry_fat, "g"),
                                    class_name="text-lg font-semibold text-amber-400",
                                ),
                            ),
                            class_name="grid grid-cols-3 gap-4",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Close button
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def medication_entry_detail_modal(
    show_modal: rx.Var[bool],
    entry_name: rx.Var[str],
    entry_dosage: rx.Var[str],
    entry_taken_at: rx.Var[str],
    entry_notes: rx.Var[str],
    on_close: rx.EventHandler,
) -> rx.Component:
    """Medication entry (log) detail modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        entry_name: Medication name
        entry_dosage: Dosage taken
        entry_taken_at: Timestamp when taken
        entry_notes: Additional notes
        on_close: Event handler to close modal

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    _modal_header("Medication Log", "clipboard-check", "food"),
                    # Main info
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Medication",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                entry_name,
                                class_name="text-xl font-bold text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Dosage",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                entry_dosage,
                                class_name="text-white",
                            ),
                        ),
                        class_name=f"grid grid-cols-2 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Timing
                    rx.el.div(
                        rx.el.div(
                            rx.icon("clock", class_name="w-4 h-4 text-slate-400 mr-2"),
                            rx.el.span("Taken: ", class_name="text-slate-400"),
                            rx.cond(
                                entry_taken_at != "",
                                rx.moment(
                                    entry_taken_at, format="MMMM D, YYYY [at] h:mm A"
                                ),
                                rx.text("Unknown time"),
                            ),
                            class_name="flex items-center text-white",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Notes section (conditional)
                    rx.cond(
                        entry_notes != "",
                        rx.el.div(
                            rx.el.p(
                                "Notes",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                            ),
                            rx.el.p(
                                entry_notes,
                                class_name="text-sm text-slate-300 leading-relaxed",
                            ),
                            class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    # Close button
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def prescription_detail_modal(
    show_modal: rx.Var[bool],
    prescription_name: rx.Var[str],
    prescription_dosage: rx.Var[str],
    prescription_frequency: rx.Var[str],
    prescription_instructions: rx.Var[str],
    prescription_status: rx.Var[str],
    prescription_adherence: rx.Var[float],
    prescription_assigned_by: rx.Var[str],
    on_close: rx.EventHandler,
    on_log_dose: rx.EventHandler | None = None,
) -> rx.Component:
    """Prescription (medication subscription) detail modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        prescription_name: Medication name
        prescription_dosage: Prescribed dosage
        prescription_frequency: How often to take
        prescription_instructions: Taking instructions
        prescription_status: active/paused/completed
        prescription_adherence: Adherence rate 0-100
        prescription_assigned_by: Prescribing provider
        on_close: Event handler to close modal
        on_log_dose: Optional handler to log a dose

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    _modal_header("Prescription Details", "pill", "medication"),
                    # Header with name and status
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                prescription_name,
                                class_name="text-xl font-bold text-white mb-1",
                            ),
                            rx.el.span(
                                prescription_status,
                                class_name=rx.cond(
                                    prescription_status == "active",
                                    "px-3 py-1 rounded-full text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                                    "px-3 py-1 rounded-full text-xs font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20",
                                ),
                            ),
                        ),
                        # Adherence badge
                        rx.el.div(
                            rx.el.p(
                                "Adherence", class_name="text-xs text-slate-400 mb-1"
                            ),
                            rx.el.p(
                                rx.text(prescription_adherence, "%"),
                                class_name=rx.cond(
                                    prescription_adherence >= 90,
                                    "text-2xl font-bold text-teal-400",
                                    rx.cond(
                                        prescription_adherence >= 70,
                                        "text-2xl font-bold text-amber-400",
                                        "text-2xl font-bold text-red-400",
                                    ),
                                ),
                            ),
                            class_name="text-right",
                        ),
                        class_name=f"flex justify-between items-start {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Dosage and frequency
                    rx.el.div(
                        _detail_row("Dosage", prescription_dosage, highlight=True),
                        _detail_row("Frequency", prescription_frequency),
                        _detail_row("Prescribed By", prescription_assigned_by),
                        class_name=f"grid grid-cols-3 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Instructions
                    rx.cond(
                        prescription_instructions != "",
                        rx.el.div(
                            rx.el.p(
                                "Instructions",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                            ),
                            rx.el.p(
                                prescription_instructions,
                                class_name="text-sm text-slate-300 leading-relaxed",
                            ),
                            class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.cond(
                            on_log_dose is not None,  # type: ignore[arg-type]
                            (
                                rx.el.button(
                                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                                    "Log Dose",
                                    on_click=on_log_dose,
                                    class_name=f"{GlassStyles.BUTTON_PRIMARY} flex items-center",
                                )
                                if on_log_dose
                                else rx.fragment()
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex justify-between",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg {GlassStyles.MODAL} z-50",
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def symptom_detail_modal(
    show_modal: rx.Var[bool],
    symptom_name: rx.Var[str],
    symptom_severity: rx.Var[str],
    symptom_frequency: rx.Var[str],
    symptom_trend: rx.Var[str],
    on_close: rx.EventHandler,
    on_log_symptom: rx.EventHandler | None = None,
) -> rx.Component:
    """Symptom detail modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        symptom_name: Symptom name
        symptom_severity: Severity level
        symptom_frequency: How often it occurs
        symptom_trend: Trend direction
        on_close: Event handler to close modal
        on_log_symptom: Optional handler to log symptom occurrence

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    _modal_header("Symptom Details", "thermometer", "symptom"),
                    # Main info
                    rx.el.div(
                        rx.el.p(
                            symptom_name,
                            class_name="text-xl font-bold text-white mb-3",
                        ),
                        rx.el.div(
                            # Severity badge
                            rx.el.div(
                                rx.el.p(
                                    "Severity", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.span(
                                    symptom_severity,
                                    class_name=rx.match(
                                        symptom_severity.to(str).lower(),
                                        (
                                            "severe",
                                            "px-3 py-1 rounded-full text-xs font-bold bg-red-500/10 text-red-300 border border-red-500/20",
                                        ),
                                        (
                                            "moderate",
                                            "px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-300 border border-amber-500/20",
                                        ),
                                        (
                                            "mild",
                                            "px-3 py-1 rounded-full text-xs font-bold bg-teal-500/10 text-teal-300 border border-teal-500/20",
                                        ),
                                        "px-3 py-1 rounded-full text-xs font-bold bg-slate-500/10 text-slate-300 border border-slate-500/20",
                                    ),
                                ),
                            ),
                            # Trend indicator
                            rx.el.div(
                                rx.el.p(
                                    "Trend", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.div(
                                    rx.cond(
                                        symptom_trend.to(str).lower() == "improving",
                                        rx.icon(
                                            "trending-down",
                                            class_name="w-4 h-4 text-teal-400 mr-1",
                                        ),
                                        rx.cond(
                                            symptom_trend.to(str).lower()
                                            == "worsening",
                                            rx.icon(
                                                "trending-up",
                                                class_name="w-4 h-4 text-red-400 mr-1",
                                            ),
                                            rx.icon(
                                                "minus",
                                                class_name="w-4 h-4 text-slate-400 mr-1",
                                            ),
                                        ),
                                    ),
                                    rx.text(symptom_trend),
                                    class_name=rx.match(
                                        symptom_trend.to(str).lower(),
                                        (
                                            "improving",
                                            "flex items-center text-teal-400",
                                        ),
                                        ("worsening", "flex items-center text-red-400"),
                                        "flex items-center text-slate-400",
                                    ),
                                ),
                            ),
                            class_name="flex gap-6",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Frequency
                    rx.el.div(
                        rx.el.div(
                            rx.icon("clock", class_name="w-4 h-4 text-slate-400 mr-2"),
                            rx.el.span("Frequency: ", class_name="text-slate-400"),
                            rx.text(symptom_frequency),
                            class_name="flex items-center text-white",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        (
                            rx.el.button(
                                rx.icon("plus", class_name="w-4 h-4 mr-2"),
                                "Log Symptom",
                                on_click=on_log_symptom,
                                class_name=f"{GlassStyles.BUTTON_PRIMARY} flex items-center",
                            )
                            if on_log_symptom
                            else rx.fragment()
                        ),
                        class_name="flex justify-between",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def symptom_log_detail_modal(
    show_modal: rx.Var[bool],
    log_symptom_name: rx.Var[str],
    log_severity: rx.Var[int],
    log_notes: rx.Var[str],
    log_timestamp: rx.Var[str],
    on_close: rx.EventHandler,
) -> rx.Component:
    """Symptom log entry detail modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        log_symptom_name: Symptom name
        log_severity: Severity rating 0-10
        log_notes: Additional notes
        log_timestamp: When logged
        on_close: Event handler to close modal

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    _modal_header("Symptom Log", "file-text", "symptom"),
                    # Main info
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                log_symptom_name,
                                class_name="text-xl font-bold text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Severity", class_name="text-xs text-slate-400 mb-1"
                            ),
                            rx.el.div(
                                rx.el.span(
                                    log_severity,
                                    class_name="text-2xl font-bold text-white",
                                ),
                                rx.el.span("/10", class_name="text-slate-400 ml-1"),
                                class_name="flex items-baseline",
                            ),
                        ),
                        class_name=f"flex justify-between items-center {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Timestamp
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "calendar", class_name="w-4 h-4 text-slate-400 mr-2"
                            ),
                            rx.el.span("Logged: ", class_name="text-slate-400"),
                            rx.text(log_timestamp),
                            class_name="flex items-center text-white",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Notes (conditional)
                    rx.cond(
                        log_notes != "",
                        rx.el.div(
                            rx.el.p(
                                "Notes",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                            ),
                            rx.el.p(
                                log_notes,
                                class_name="text-sm text-slate-300 leading-relaxed",
                            ),
                            class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    # Close button
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
    )
