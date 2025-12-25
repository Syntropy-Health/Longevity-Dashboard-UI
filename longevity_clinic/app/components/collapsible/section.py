"""Generic collapsible section component.

Provides a reusable accordion wrapper that can make any content collapsible.
Uses glassmorphism styling consistent with the app theme.
"""

from collections.abc import Callable

import reflex as rx

from ...styles.constants import GlassStyles


def collapsible_section(
    title: str | rx.Var,
    content: rx.Component,
    value: str | rx.Var | None = None,
    icon: str = "layers",
    icon_color: str | None = None,
    badge_count: int | rx.Var | None = None,
) -> rx.Component:
    """Create a collapsible accordion section with glassmorphism styling.

    Args:
        title: Section title text
        content: The content component to show when expanded
        value: Unique value for accordion state (defaults to title)
        icon: Lucide icon name for the section header (default: layers)
        icon_color: Tailwind text color class for the icon (default: emerald-400)
        badge_count: Optional count to show in badge (e.g., item count)

    Returns:
        Accordion item component
    """
    section_value = value if value is not None else title
    # Use provided icon_color or default from GlassStyles
    icon_class = f"w-5 h-5 {icon_color} mr-3" if icon_color else GlassStyles.COLLAPSIBLE_ICON

    # Build badge if count provided - emerald styling to match theme
    badge = (
        rx.el.span(
            badge_count,
            class_name=GlassStyles.COLLAPSIBLE_BADGE,
        )
        if badge_count is not None
        else rx.fragment()
    )

    return rx.accordion.item(
        rx.accordion.header(
            rx.accordion.trigger(
                rx.el.div(
                    # Icon and title
                    rx.el.div(
                        rx.icon(icon, class_name=icon_class),
                        rx.el.span(
                            title,
                            class_name=GlassStyles.COLLAPSIBLE_TITLE,
                        ),
                        class_name="flex items-center",
                    ),
                    # Badge + chevron
                    rx.el.div(
                        badge,
                        rx.icon(
                            "chevron-down",
                            class_name=GlassStyles.COLLAPSIBLE_CHEVRON,
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center justify-between w-full",
                ),
                class_name=GlassStyles.COLLAPSIBLE_TRIGGER,
            ),
        ),
        rx.accordion.content(
            rx.el.div(content, class_name=GlassStyles.COLLAPSIBLE_CONTENT_INNER),
            class_name=GlassStyles.COLLAPSIBLE_CONTENT,
        ),
        value=section_value,
        class_name=GlassStyles.COLLAPSIBLE_ITEM,
    )


def collapsible_container(
    children: list[rx.Component],
    default_expanded: list[str] | rx.Var | None = None,
    allow_multiple: bool = True,
) -> rx.Component:
    """Container for multiple collapsible sections.

    Args:
        children: List of collapsible_section components
        default_expanded: List of section values to expand by default, or a
                         Reflex Var containing the list (e.g., State.all_names)
        allow_multiple: If True, multiple sections can be open; if False, only one

    Returns:
        Accordion root component
    """
    return rx.accordion.root(
        *children,
        type="multiple" if allow_multiple else "single",
        default_value=default_expanded if default_expanded is not None else [],
        class_name=GlassStyles.COLLAPSIBLE_CONTAINER,
    )


def collapsible_grid(
    items: rx.Var | list,
    render_item: Callable,
    columns: str = "grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
    gap: str = "gap-6",
) -> rx.Component:
    """Grid layout for items inside a collapsible section.

    Args:
        items: List of items or Reflex Var
        render_item: Function to render each item
        columns: Tailwind grid column classes
        gap: Tailwind gap class

    Returns:
        Grid component with items
    """
    return rx.el.div(
        rx.foreach(items, render_item),
        class_name=f"grid {columns} {gap}",
    )
