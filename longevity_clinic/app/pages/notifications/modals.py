"""Notifications page modals.

This module contains modal dialogs for the notifications page:
- Notification detail modal
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ...states.notification_state import NotificationState
from .components import notification_type_badge


def notification_detail_modal() -> rx.Component:
    """Render notification detail modal.
    
    Returns:
        A modal dialog component for viewing notification details
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.box(
                    # Header
                    rx.flex(
                        rx.flex(
                            rx.match(
                                NotificationState.selected_notification.get("type", "info"),
                                ("info", rx.icon("info", class_name="w-6 h-6 text-blue-500")),
                                ("warning", rx.icon("triangle-alert", class_name="w-6 h-6 text-amber-500")),
                                ("success", rx.icon("circle-check", class_name="w-6 h-6 text-emerald-500")),
                                ("error", rx.icon("circle-x", class_name="w-6 h-6 text-rose-500")),
                                ("appointment", rx.icon("calendar", class_name="w-6 h-6 text-teal-500")),
                                ("treatment", rx.icon("activity", class_name="w-6 h-6 text-purple-500")),
                                ("lab", rx.icon("flask-conical", class_name="w-6 h-6 text-cyan-500")),
                                rx.icon("bell", class_name="w-6 h-6 text-gray-500"),
                            ),
                            rx.text(
                                NotificationState.selected_notification.get("title", "Notification"),
                                class_name="text-xl font-bold text-gray-900"
                            ),
                            class_name="flex items-center gap-3"
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name=GlassStyles.CLOSE_BUTTON
                            )
                        ),
                        class_name="flex items-start justify-between mb-4"
                    ),
                    
                    # Content
                    rx.box(
                        rx.text(
                            NotificationState.selected_notification.get("message", ""),
                            class_name="text-gray-700 leading-relaxed"
                        ),
                        class_name="py-4"
                    ),
                    
                    # Metadata
                    rx.flex(
                        notification_type_badge(NotificationState.selected_notification.get("type", "info")),
                        rx.text(
                            NotificationState.selected_notification.get("created_at", ""),
                            class_name="text-sm text-gray-500"
                        ),
                        class_name="flex items-center gap-3 py-4 border-t border-teal-100/50"
                    ),
                    
                    # Actions
                    rx.flex(
                        rx.button(
                            rx.icon("trash-2", class_name="w-4 h-4 mr-2"),
                            "Delete",
                            on_click=lambda: NotificationState.delete_notification(
                                NotificationState.selected_notification.get("id", "")
                            ),
                            class_name="px-4 py-2 rounded-xl text-rose-600 hover:bg-rose-100/50 transition-colors"
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_PRIMARY_LIGHT
                            )
                        ),
                        class_name="flex justify-end gap-3"
                    ),
                    class_name=f"{GlassStyles.MODAL_PANEL} {GlassStyles.MODAL_CONTENT_MD}"
                )
            )
        ),
        open=NotificationState.selected_notification != {},
        on_open_change=lambda _: NotificationState.clear_selection()
    )
