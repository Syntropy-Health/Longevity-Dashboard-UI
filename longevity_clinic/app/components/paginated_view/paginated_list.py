"""Generic paginated list component.

Provides reusable paginated list views with customizable item renderers,
empty states, and optional filter tabs.
"""

from collections.abc import Callable

import reflex as rx

from ..shared.checkin import pagination_controls

# =============================================================================
# Empty State
# =============================================================================


def empty_state_box(
    icon: str = "inbox",
    message: str = "No items found",
    subtitle: str = "",
) -> rx.Component:
    """Render an empty state placeholder.

    Args:
        icon: Lucide icon name
        message: Primary message text
        subtitle: Optional secondary message

    Returns:
        Centered empty state component
    """
    return rx.el.div(
        rx.icon(icon, class_name="w-12 h-12 text-slate-600 mb-4"),
        rx.el.p(message, class_name="text-slate-400"),
        rx.cond(
            subtitle != "",
            rx.el.p(subtitle, class_name="text-slate-500 text-sm mt-1"),
            rx.fragment(),
        ),
        class_name="flex flex-col items-center justify-center py-12",
    )


# =============================================================================
# Paginated List Component
# =============================================================================


def paginated_list(
    items: rx.Var,
    item_renderer: Callable[[dict], rx.Component],
    has_previous: rx.Var[bool],
    has_next: rx.Var[bool],
    page_info: rx.Var[str],
    showing_info: rx.Var[str],
    on_previous: rx.EventHandler,
    on_next: rx.EventHandler,
    empty_icon: str = "inbox",
    empty_message: str = "No items found",
    empty_subtitle: str = "",
    list_class: str = "space-y-4",
) -> rx.Component:
    """Generic paginated list with customizable item renderer.

    Args:
        items: List of items to display (paginated slice)
        item_renderer: Function that renders each item as a component
        has_previous: Whether previous page exists
        has_next: Whether next page exists
        page_info: Page info string (e.g., 'Page 1 of 5')
        showing_info: Showing info string (e.g., 'Showing 1-10 of 25')
        on_previous: Event handler for previous page
        on_next: Event handler for next page
        empty_icon: Icon for empty state
        empty_message: Message for empty state
        empty_subtitle: Subtitle for empty state
        list_class: CSS class for the list container

    Returns:
        Paginated list component with pagination controls
    """
    return rx.match(
        items.length() > 0,
        (
            True,
            rx.el.div(
                rx.el.div(
                    rx.foreach(items, item_renderer),
                    class_name=list_class,
                ),
                pagination_controls(
                    has_previous=has_previous,
                    has_next=has_next,
                    page_info=page_info,
                    showing_info=showing_info,
                    on_previous=on_previous,
                    on_next=on_next,
                ),
            ),
        ),
        empty_state_box(
            icon=empty_icon,
            message=empty_message,
            subtitle=empty_subtitle,
        ),
    )


# =============================================================================
# Paginated List with Filter Tabs
# =============================================================================


def filter_tab_button(
    label: str,
    value: str,
    count: rx.Var,
    color: str,
    active_value: rx.Var[str],
    on_click: rx.EventHandler,
) -> rx.Component:
    """Single filter tab button.

    Args:
        label: Button label text
        value: Filter value
        count: Count to display in badge
        color: Color name (amber/teal/red/white)
        active_value: Currently active filter value
        on_click: Handler when clicked

    Returns:
        Tab button component
    """
    return rx.el.button(
        rx.el.span(label, class_name="mr-2"),
        rx.el.span(
            count,
            class_name=f"px-2 py-0.5 rounded-full text-xs bg-{color}-500/20 text-{color}-400",
        ),
        on_click=lambda: on_click(value),  # type: ignore[arg-type]
        class_name=rx.cond(
            active_value == value,
            "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
            "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
        ),
    )


def paginated_list_with_filters(
    items: rx.Var,
    item_renderer: Callable[[dict], rx.Component],
    filter_tabs: list[tuple[str, str, rx.Var, str]],
    active_filter: rx.Var[str],
    on_filter_change: rx.EventHandler,
    has_previous: rx.Var[bool],
    has_next: rx.Var[bool],
    page_info: rx.Var[str],
    showing_info: rx.Var[str],
    on_previous: rx.EventHandler,
    on_next: rx.EventHandler,
    empty_icon: str = "inbox",
    empty_message: str = "No items found",
    empty_subtitle: str = "",
    list_class: str = "space-y-4",
    filter_class: str = "flex gap-2 mb-6",
) -> rx.Component:
    """Paginated list with filter tabs.

    Args:
        items: List of items to display (paginated slice)
        item_renderer: Function that renders each item as a component
        filter_tabs: List of (label, value, count, color) tuples for filter tabs
        active_filter: Currently active filter value
        on_filter_change: Handler when filter changes
        has_previous: Whether previous page exists
        has_next: Whether next page exists
        page_info: Page info string
        showing_info: Showing info string
        on_previous: Event handler for previous page
        on_next: Event handler for next page
        empty_icon: Icon for empty state
        empty_message: Message for empty state
        empty_subtitle: Subtitle for empty state
        list_class: CSS class for the list container
        filter_class: CSS class for the filter tabs container

    Returns:
        Paginated list with filter tabs
    """
    return rx.el.div(
        # Filter tabs
        rx.el.div(
            *[
                filter_tab_button(
                    label=label,
                    value=value,
                    count=count,
                    color=color,
                    active_value=active_filter,
                    on_click=on_filter_change,
                )
                for label, value, count, color in filter_tabs
            ],
            class_name=filter_class,
        ),
        # Paginated list
        paginated_list(
            items=items,
            item_renderer=item_renderer,
            has_previous=has_previous,
            has_next=has_next,
            page_info=page_info,
            showing_info=showing_info,
            on_previous=on_previous,
            on_next=on_next,
            empty_icon=empty_icon,
            empty_message=empty_message,
            empty_subtitle=empty_subtitle,
            list_class=list_class,
        ),
    )
