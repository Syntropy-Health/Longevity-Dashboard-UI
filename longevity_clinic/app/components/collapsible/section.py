"""Generic collapsible section component.

Provides a reusable accordion wrapper that can make any content collapsible.
Uses glassmorphism styling consistent with the app theme.
"""

from collections.abc import Callable

import reflex as rx


def collapsible_section(
    title: str | rx.Var,
    content: rx.Component,
    value: str | rx.Var | None = None,
    icon: str = "layers",
    icon_color: str = "text-teal-400",
    badge_count: int | rx.Var | None = None,
) -> rx.Component:
    """Create a collapsible accordion section with glassmorphism styling.

    Args:
        title: Section title text
        content: The content component to show when expanded
        value: Unique value for accordion state (defaults to title)
        icon: Lucide icon name for the section header (default: layers)
        icon_color: Tailwind text color class for the icon
        badge_count: Optional count to show in badge (e.g., item count)

    Returns:
        Accordion item component
    """
    section_value = value if value is not None else title

    # Build badge if count provided - subtle teal styling
    badge = (
        rx.el.span(
            badge_count,
            class_name="text-xs font-medium text-teal-300 bg-teal-500/15 "
            "px-2.5 py-0.5 rounded-full mr-3 border border-teal-500/25",
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
                        rx.icon(icon, class_name=f"w-5 h-5 {icon_color} mr-3"),
                        rx.el.span(
                            title,
                            class_name="text-lg font-semibold text-slate-200",
                        ),
                        class_name="flex items-center",
                    ),
                    # Badge + chevron
                    rx.el.div(
                        badge,
                        rx.icon(
                            "chevron-down",
                            class_name="w-5 h-5 text-slate-400 transition-transform duration-300 ease-out "
                            "group-data-[state=open]:rotate-180",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center justify-between w-full",
                ),
                class_name="group flex w-full p-4 hover:bg-teal-500/10 "
                "transition-all duration-300 rounded-xl",
            ),
        ),
        rx.accordion.content(
            rx.el.div(content, class_name="px-4 pb-4 pt-2"),
            class_name="overflow-hidden data-[state=open]:animate-accordion-down "
            "data-[state=closed]:animate-accordion-up",
        ),
        value=section_value,
        class_name=(
            "bg-slate-800/40 backdrop-blur-xl rounded-2xl "
            "border border-slate-700/50 hover:border-teal-500/30 "
            "my-3 overflow-hidden transition-all duration-300 "
            "shadow-lg shadow-slate-900/20"
        ),
    )


def collapsible_container(
    children: list[rx.Component],
    default_expanded: list[str] | None = None,
    allow_multiple: bool = True,
) -> rx.Component:
    """Container for multiple collapsible sections.

    Args:
        children: List of collapsible_section components
        default_expanded: List of section values to expand by default
        allow_multiple: If True, multiple sections can be open; if False, only one

    Returns:
        Accordion root component
    """
    return rx.accordion.root(
        *children,
        type="multiple" if allow_multiple else "single",
        default_value=default_expanded or [],
        class_name="w-full space-y-1",
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
