"""Shared treatment card components for the Longevity Clinic application.

This module contains reusable treatment card components used across both
patient treatment search and admin treatment management views.
"""

from collections.abc import Callable

import reflex as rx

from ...config import current_config
from ...styles.constants import GlassStyles

# =============================================================================
# Category Badge - Reusable treatment category badge
# =============================================================================

# Category color mapping for consistent styling
CATEGORY_COLORS = {
    "IV Therapy": ("bg-sky-100/80", "text-sky-700", "border-sky-200/60"),
    "Cryotherapy": ("bg-cyan-100/80", "text-cyan-700", "border-cyan-200/60"),
    "Supplements": ("bg-emerald-100/80", "text-emerald-700", "border-emerald-200/60"),
    "Hormone Therapy": ("bg-purple-100/80", "text-purple-700", "border-purple-200/60"),
    "Physical Therapy": ("bg-orange-100/80", "text-orange-700", "border-orange-200/60"),
    "Spa Services": ("bg-pink-100/80", "text-pink-700", "border-pink-200/60"),
    "Oxygen Therapy": ("bg-blue-100/80", "text-blue-700", "border-blue-200/60"),
    "Peptide Therapy": ("bg-violet-100/80", "text-violet-700", "border-violet-200/60"),
    "Light Therapy": ("bg-amber-100/80", "text-amber-700", "border-amber-200/60"),
}

DEFAULT_CATEGORY_COLORS = ("bg-gray-100/80", "text-gray-700", "border-gray-200/60")


def category_badge(category: str, size: str = "sm") -> rx.Component:
    """Category badge with styled colors.

    Args:
        category: Treatment category name
        size: Badge size - "xs", "sm", or "md"

    Returns:
        A styled badge component
    """
    colors = CATEGORY_COLORS.get(category, DEFAULT_CATEGORY_COLORS)
    bg, text, border = colors

    size_classes = {
        "xs": "px-2 py-0.5 text-[10px]",
        "sm": "px-2.5 py-1 text-xs",
        "md": "px-3 py-1.5 text-sm",
    }

    return rx.el.span(
        category,
        class_name=f"{bg} {text} border {border} {size_classes.get(size, size_classes['sm'])} "
        "rounded-full font-semibold uppercase tracking-wider backdrop-blur-sm",
    )


# =============================================================================
# Treatment Meta Item - Shows icon + value (duration, frequency, cost)
# =============================================================================


def treatment_meta_item(
    icon: str,
    value: rx.Var | str,
    with_background: bool = False,
) -> rx.Component:
    """Single treatment metadata item with icon.

    Args:
        icon: Lucide icon name
        value: The value to display
        with_background: Whether to show a background container

    Returns:
        A metadata display component
    """
    content = rx.el.div(
        rx.icon(icon, class_name=GlassStyles.TREATMENT_META_ICON),
        rx.el.span(value, class_name=GlassStyles.TREATMENT_META_TEXT),
        class_name=GlassStyles.TREATMENT_META_ITEM,
    )

    if with_background:
        return rx.el.div(
            content,
            class_name="bg-white/50 px-3 py-1.5 rounded-lg border border-white/60 shadow-sm backdrop-blur-sm",
        )

    return content


# =============================================================================
# Treatment Card - Unified card for patient and admin views
# =============================================================================


def treatment_card(
    protocol: dict,
    on_primary_click: Callable | None = None,
    on_secondary_click: Callable | None = None,
    primary_label: str = "View Details",
    secondary_label: str | None = None,
    show_frequency: bool = False,
    compact: bool = False,
) -> rx.Component:
    """Unified treatment card component for both patient and admin views.

    Args:
        protocol: Treatment protocol dict with name, category, description, duration, cost, frequency
        on_primary_click: Handler for primary button click
        on_secondary_click: Handler for secondary button click (admin only)
        primary_label: Label for primary button
        secondary_label: Label for secondary button (if None, single button layout)
        show_frequency: Whether to show frequency in meta row
        compact: Whether to use compact spacing

    Returns:
        A styled treatment card component

    Note:
        Uses GlassStyles.TREATMENT_CARD_CONTENT with adequate bottom padding (pb-7)
        to prevent letter descender cutoff (g, p, y, q).
    """
    # Build meta items
    meta_items = [
        treatment_meta_item("clock", protocol["duration"]),
    ]
    if show_frequency:
        meta_items.append(treatment_meta_item("repeat", protocol["frequency"]))
    meta_items.append(treatment_meta_item("dollar-sign", f"${protocol['cost']}"))

    # Card content - uses adequate padding to prevent descender cutoff
    card_content = rx.el.div(
        # Header with title and badge
        rx.el.div(
            rx.el.h3(
                protocol["name"],
                class_name=GlassStyles.TREATMENT_CARD_TITLE,
            ),
            category_badge(protocol["category"], size="xs"),
            class_name="flex justify-between items-start gap-3 mb-3",
        ),
        # Description with adequate line height and bottom margin
        rx.el.p(
            protocol["description"],
            class_name=GlassStyles.TREATMENT_CARD_DESCRIPTION,
        ),
        # Meta row
        rx.el.div(
            *meta_items,
            class_name="flex items-center justify-between gap-3 pt-4 border-t border-gray-100/60",
        ),
        class_name=(
            GlassStyles.TREATMENT_CARD_CONTENT
            if not compact
            else "p-5 pb-6 flex-1 flex flex-col"
        ),
    )

    # Footer buttons
    if secondary_label and on_secondary_click:
        # Two-button layout (admin)
        footer = rx.el.div(
            rx.el.button(
                secondary_label,
                on_click=on_secondary_click,
                class_name=GlassStyles.TREATMENT_CARD_BUTTON_SECONDARY,
            ),
            rx.el.button(
                primary_label,
                on_click=on_primary_click,
                class_name=GlassStyles.TREATMENT_CARD_BUTTON_PRIMARY,
            ),
            class_name=GlassStyles.TREATMENT_CARD_FOOTER,
        )
    else:
        # Single button layout (patient)
        footer = rx.el.div(
            rx.el.button(
                primary_label,
                on_click=on_primary_click,
                class_name=f"w-full py-3.5 text-sm font-semibold {current_config.glass_button_secondary} "
                "rounded-xl transition-all duration-300",
            ),
            class_name="px-6 pb-6",
        )

    return rx.el.div(
        card_content,
        footer,
        class_name=GlassStyles.TREATMENT_CARD,
    )


# =============================================================================
# Protocol Filters - Search and category filter controls
# =============================================================================


def protocol_filters(
    search_placeholder: str = "Search treatments...",
    on_search_change: rx.EventHandler = None,
    on_category_change: rx.EventHandler = None,
    categories: list[str] = None,
) -> rx.Component:
    """Protocol filter controls with search and category dropdown.

    Args:
        search_placeholder: Placeholder for search input
        on_search_change: Handler for search input changes
        on_category_change: Handler for category filter changes
        categories: List of category options

    Returns:
        A filter controls component
    """
    if categories is None:
        categories = list(CATEGORY_COLORS.keys())

    return rx.el.div(
        # Search input
        rx.el.div(
            rx.icon(
                "search",
                class_name="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder=search_placeholder,
                on_change=on_search_change,
                class_name=f"pl-12 w-full py-3 {current_config.glass_input_style} text-sm font-medium",
            ),
            class_name="relative flex-1 max-w-md",
        ),
        # Category dropdown
        rx.el.select(
            rx.el.option("All Categories", value="All"),
            *[rx.el.option(cat, value=cat) for cat in categories],
            on_change=on_category_change,
            class_name=f"py-3 px-6 {current_config.glass_input_style} cursor-pointer text-sm font-medium text-gray-700",
        ),
        class_name="flex gap-4 mb-8 flex-wrap items-center",
    )


__all__ = [
    "CATEGORY_COLORS",
    "category_badge",
    "protocol_filters",
    "treatment_card",
    "treatment_meta_item",
]
