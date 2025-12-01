"""Notifications page with differential admin/patient views."""

import reflex as rx

from ..components.layout import authenticated_layout
from ..states.notification_state import NotificationState
from ..states.auth_state import AuthState
from ..styles.constants import GlassStyles


def notification_icon(notification_type: str) -> rx.Component:
    """Get icon component for notification type."""
    icon_map = {
        "info": "info",
        "warning": "triangle-alert",
        "success": "circle-check",
        "error": "x-circle",
        "appointment": "calendar",
        "treatment": "activity",
        "lab": "flask-conical"
    }
    color_map = {
        "info": "text-blue-500",
        "warning": "text-amber-500",
        "success": "text-emerald-500",
        "error": "text-rose-500",
        "appointment": "text-teal-500",
        "treatment": "text-purple-500",
        "lab": "text-cyan-500"
    }
    
    return rx.icon(
        icon_map.get(notification_type, "bell"),
        class_name=f"w-5 h-5 {color_map.get(notification_type, 'text-gray-500')}"
    )


def notification_type_badge(notification_type: str) -> rx.Component:
    """Render a type badge for notifications."""
    color_map = {
        "info": "bg-blue-100 text-blue-700",
        "warning": "bg-amber-100 text-amber-700",
        "success": "bg-emerald-100 text-emerald-700",
        "error": "bg-rose-100 text-rose-700",
        "appointment": "bg-teal-100 text-teal-700",
        "treatment": "bg-purple-100 text-purple-700",
        "lab": "bg-cyan-100 text-cyan-700"
    }
    
    return rx.box(
        notification_type.capitalize(),
        class_name=f"px-2 py-0.5 rounded-full text-xs font-medium {color_map.get(notification_type, 'bg-gray-100 text-gray-600')}"
    )


def notification_card(notification: dict) -> rx.Component:
    """Render a single notification card."""
    is_read = notification.get("is_read", False)
    
    return rx.box(
        rx.flex(
            # Icon with background
            rx.box(
                rx.match(
                    notification.get("type", "info"),
                    ("info", rx.icon("info", class_name="w-5 h-5 text-blue-500")),
                    ("warning", rx.icon("triangle-alert", class_name="w-5 h-5 text-amber-500")),
                    ("success", rx.icon("circle-check", class_name="w-5 h-5 text-emerald-500")),
                    ("error", rx.icon("x-circle", class_name="w-5 h-5 text-rose-500")),
                    ("appointment", rx.icon("calendar", class_name="w-5 h-5 text-teal-500")),
                    ("treatment", rx.icon("activity", class_name="w-5 h-5 text-purple-500")),
                    ("lab", rx.icon("flask-conical", class_name="w-5 h-5 text-cyan-500")),
                    rx.icon("bell", class_name="w-5 h-5 text-gray-500"),
                ),
                class_name="p-3 rounded-xl bg-white/50 border border-white/40"
            ),
            # Content
            rx.box(
                rx.flex(
                    rx.text(
                        notification.get("title", "Notification"),
                        class_name=f"font-semibold {'text-gray-900' if not is_read else 'text-gray-600'}"
                    ),
                    rx.cond(
                        ~notification.get("is_read", False),
                        rx.box(
                            class_name="w-2 h-2 rounded-full bg-teal-500"
                        ),
                        rx.fragment()
                    ),
                    class_name="flex items-center gap-2"
                ),
                rx.text(
                    notification.get("message", ""),
                    class_name="text-sm text-gray-600 mt-1 line-clamp-2"
                ),
                rx.flex(
                    notification_type_badge(notification.get("type", "info")),
                    rx.text(
                        notification.get("created_at", "")[:10],
                        class_name="text-xs text-gray-400"
                    ),
                    class_name="flex items-center gap-3 mt-2"
                ),
                class_name="flex-1 min-w-0"
            ),
            # Actions
            rx.flex(
                rx.button(
                    rx.icon("check", class_name="w-4 h-4"),
                    on_click=lambda: NotificationState.mark_as_read(notification.get("id", "")),
                    class_name="p-2 rounded-lg hover:bg-teal-100/50 text-gray-400 hover:text-teal-600 transition-colors",
                    title="Mark as read"
                ),
                rx.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: NotificationState.delete_notification(notification.get("id", "")),
                    class_name="p-2 rounded-lg hover:bg-rose-100/50 text-gray-400 hover:text-rose-600 transition-colors",
                    title="Delete"
                ),
                class_name="flex items-center gap-1"
            ),
            class_name="flex items-start gap-4"
        ),
        on_click=lambda: NotificationState.select_notification(notification),
        class_name=f"""
            p-4 rounded-xl cursor-pointer transition-all duration-200
            {'bg-teal-50/50 border-teal-200/50' if not is_read else 'bg-white/60 border-white/40'}
            border backdrop-blur-sm hover:shadow-md hover:border-teal-300/50
        """
    )


def filter_tabs() -> rx.Component:
    """Render filter tabs for notifications."""
    return rx.flex(
        rx.button(
            "All",
            on_click=lambda: NotificationState.set_filter("all"),
            class_name=f"""
                px-4 py-2 rounded-lg text-sm font-medium transition-all
                {GlassStyles.TAB_TRIGGER_LIGHT}
            """,
            data_state=rx.cond(NotificationState.filter_type == "all", "active", "inactive")
        ),
        rx.button(
            rx.flex(
                "Unread",
                rx.cond(
                    NotificationState.unread_count > 0,
                    rx.box(
                        NotificationState.unread_count,
                        class_name="ml-2 px-2 py-0.5 rounded-full bg-teal-500 text-white text-xs"
                    ),
                    rx.fragment()
                ),
                class_name="flex items-center"
            ),
            on_click=lambda: NotificationState.set_filter("unread"),
            class_name=f"""
                px-4 py-2 rounded-lg text-sm font-medium transition-all
                {GlassStyles.TAB_TRIGGER_LIGHT}
            """,
            data_state=rx.cond(NotificationState.filter_type == "unread", "active", "inactive")
        ),
        rx.button(
            "Read",
            on_click=lambda: NotificationState.set_filter("read"),
            class_name=f"""
                px-4 py-2 rounded-lg text-sm font-medium transition-all
                {GlassStyles.TAB_TRIGGER_LIGHT}
            """,
            data_state=rx.cond(NotificationState.filter_type == "read", "active", "inactive")
        ),
        class_name=GlassStyles.TAB_LIST_LIGHT
    )


def empty_state() -> rx.Component:
    """Render empty state when no notifications."""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon("bell-off", class_name="w-12 h-12 text-gray-300"),
                class_name="p-6 rounded-full bg-gray-100"
            ),
            rx.text(
                "No notifications",
                class_name="text-xl font-semibold text-gray-600 mt-4"
            ),
            rx.text(
                "You're all caught up! Check back later for updates.",
                class_name="text-gray-400 text-center mt-2"
            ),
            class_name="flex flex-col items-center justify-center py-16"
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-8"
    )


def notification_detail_modal() -> rx.Component:
    """Render notification detail modal."""
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
                                ("error", rx.icon("x-circle", class_name="w-6 h-6 text-rose-500")),
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
                            NotificationState.selected_notification.get("created_at", "")[:16].replace("T", " at "),
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


def admin_notifications_view() -> rx.Component:
    """Render admin-specific notifications view."""
    return rx.box(
        # Header
        rx.flex(
            rx.box(
                rx.text(
                    "Notifications",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}"
                ),
                rx.text(
                    "Manage clinic alerts, patient updates, and system notifications",
                    class_name=GlassStyles.SUBHEADING_LIGHT
                )
            ),
            rx.flex(
                rx.button(
                    rx.icon("check-check", class_name="w-4 h-4 mr-2"),
                    "Mark all read",
                    on_click=NotificationState.mark_all_as_read,
                    class_name=GlassStyles.BUTTON_SECONDARY_LIGHT
                ),
                class_name="flex gap-3"
            ),
            class_name="flex items-start justify-between mb-6"
        ),
        
        # Filter tabs
        rx.box(
            filter_tabs(),
            class_name="mb-6"
        ),
        
        # Notifications list
        rx.cond(
            NotificationState.filtered_notifications.length() > 0,
            rx.box(
                rx.foreach(
                    NotificationState.filtered_notifications,
                    notification_card
                ),
                class_name="space-y-3"
            ),
            empty_state()
        ),
        
        # Detail modal
        notification_detail_modal()
    )


def patient_notifications_view() -> rx.Component:
    """Render patient-specific notifications view."""
    return rx.box(
        # Header
        rx.flex(
            rx.box(
                rx.text(
                    "My Notifications",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}"
                ),
                rx.text(
                    "Stay updated on your appointments, lab results, and treatment progress",
                    class_name=GlassStyles.SUBHEADING_LIGHT
                )
            ),
            rx.button(
                rx.icon("check-check", class_name="w-4 h-4 mr-2"),
                "Mark all read",
                on_click=NotificationState.mark_all_as_read,
                class_name=GlassStyles.BUTTON_SECONDARY_LIGHT
            ),
            class_name="flex items-start justify-between mb-6"
        ),
        
        # Filter tabs
        rx.box(
            filter_tabs(),
            class_name="mb-6"
        ),
        
        # Notifications list
        rx.cond(
            NotificationState.filtered_notifications.length() > 0,
            rx.box(
                rx.foreach(
                    NotificationState.filtered_notifications,
                    notification_card
                ),
                class_name="space-y-3"
            ),
            empty_state()
        ),
        
        # Detail modal
        notification_detail_modal()
    )


def notifications_content() -> rx.Component:
    """Main notifications content with role-based views."""
    return rx.cond(
        AuthState.is_admin,
        admin_notifications_view(),
        patient_notifications_view()
    )


@rx.page(
    route="/notifications",
    title="Notifications - Longevity Clinic",
    on_load=[
        AuthState.check_auth,
        rx.cond(
            AuthState.is_admin,
            NotificationState.load_admin_notifications,
            NotificationState.load_patient_notifications
        )
    ]
)
def notifications_page() -> rx.Component:
    """Notifications page component."""
    return authenticated_layout(
        rx.box(
            notifications_content(),
            class_name="p-6 max-w-4xl mx-auto"
        )
    )
