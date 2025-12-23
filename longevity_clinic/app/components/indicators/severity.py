"""Severity indicator components.

Provides visual severity indicators on a 0-10 scale with 3-tier color coding:
- Green (0-3): Low severity - Good
- Amber (4-6): Moderate severity - Caution
- Red (7-10): High severity - Concern
"""

import reflex as rx


def _get_severity_color(severity: rx.Var[int] | int) -> rx.Var[str]:
    """Get color class based on severity tier (0-3: green, 4-6: amber, 7-10: red)."""
    return rx.cond(
        severity <= 3,
        "emerald",
        rx.cond(severity <= 6, "amber", "red"),
    )


def severity_bar(
    severity: rx.Var[int] | int,
    max_value: int = 10,
    show_label: bool = True,
    size: str = "sm",
) -> rx.Component:
    """Progress bar severity indicator with 3-tier color coding.

    Args:
        severity: Severity value (0-10)
        max_value: Maximum value (default 10)
        show_label: Whether to show the severity number
        size: Size variant ("xs", "sm", "md")

    Returns:
        Colored progress bar with optional label
    """
    # Size to height mapping
    height_map = {"xs": "1", "sm": "2", "md": "3"}
    height = height_map.get(size, "2")

    # 3-tier color scheme
    color_scheme = _get_severity_color(severity)

    return rx.el.div(
        # Label
        rx.cond(
            show_label,
            rx.el.div(
                rx.el.span(
                    severity,
                    class_name=rx.cond(
                        severity <= 3,
                        "text-emerald-500 font-semibold text-xs",
                        rx.cond(
                            severity <= 6,
                            "text-amber-500 font-semibold text-xs",
                            "text-red-500 font-semibold text-xs",
                        ),
                    ),
                ),
                rx.el.span(f"/{max_value}", class_name="text-xs text-slate-400 ml-0.5"),
                class_name="flex items-baseline mb-1",
            ),
        ),
        # Progress bar
        rx.progress(
            value=(severity / max_value) * 100,
            height=height,
            color_scheme=color_scheme,
            class_name="w-full",
        ),
        class_name="w-full min-w-[60px]",
    )


def severity_badge(
    severity: rx.Var[int] | int,
    max_value: int = 10,
    compact: bool = False,
) -> rx.Component:
    """Compact badge-style severity indicator with 3-tier colors.

    Args:
        severity: Severity value (0-10)
        max_value: Maximum value (default 10)
        compact: If True, shows only the number without "/10"

    Returns:
        Colored badge with severity value
    """
    return rx.el.span(
        severity,
        rx.cond(compact, "", f"/{max_value}"),
        class_name=rx.cond(
            severity <= 3,
            "px-2 py-0.5 rounded text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200",
            rx.cond(
                severity <= 6,
                "px-2 py-0.5 rounded text-xs font-semibold bg-amber-100 text-amber-700 border border-amber-200",
                "px-2 py-0.5 rounded text-xs font-semibold bg-red-100 text-red-700 border border-red-200",
            ),
        ),
    )


def severity_comparison(
    current: rx.Var[int] | int,
    previous: rx.Var[int] | int,
    max_value: int = 10,
) -> rx.Component:
    """Side-by-side severity comparison.

    Args:
        current: Current severity value
        previous: Previous severity value
        max_value: Maximum severity value (default 10)

    Returns:
        Component showing current vs previous with trend indicator
    """
    return rx.el.div(
        # Current value
        rx.el.div(
            rx.el.span("Now: ", class_name="text-xs text-slate-500"),
            severity_badge(current, max_value, compact=True),
            class_name="flex items-center gap-1",
        ),
        # Trend arrow
        rx.cond(
            current < previous,
            rx.icon("trending-down", class_name="w-4 h-4 text-emerald-500"),
            rx.cond(
                current > previous,
                rx.icon("trending-up", class_name="w-4 h-4 text-red-500"),
                rx.icon("minus", class_name="w-4 h-4 text-slate-400"),
            ),
        ),
        # Previous value
        rx.el.div(
            rx.el.span("Was: ", class_name="text-xs text-slate-400"),
            rx.el.span(
                previous,
                f"/{max_value}",
                class_name="text-xs text-slate-400",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center gap-2",
    )
