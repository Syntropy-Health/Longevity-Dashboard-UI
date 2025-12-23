import reflex as rx

from ..styles import GlassStyles


def page_header(
    title: str,
    button_text: str,
    button_icon: str,
    button_onclick: rx.EventHandler,
) -> rx.Component:
    """
    Standardized page header with title and action button.
    Ensures proper positioning and visibility across all pages.
    """
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                title,
                class_name=f"text-2xl font-bold {GlassStyles.HEADING}",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.button(
            rx.icon(button_icon, class_name="w-4 h-4 mr-2"),
            button_text,
            on_click=button_onclick,
            class_name=f"flex items-center {GlassStyles.BUTTON_PRIMARY} text-sm font-medium whitespace-nowrap ml-4 flex-shrink-0",
        ),
        class_name="flex flex-row items-center justify-between gap-4 mb-8 w-full",
    )


def section_header(
    title: str,
    button_text: str,
    button_icon: str,
    button_onclick: rx.EventHandler,
) -> rx.Component:
    """
    Standardized section header with title and action button.
    For use within page sections (smaller than page_header).
    """
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                title,
                class_name=f"text-xl font-bold {GlassStyles.HEADING}",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.button(
            rx.icon(button_icon, class_name="w-4 h-4 mr-2"),
            button_text,
            on_click=button_onclick,
            class_name=f"flex items-center {GlassStyles.BUTTON_PRIMARY} text-sm font-medium whitespace-nowrap ml-4 flex-shrink-0",
        ),
        class_name="flex flex-row items-center justify-between gap-4 mb-6 w-full",
    )
