"""Centralized check-in components for admin and patient views.

This module provides unified UI components for check-in functionality:
- status_badge: Status indicator pill (pending/reviewed/flagged)
- type_icon: Check-in type icon (voice/call/text)
- topics_list: Topics/keywords display
- checkin_card: Unified card used by both admin and patient views
- patient_checkin_card: Pre-configured card for patient views (no patient name)
- admin_checkin_card: Pre-configured card for admin views (shows patient name)
- status_filter_button: Tab filter for status filtering
- stat_card: Statistics display card

Usage:
    from longevity_clinic.app.components.shared import checkin_card, patient_checkin_card

    # Admin view (shows patient name)
    admin_checkin_card(checkin, on_click=handler)

    # Patient view (hides patient name)
    patient_checkin_card(checkin, on_click=handler)
"""

import reflex as rx
from ...styles.constants import GlassStyles


def status_badge(status: str) -> rx.Component:
    """Reusable status badge component.

    Args:
        status: One of 'pending', 'flagged', 'reviewed'

    Returns:
        Colored badge component
    """
    base = "px-2 py-0.5 rounded-full text-xs capitalize"
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "pending",
                f"{base} bg-amber-500/10 text-amber-400 border border-amber-500/20",
            ),
            ("flagged", f"{base} bg-red-500/10 text-red-400 border border-red-500/20"),
            f"{base} bg-teal-500/10 text-teal-400 border border-teal-500/20",
        ),
    )


def type_icon(checkin_type: str) -> rx.Component:
    """Icon based on check-in type.

    Args:
        checkin_type: One of 'voice', 'call', 'text'

    Returns:
        Icon component with appropriate color
    """
    return rx.match(
        checkin_type,
        ("voice", rx.icon("mic", class_name="w-3.5 h-3.5 text-teal-400")),
        ("call", rx.icon("phone", class_name="w-3.5 h-3.5 text-purple-400")),
        rx.icon("message-square", class_name="w-3.5 h-3.5 text-blue-400"),
    )


def topics_list(topics: list) -> rx.Component:
    """Display list of topics/keywords.

    Args:
        topics: List of topic strings

    Returns:
        Wrapped flex container of topic pills
    """
    return rx.el.div(
        rx.foreach(
            topics,
            lambda topic: rx.el.span(
                topic,
                class_name="px-2 py-0.5 rounded-full text-xs bg-white/5 text-slate-400 border border-white/10",
            ),
        ),
        class_name="flex flex-wrap gap-1.5",
    )


def checkin_card(
    checkin: dict,
    show_patient_name: bool = False,
    on_click: rx.EventHandler | None = None,
) -> rx.Component:
    """Unified check-in card component for admin and patient views.

    Uses admin-style design with:
    - Type icon (not text label)
    - Topics/keywords tags
    - Status badge
    - Optional patient name display
    - Call type indicator (purple border)

    Args:
        checkin: Check-in data dict with keys: patient_name, type, timestamp,
                 summary, raw_transcript, key_topics, status
        show_patient_name: Whether to show patient name (True for admin, False for patient)
        on_click: Optional click handler for opening details modal

    Returns:
        Styled card component
    """
    card_content = rx.el.div(
        rx.el.div(
            # Header row: name/type and timestamp
            rx.el.div(
                rx.el.div(
                    # Patient name (admin only)
                    rx.cond(
                        show_patient_name,
                        rx.el.span(
                            checkin["patient_name"],
                            class_name="font-semibold text-white mr-2",
                        ),
                        rx.fragment(),
                    ),
                    # Type icon
                    type_icon(checkin["type"]),
                    class_name="flex items-center",
                ),
                rx.el.span(checkin["timestamp"], class_name="text-xs text-slate-500"),
                class_name="flex items-center justify-between mb-2",
            ),
            # Summary content
            rx.el.p(
                rx.cond(
                    checkin["summary"] != "",
                    checkin["summary"],
                    rx.cond(
                        checkin["raw_transcript"] != "",
                        checkin["raw_transcript"],
                        "No content available",
                    ),
                ),
                class_name="text-sm text-slate-300 line-clamp-2 mb-3",
            ),
            # Footer: topics and status
            rx.el.div(
                topics_list(checkin["key_topics"]),
                status_badge(checkin["status"]),
                class_name="flex items-center justify-between mt-2",
            ),
            class_name=rx.cond(
                checkin["type"] == "call",
                f"{GlassStyles.PANEL} p-4 hover:bg-white/10 transition-all cursor-pointer border-l-2 border-purple-500/50",
                f"{GlassStyles.PANEL} p-4 hover:bg-white/10 transition-all cursor-pointer",
            ),
        ),
    )

    # Wrap with click handler if provided
    if on_click is not None:
        return rx.el.div(
            card_content,
            on_click=lambda: on_click(checkin),  # type: ignore[arg-type]
        )
    return card_content


def status_filter_button(
    label: str,
    status: str,
    count: rx.Var,
    color: str,
    active_status: rx.Var[str],
    on_click: rx.EventHandler,
) -> rx.Component:
    """Reusable status filter tab button.

    Args:
        label: Button display text
        status: Status value to filter by
        count: Count var to display
        color: Color name for the count badge (amber/teal/red/white)
        active_status: Currently active status var
        on_click: Event handler for status change

    Returns:
        Tab button component
    """
    return rx.el.button(
        rx.el.span(label, class_name="mr-2"),
        rx.el.span(
            count,
            class_name=f"px-2 py-0.5 rounded-full text-xs bg-{color}-500/20 text-{color}-400",
        ),
        on_click=lambda: on_click(status),  # type: ignore[arg-type]
        class_name=rx.cond(
            active_status == status,
            "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
            "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
        ),
    )


def stat_card(
    icon_name: str, icon_color: str, label: str, value: rx.Var, suffix: str = ""
) -> rx.Component:
    """Reusable stat card for check-in summaries.

    Args:
        icon_name: Lucide icon name
        icon_color: Color name for icon (teal/purple/amber)
        label: Label text
        value: Numeric value var
        suffix: Optional suffix text

    Returns:
        Stat card component
    """
    return rx.el.div(
        rx.icon(icon_name, class_name=f"w-6 h-6 text-{icon_color}-400 mb-2"),
        rx.el.p(label, class_name="text-xs text-slate-400 uppercase tracking-wider"),
        rx.el.div(
            rx.el.span(value, class_name="text-2xl font-bold text-white"),
            rx.cond(
                suffix != "",
                rx.el.span(suffix, class_name="text-sm text-slate-400 ml-1"),
                rx.fragment(),
            ),
            class_name="flex items-baseline",
        ),
        class_name=f"{GlassStyles.PANEL} p-4",
    )


def patient_checkin_card(
    checkin: dict,
    on_click: rx.EventHandler | None = None,
) -> rx.Component:
    """Patient check-in card (no patient name shown).

    Pre-configured checkin_card for patient views that hides patient name.

    Args:
        checkin: Check-in data dict
        on_click: Optional click handler for opening details modal

    Returns:
        Styled card component without patient name
    """
    return checkin_card(
        checkin=checkin,
        show_patient_name=False,
        on_click=on_click,
    )


def admin_checkin_card(
    checkin: dict,
    on_click: rx.EventHandler | None = None,
) -> rx.Component:
    """Admin check-in card (shows patient name).

    Pre-configured checkin_card for admin views that shows patient name.

    Args:
        checkin: Check-in data dict
        on_click: Optional click handler for opening details modal

    Returns:
        Styled card component with patient name
    """
    return checkin_card(
        checkin=checkin,
        show_patient_name=True,
        on_click=on_click,
    )
