"""Shared UI components for the Longevity Clinic application.

This module contains reusable components used across both patient and admin views.
"""

import reflex as rx
from ...styles.constants import GlassStyles


def search_input(
    value: rx.Var,
    on_change: rx.EventHandler,
    placeholder: str = "Search...",
    class_name: str = "",
) -> rx.Component:
    """Reusable search input with icon.
    
    Args:
        value: Reactive value for the input
        on_change: Event handler for input changes
        placeholder: Placeholder text for the input
        class_name: Additional CSS classes
    """
    return rx.el.div(
        rx.el.div(
            rx.icon("search", class_name="w-4 h-4 text-slate-400"),
            class_name="absolute left-3 top-1/2 -translate-y-1/2",
        ),
        rx.el.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            class_name=f"w-full pl-10 pr-4 py-2.5 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/30 {class_name}",
        ),
        class_name="relative",
    )


def patient_select_item(
    patient: dict,
    on_click: rx.EventHandler,
) -> rx.Component:
    """Patient selection item for dropdowns.
    
    Args:
        patient: Patient dict with full_name and email
        on_click: Click handler
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    patient["full_name"][0],
                    class_name="text-xs font-bold text-teal-300",
                ),
                class_name="w-8 h-8 rounded-full bg-teal-500/20 flex items-center justify-center mr-3 border border-teal-500/30",
            ),
            rx.el.div(
                rx.el.p(
                    patient["full_name"],
                    class_name="text-sm font-medium text-white",
                ),
                rx.el.p(
                    patient["email"],
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center",
        ),
        on_click=on_click,
        class_name="p-3 hover:bg-slate-700/50 cursor-pointer transition-colors border-b border-slate-700/30 last:border-0",
    )


def stat_metric_card(
    title: str,
    value: rx.Var | str,
    suffix: str = "",
    icon: str = "activity",
    icon_color: str = "teal",
) -> rx.Component:
    """Compact metric card for displaying a single stat.
    
    Args:
        title: Metric title/label
        value: Metric value (can be reactive)
        suffix: Optional suffix (e.g., "g", "%", "kcal")
        icon: Lucide icon name
        icon_color: Color theme (teal, orange, red, amber, blue, purple)
    """
    color_map = {
        "teal": "text-teal-400 bg-teal-500/10 border-teal-500/20",
        "orange": "text-orange-400 bg-orange-500/10 border-orange-500/20",
        "red": "text-red-400 bg-red-500/10 border-red-500/20",
        "amber": "text-amber-400 bg-amber-500/10 border-amber-500/20",
        "blue": "text-blue-400 bg-blue-500/10 border-blue-500/20",
        "purple": "text-purple-400 bg-purple-500/10 border-purple-500/20",
        "rose": "text-rose-400 bg-rose-500/10 border-rose-500/20",
    }
    colors = color_map.get(icon_color, color_map["teal"])
    icon_text_color = colors.split()[0]
    
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 {icon_text_color}"),
            class_name=f"w-10 h-10 rounded-xl {colors} flex items-center justify-center mb-2 border",
        ),
        rx.el.p(
            title,
            class_name="text-xs text-slate-400 uppercase tracking-wider",
        ),
        rx.el.p(
            rx.text(value, suffix),
            class_name="text-2xl font-bold text-white",
        ),
        class_name=f"{GlassStyles.PANEL} p-4",
    )


def loading_spinner(message: str = "Loading...") -> rx.Component:
    """Loading spinner with optional message.
    
    Args:
        message: Loading message to display
    """
    return rx.el.div(
        rx.icon("loader-circle", class_name="w-8 h-8 text-teal-400 animate-spin"),
        rx.el.p(message, class_name="text-slate-400 mt-2"),
        class_name="flex flex-col items-center justify-center py-12",
    )


def empty_state(
    icon: str = "inbox",
    message: str = "No data found",
) -> rx.Component:
    """Empty state placeholder.
    
    Args:
        icon: Lucide icon name
        message: Message to display
    """
    return rx.el.div(
        rx.icon(icon, class_name="w-16 h-16 text-slate-600 mb-4"),
        rx.el.p(message, class_name="text-slate-500 text-center"),
        class_name="flex flex-col items-center justify-center py-12",
    )
