"""Trend indicator components.

Provides visual trend indicators for improving/stable/worsening states.
"""

import reflex as rx


def trend_badge(
    trend: rx.Var[str] | str,
    show_icon: bool = True,
    size: str = "sm",
) -> rx.Component:
    """Trend badge with icon showing improving/stable/worsening.

    Args:
        trend: Trend value ("improving", "worsening", or "stable")
        show_icon: Whether to show the trend icon
        size: Size variant ("xs", "sm", "md")

    Returns:
        Colored badge with trend icon and label
    """
    # Size variants
    size_classes = {
        "xs": "px-2 py-0.5 text-[10px]",
        "sm": "px-3 py-1 text-xs",
        "md": "px-4 py-1.5 text-sm",
    }
    icon_sizes = {"xs": "w-3 h-3", "sm": "w-4 h-4", "md": "w-5 h-5"}

    size_class = size_classes.get(size, size_classes["sm"])
    icon_size = icon_sizes.get(size, icon_sizes["sm"])

    return rx.match(
        trend,
        (
            "improving",
            rx.el.div(
                rx.cond(
                    show_icon,
                    rx.icon(
                        "trending-down", class_name=f"{icon_size} text-emerald-400 mr-1"
                    ),
                    rx.fragment(),
                ),
                rx.el.span("Improving", class_name="font-medium text-emerald-400"),
                class_name=f"flex items-center {size_class} rounded-full bg-emerald-500/10 border border-emerald-500/20",
            ),
        ),
        (
            "worsening",
            rx.el.div(
                rx.cond(
                    show_icon,
                    rx.icon("trending-up", class_name=f"{icon_size} text-red-400 mr-1"),
                    rx.fragment(),
                ),
                rx.el.span("Worsening", class_name="font-medium text-red-400"),
                class_name=f"flex items-center {size_class} rounded-full bg-red-500/10 border border-red-500/20",
            ),
        ),
        # Default: stable
        rx.el.div(
            rx.cond(
                show_icon,
                rx.icon("minus", class_name=f"{icon_size} text-slate-400 mr-1"),
                rx.fragment(),
            ),
            rx.el.span("Stable", class_name="font-medium text-slate-400"),
            class_name=f"flex items-center {size_class} rounded-full bg-slate-500/10 border border-slate-500/20",
        ),
    )


def trend_text(
    trend: rx.Var[str] | str,
    show_icon: bool = True,
) -> rx.Component:
    """Inline trend indicator (no badge background).

    Args:
        trend: Trend value ("improving", "worsening", or "stable")
        show_icon: Whether to show the trend icon

    Returns:
        Colored text with optional trend icon
    """
    return rx.match(
        trend,
        (
            "improving",
            rx.fragment(
                rx.cond(
                    show_icon,
                    rx.icon(
                        "trending-down", class_name="w-4 h-4 text-emerald-400 mr-1"
                    ),
                    rx.fragment(),
                ),
                rx.el.span("Improving", class_name="text-xs text-emerald-400"),
            ),
        ),
        (
            "worsening",
            rx.fragment(
                rx.cond(
                    show_icon,
                    rx.icon("trending-up", class_name="w-4 h-4 text-red-400 mr-1"),
                    rx.fragment(),
                ),
                rx.el.span("Worsening", class_name="text-xs text-red-400"),
            ),
        ),
        # Default: stable
        rx.fragment(
            rx.cond(
                show_icon,
                rx.icon("minus", class_name="w-4 h-4 text-slate-400 mr-1"),
                rx.fragment(),
            ),
            rx.el.span("Stable", class_name="text-xs text-slate-400"),
        ),
    )
