"""Common reusable modal components.

This module provides generic, state-agnostic modal components that can be used
across different pages by passing state vars and handlers.
"""

import reflex as rx

from ...styles.constants import GlassStyles


def edit_modal(
    show_modal: rx.Var[bool],
    content_value: rx.Var[str],
    on_content_change: rx.EventHandler,
    on_save: rx.EventHandler,
    on_close: rx.EventHandler,
    title: str = "Edit",
    placeholder: str = "Edit content...",
    input_height: str = "h-32",
) -> rx.Component:
    """Reusable edit modal for text content.

    Args:
        show_modal: Boolean var controlling modal visibility
        content_value: Current content value var
        on_content_change: Handler for content changes
        on_save: Handler for save action
        on_close: Handler for closing modal (also handles open_change)
        title: Modal title (default: "Edit")
        placeholder: Textarea placeholder text
        input_height: Height class for textarea (default: "h-32")

    Returns:
        Dialog modal component
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(title, class_name="text-lg font-bold text-white"),
            rx.el.div(
                rx.el.textarea(
                    value=content_value,
                    on_change=on_content_change,
                    placeholder=placeholder,
                    class_name=f"{GlassStyles.INPUT} w-full {input_height} resize-none",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button("Cancel", class_name=GlassStyles.BUTTON_SECONDARY),
                ),
                rx.el.button(
                    "Save",
                    on_click=on_save,
                    class_name=GlassStyles.BUTTON_PRIMARY,
                ),
                class_name="flex justify-end gap-3",
            ),
            class_name=f"{GlassStyles.MODAL} p-6 max-w-md",
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def delete_confirm_modal(
    show_modal: rx.Var[bool],
    on_confirm: rx.EventHandler,
    on_close: rx.EventHandler,
    title: str = "Confirm Delete",
    description: str = "This action cannot be undone. The item will be permanently deleted.",
    confirm_text: str = "Delete",
) -> rx.Component:
    """Reusable delete confirmation modal.

    Args:
        show_modal: Boolean var controlling modal visibility
        on_confirm: Handler for confirm delete action
        on_close: Handler for closing modal (also handles open_change)
        title: Modal title (default: "Confirm Delete")
        description: Confirmation message
        confirm_text: Text for confirm button (default: "Delete")

    Returns:
        AlertDialog modal component
    """
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title(title, class_name="text-lg font-bold text-white"),
            rx.alert_dialog.description(
                description,
                class_name="text-slate-400 text-sm my-4",
            ),
            rx.el.div(
                rx.alert_dialog.cancel(
                    rx.el.button("Cancel", class_name=GlassStyles.BUTTON_SECONDARY),
                ),
                rx.alert_dialog.action(
                    rx.el.button(
                        confirm_text,
                        on_click=on_confirm,
                        class_name="px-4 py-2 rounded-xl text-sm font-medium bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 transition-all",
                    ),
                ),
                class_name="flex justify-end gap-3",
            ),
            class_name=f"{GlassStyles.MODAL} p-6 max-w-sm",
        ),
        open=show_modal,
        on_open_change=on_close,
    )


def confirmation_modal(
    show_modal: rx.Var[bool],
    on_confirm: rx.EventHandler,
    on_close: rx.EventHandler,
    title: str = "Confirm Action",
    description: str = "Are you sure you want to proceed?",
    confirm_text: str = "Confirm",
    confirm_color: str = "teal",
) -> rx.Component:
    """Reusable confirmation modal with customizable styling.

    Args:
        show_modal: Boolean var controlling modal visibility
        on_confirm: Handler for confirm action
        on_close: Handler for closing modal
        title: Modal title
        description: Confirmation message
        confirm_text: Text for confirm button
        confirm_color: Color theme for confirm button (teal/red/amber)

    Returns:
        AlertDialog modal component
    """
    color_classes = {
        "teal": "bg-teal-500/20 text-teal-400 border-teal-500/30 hover:bg-teal-500/30",
        "red": "bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-500/30",
        "amber": "bg-amber-500/20 text-amber-400 border-amber-500/30 hover:bg-amber-500/30",
    }
    button_class = color_classes.get(confirm_color, color_classes["teal"])

    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title(title, class_name="text-lg font-bold text-white"),
            rx.alert_dialog.description(
                description,
                class_name="text-slate-400 text-sm my-4",
            ),
            rx.el.div(
                rx.alert_dialog.cancel(
                    rx.el.button("Cancel", class_name=GlassStyles.BUTTON_SECONDARY),
                ),
                rx.alert_dialog.action(
                    rx.el.button(
                        confirm_text,
                        on_click=on_confirm,
                        class_name=f"px-4 py-2 rounded-xl text-sm font-medium border transition-all {button_class}",
                    ),
                ),
                class_name="flex justify-end gap-3",
            ),
            class_name=f"{GlassStyles.MODAL} p-6 max-w-sm",
        ),
        open=show_modal,
        on_open_change=on_close,
    )
