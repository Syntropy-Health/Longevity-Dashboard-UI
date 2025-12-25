"""Patient treatment search components."""

import reflex as rx

from ....components.collapsible import collapsible_grid, collapsible_section
from ....components.shared.treatment import (
    category_badge,
    protocol_filters,
    treatment_card as shared_treatment_card,
)
from ....states import TreatmentProtocol, TreatmentSearchState

# Icon mapping for treatment categories (using teal-compatible palette)
CATEGORY_ICONS = {
    "IV Therapy": ("syringe", "text-teal-500"),
    "Cryotherapy": ("snowflake", "text-cyan-500"),
    "Supplements": ("pill", "text-emerald-500"),
    "Hormone Therapy": ("activity", "text-teal-600"),
    "Physical Therapy": ("dumbbell", "text-amber-600"),
    "Spa Services": ("sparkles", "text-rose-500"),
    "Oxygen Therapy": ("wind", "text-sky-500"),
    "Peptide Therapy": ("flask-conical", "text-violet-500"),
    "Light Therapy": ("sun", "text-amber-500"),
}


def treatment_card(protocol: TreatmentProtocol) -> rx.Component:
    """Treatment protocol card for patient browsing.

    Uses the shared treatment_card with single "View Details" button.
    """
    return shared_treatment_card(
        protocol=protocol,
        on_primary_click=lambda: TreatmentSearchState.open_details(protocol),
        primary_label="View Details",
        show_frequency=False,
        compact=False,
    )


def treatment_category_section(category_data: dict) -> rx.Component:
    """Collapsible section for a treatment category.

    Args:
        category_data: Dict with 'category', 'treatments', 'count' keys

    Returns:
        Collapsible section with treatment cards grid
    """
    category = category_data["category"]
    icon, icon_color = CATEGORY_ICONS.get(category, ("sparkles", "text-teal-400"))

    return collapsible_section(
        title=category,
        value=category,
        icon=icon,
        icon_color=icon_color,
        badge_count=category_data["count"],
        content=collapsible_grid(
            items=category_data["treatments"],
            render_item=treatment_card,
            columns="grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
        ),
    )


# Re-export for convenience
__all__ = [
    "category_badge",
    "protocol_filters",
    "treatment_card",
    "treatment_category_section",
]
