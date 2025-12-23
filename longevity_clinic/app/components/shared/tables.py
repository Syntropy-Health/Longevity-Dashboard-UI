"""Reusable table components for data display."""

import reflex as rx

# =============================================================================
# TABLE STYLING CONSTANTS
# =============================================================================

TABLE_HEADER_CELL = (
    "px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider"
)
TABLE_DATA_CELL = "px-6 py-4 whitespace-nowrap"
TABLE_ROW_HOVER = "border-b border-slate-700/30 hover:bg-slate-800/30 transition-colors"


# =============================================================================
# STATUS BADGE COMPONENT
# =============================================================================


def status_badge(status: rx.Var[str] | str) -> rx.Component:
    """Status badge with dynamic coloring.

    Args:
        status: Status string (Active, Inactive, Onboarding, etc.)
    """
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "px-2 py-1 text-xs font-semibold rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30",
            ),
            (
                "Inactive",
                "px-2 py-1 text-xs font-semibold rounded-full bg-slate-700/50 text-slate-400 border border-slate-600/30",
            ),
            (
                "Onboarding",
                "px-2 py-1 text-xs font-semibold rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30",
            ),
            # Default
            "px-2 py-1 text-xs font-semibold rounded-full bg-slate-700/50 text-slate-400 border border-slate-600/30",
        ),
    )


# =============================================================================
# HEALTH SCORE BAR COMPONENT
# =============================================================================


def health_score_bar(score: rx.Var[int] | int) -> rx.Component:
    """Health score progress bar with color coding.

    Args:
        score: Health score (0-100)
    """
    # Calculate percentage and color based on score
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=rx.cond(
                    score >= 70,
                    "h-full rounded-full bg-teal-500",
                    rx.cond(
                        score >= 40,
                        "h-full rounded-full bg-amber-500",
                        "h-full rounded-full bg-red-500",
                    ),
                ),
                style={"width": rx.Var.create(f"{score}%")},
            ),
            class_name="w-20 h-2 bg-slate-700 rounded-full overflow-hidden",
        ),
        rx.el.span(
            score,
            class_name="ml-2 text-xs text-slate-400",
        ),
        class_name="flex items-center",
    )


# =============================================================================
# AVATAR COMPONENT
# =============================================================================


def avatar_circle(
    initial: rx.Var[str] | str,
    size: str = "sm",
    color: str = "teal",
) -> rx.Component:
    """Avatar circle with initial.

    Args:
        initial: Single character to display
        size: "sm" (8x8), "md" (10x10), or "lg" (12x12)
        color: Color theme (teal, blue, purple)
    """
    size_classes = {
        "sm": "w-8 h-8 text-xs",
        "md": "w-10 h-10 text-sm",
        "lg": "w-12 h-12 text-lg",
    }
    color_classes = {
        "teal": "bg-teal-500/20 text-teal-300 border-teal-500/30",
        "blue": "bg-blue-500/20 text-blue-300 border-blue-500/30",
        "purple": "bg-purple-500/20 text-purple-300 border-purple-500/30",
    }

    return rx.el.div(
        rx.el.span(initial, class_name="font-bold"),
        class_name=f"{size_classes.get(size, size_classes['sm'])} {color_classes.get(color, color_classes['teal'])} rounded-full flex items-center justify-center border",
    )


# =============================================================================
# TABLE HEADER COMPONENT
# =============================================================================


def table_header(columns: list[str]) -> rx.Component:
    """Create table header row.

    Args:
        columns: List of column header texts
    """
    return rx.el.thead(
        rx.el.tr(
            *[rx.el.th(col, class_name=TABLE_HEADER_CELL) for col in columns],
        ),
        class_name="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50",
    )


# =============================================================================
# SEARCH INPUT COMPONENT
# =============================================================================


def search_input_box(
    placeholder: str,
    value: rx.Var[str],
    on_change,
) -> rx.Component:
    """Search input with icon.

    Args:
        placeholder: Placeholder text
        value: Current value (state var)
        on_change: Change handler
    """
    return rx.el.div(
        rx.icon(
            "search",
            class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
        ),
        rx.el.input(
            placeholder=placeholder,
            on_change=on_change,
            default_value=value,
            class_name="pl-10 block w-full bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 sm:text-sm py-2.5 focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
        ),
        class_name="relative flex-1 max-w-xs",
    )


# =============================================================================
# FILTER SELECT COMPONENT
# =============================================================================


def filter_select(
    options: list[tuple[str, str]],
    value: rx.Var[str],
    on_change,
) -> rx.Component:
    """Filter dropdown select.

    Args:
        options: List of (label, value) tuples
        value: Current value (state var)
        on_change: Change handler
    """
    return rx.el.select(
        *[rx.el.option(label, value=val) for label, val in options],
        value=value,
        on_change=on_change,
        class_name="block bg-slate-800/50 border border-slate-700/50 rounded-xl text-white py-2.5 pl-3 pr-10 text-sm focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
    )


# =============================================================================
# LOADING STATE
# =============================================================================


def table_loading_skeleton(rows: int = 5, cols: int = 6) -> rx.Component:
    """Loading skeleton for table."""
    return rx.el.div(
        *[
            rx.el.div(
                *[
                    rx.el.div(
                        class_name="h-4 bg-slate-700/50 rounded animate-pulse",
                        style={"width": f"{60 + (i * 10) % 40}%"},
                    )
                    for i in range(cols)
                ],
                class_name="flex gap-6 p-4 border-b border-slate-700/30",
            )
            for _ in range(rows)
        ],
        class_name="space-y-1",
    )


def empty_table_state(message: str = "No data found") -> rx.Component:
    """Empty state for tables."""
    return rx.el.div(
        rx.icon("inbox", class_name="w-12 h-12 text-slate-500 mb-3"),
        rx.el.p(message, class_name="text-slate-400 text-sm"),
        class_name="flex flex-col items-center justify-center py-12",
    )
