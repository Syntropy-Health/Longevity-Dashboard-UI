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


def static_metric_card(
    name: str,
    value: str,
    unit: str,
    icon: str,
    trend: str,
    trend_value: str,
) -> rx.Component:
    """Static metric card with trend indicator for dashboard overview.

    Args:
        name: Metric name/label
        value: Display value
        unit: Unit suffix (e.g., "bpm", "mg/dL")
        icon: Lucide icon name
        trend: Trend direction ("up", "down", "stable")
        trend_value: Trend description text (e.g., "+5% this week")

    Returns:
        Styled metric card component
    """
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon,
                class_name="w-5 h-5 text-teal-400",
            ),
            rx.el.span(
                name,
                class_name="text-xs text-slate-400 uppercase tracking-wider font-semibold ml-2",
            ),
            class_name="flex items-center mb-3",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-3xl font-bold text-white",
            ),
            rx.el.span(
                unit,
                class_name="text-sm text-slate-400 ml-1",
            ),
            class_name="flex items-baseline mb-2",
        ),
        rx.el.div(
            rx.icon(
                (
                    "trending-up"
                    if trend == "up"
                    else ("trending-down" if trend == "down" else "minus")
                ),
                class_name=f"w-3 h-3 {'text-teal-400' if trend in ['up', 'down'] else 'text-slate-500'} mr-1",
            ),
            rx.el.span(
                trend_value,
                class_name="text-xs text-slate-400",
            ),
            class_name="flex items-center",
        ),
        class_name=f"{GlassStyles.PANEL} p-5 hover:bg-white/10 transition-all cursor-pointer",
    )


def dashboard_stat_card(
    title: str,
    value: str | rx.Var,
    trend: str | rx.Var,
    trend_up: bool | rx.Var,
    icon: str,
) -> rx.Component:
    """Stats card with trend indicator for admin dashboards.

    Args:
        title: Metric title
        value: Display value (can be reactive)
        trend: Trend text (e.g., "+12%")
        trend_up: Whether trend is positive (affects color)
        icon: Lucide icon name

    Returns:
        Dashboard stat card component
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    title, class_name="text-sm font-medium text-slate-400 truncate"
                ),
                rx.el.p(
                    value,
                    class_name="mt-1 text-3xl font-bold text-white tracking-tight",
                ),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-teal-400"),
                class_name="p-3 bg-teal-500/10 rounded-2xl border border-teal-500/20",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                trend,
                class_name=rx.cond(
                    trend_up,
                    "text-teal-400 text-sm font-medium",
                    "text-red-400 text-sm font-medium",
                ),
            ),
            rx.el.span(" from last month", class_name="text-sm text-slate-500 ml-2"),
            class_name="mt-4",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} p-5",
    )


def efficiency_stat_card(
    title: str,
    value: str | rx.Var,
    subtitle: str,
    icon: str,
    color: str = "teal",
) -> rx.Component:
    """Stat card for clinical efficiency metrics.

    Args:
        title: Metric title
        value: Display value (can be reactive)
        subtitle: Additional context text
        icon: Lucide icon name
        color: Color theme (teal, blue, purple, amber, emerald)

    Returns:
        Efficiency stat card component
    """
    color_classes = {
        "teal": "text-teal-400 bg-teal-500/10 border-teal-500/20",
        "blue": "text-blue-400 bg-blue-500/10 border-blue-500/20",
        "purple": "text-purple-400 bg-purple-500/10 border-purple-500/20",
        "amber": "text-amber-400 bg-amber-500/10 border-amber-500/20",
        "emerald": "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    }

    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon,
                class_name=f"w-5 h-5 {color_classes.get(color, color_classes['teal']).split()[0]}",
            ),
            class_name=f"p-2.5 rounded-xl border {color_classes.get(color, color_classes['teal'])}",
        ),
        rx.el.div(
            rx.el.p(
                value,
                class_name="text-2xl font-bold text-white mt-3",
            ),
            rx.el.p(title, class_name="text-sm font-medium text-slate-300 mt-1"),
            rx.el.p(subtitle, class_name="text-xs text-slate-500 mt-0.5"),
        ),
        class_name=f"{GlassStyles.PANEL} p-4 hover:border-teal-500/30 transition-all",
    )


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    """Card wrapper for charts with title.

    Args:
        title: Chart title
        chart: Chart component to wrap

    Returns:
        Card-wrapped chart component
    """
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-6"),
        rx.el.div(chart, class_name="w-full h-64"),
        class_name=f"{GlassStyles.PANEL} p-6",
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
    subtitle: str = "",
    icon_size: str = "w-12 h-12",
    center_full: bool = False,
) -> rx.Component:
    """Empty state placeholder with optional subtitle.

    Args:
        icon: Lucide icon name
        message: Primary message to display
        subtitle: Optional secondary message
        icon_size: Icon size classes (default "w-12 h-12")
        center_full: If True, centers in both x and y with min-height
    """
    container_class = (
        "flex flex-col items-center justify-center min-h-[200px] h-full"
        if center_full
        else "flex flex-col items-center justify-center py-12"
    )

    return rx.el.div(
        rx.icon(icon, class_name=f"{icon_size} text-slate-500 mb-4"),
        rx.el.p(message, class_name="text-slate-400 text-sm text-center"),
        rx.cond(
            subtitle != "",
            rx.el.p(subtitle, class_name="text-slate-500 text-xs mt-1 text-center"),
            rx.fragment(),
        ),
        class_name=container_class,
    )


def sidebar_item_with_tag(
    text: str,
    icon_name: str,
    href: str = "#",
    tag: str = "",
    tag_color: str = "amber",
    is_active: bool = False,
    is_disabled: bool = False,
) -> rx.Component:
    """A sidebar navigation item with an optional tag badge.

    Args:
        text: Label text for the nav item
        icon_name: Lucide icon name
        href: Navigation URL (default "#" for disabled items)
        tag: Tag text (e.g., "coming soon", "beta", "new")
        tag_color: Color theme for tag ("amber", "teal", "purple", "red")
        is_active: Whether this item is currently active
        is_disabled: Whether this item is disabled/non-clickable

    Returns:
        Sidebar navigation component with optional tag
    """
    tag_colors = {
        "amber": "bg-amber-500/20 text-amber-400 border-amber-500/30",
        "teal": "bg-teal-500/20 text-teal-400 border-teal-500/30",
        "purple": "bg-purple-500/20 text-purple-400 border-purple-500/30",
        "red": "bg-red-500/20 text-red-400 border-red-500/30",
        "blue": "bg-blue-500/20 text-blue-400 border-blue-500/30",
    }
    tag_style = tag_colors.get(tag_color, tag_colors["amber"])

    disabled_class = "opacity-50 cursor-not-allowed" if is_disabled else ""
    active_class = (
        "bg-teal-500/10 text-white border border-teal-500/20"
        if is_active
        else "text-slate-400 hover:text-white hover:bg-white/5 border border-transparent"
    )

    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=f"w-5 h-5 mr-3 transition-colors {('text-teal-400' if is_active else 'text-slate-400 group-hover:text-teal-300')}",
            ),
            rx.el.span(text, class_name="flex-1"),
            rx.cond(
                tag != "",
                rx.el.span(
                    tag,
                    class_name=f"ml-2 px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wider rounded border {tag_style}",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center w-full",
        ),
        href=href if not is_disabled else None,
        class_name=f"flex items-center px-4 py-3 mb-1 rounded-xl text-sm font-medium transition-all duration-200 group {active_class} {disabled_class}",
    )
