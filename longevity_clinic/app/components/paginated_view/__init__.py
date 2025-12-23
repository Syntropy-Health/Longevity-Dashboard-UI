"""Paginated view components for displaying lists with pagination.

This module provides reusable paginated view components:
- paginated_list: Generic paginated list with customizable item renderer
- paginated_checkins_view: Pre-configured paginated view for check-ins

Usage:
    from longevity_clinic.app.components.paginated_view import paginated_list

    paginated_list(
        items=MyState.paginated_items,
        item_renderer=my_card_component,
        empty_icon="inbox",
        empty_message="No items found",
        has_previous=MyState.has_previous_page,
        has_next=MyState.has_next_page,
        page_info=MyState.page_info,
        showing_info=MyState.showing_info,
        on_previous=MyState.previous_page,
        on_next=MyState.next_page,
    )
"""

from .paginated_list import (
    empty_state_box,
    paginated_list,
    paginated_list_with_filters,
)

__all__ = [
    "empty_state_box",
    "paginated_list",
    "paginated_list_with_filters",
]
