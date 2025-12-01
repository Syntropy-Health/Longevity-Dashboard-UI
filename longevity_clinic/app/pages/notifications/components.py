"""Notifications page components.

This module contains reusable UI components for the notifications page:
- Notification icon based on type
- Notification type badge
- Notification card
- Filter tabs
- Empty state display
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ...states.notification_state import NotificationState


def notification_icon(notification_type: str) -> rx.Component:
    """Get icon component for notification type.
    
    Args:
        notification_type: Type of notification (info, warning, success, etc.)
        
    Returns:
        An icon component styled for the notification type
    """
    icon_map = {
        "info": "info",
        "warning": "triangle-alert",
        "success": "circle-check",
        "error": "circle-x",
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
    """Render a type badge for notifications.
    
    Args:
        notification_type: Type of notification
        
    Returns:
        A styled badge component showing the notification type
    """
    return rx.match(
        notification_type,
        ("info", rx.box("Info", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700")),
        ("warning", rx.box("Warning", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-700")),
        ("success", rx.box("Success", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700")),
        ("error", rx.box("Error", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-700")),
        ("appointment", rx.box("Appointment", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-teal-100 text-teal-700")),
        ("treatment", rx.box("Treatment", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-700")),
        ("lab", rx.box("Lab", class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-cyan-100 text-cyan-700")),
        rx.box(notification_type, class_name="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600")
    )


def notification_card(notification: dict) -> rx.Component:
    """Render a single notification card.
    
    Args:
        notification: Dictionary containing notification data
        
    Returns:
        A styled card component displaying the notification
    """
    return rx.box(
        rx.flex(
            # Icon with background
            rx.box(
                rx.match(
                    notification.get("type", "info"),
                    ("info", rx.icon("info", class_name="w-5 h-5 text-blue-500")),
                    ("warning", rx.icon("triangle-alert", class_name="w-5 h-5 text-amber-500")),
                    ("success", rx.icon("circle-check", class_name="w-5 h-5 text-emerald-500")),
                    ("error", rx.icon("circle-x", class_name="w-5 h-5 text-rose-500")),
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
                        class_name=rx.cond(
                            notification.get("is_read", False),
                            "font-semibold text-gray-600",
                            "font-semibold text-gray-900",
                        )
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
                        notification.get("created_at", ""),
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
        class_name=rx.cond(
            notification.get("is_read", False),
            "p-4 rounded-xl cursor-pointer transition-all duration-200 bg-white/60 border-white/40 border backdrop-blur-sm hover:shadow-md hover:border-teal-300/50",
            "p-4 rounded-xl cursor-pointer transition-all duration-200 bg-teal-50/50 border-teal-200/50 border backdrop-blur-sm hover:shadow-md hover:border-teal-300/50",
        )
    )


def filter_tabs() -> rx.Component:
    """Render filter tabs for notifications.
    
    Returns:
        A tab component for filtering notifications
    """
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
    """Render empty state when no notifications.
    
    Returns:
        An empty state component with illustration and message
    """
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
