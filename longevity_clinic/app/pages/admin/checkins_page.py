"""Admin check-ins page for viewing and managing all patient check-ins."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...styles import GlassStyles
from ...states.admin_checkins_state import AdminCheckinsState
from ...config import get_logger

logger = get_logger("longevity_clinic.admin_checkins")


def checkin_status_badge(status: str) -> rx.Component:
    """Status badge for check-in status."""
    color_map = {
        "pending": "bg-amber-500/20 text-amber-400 border-amber-500/30",
        "reviewed": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
        "flagged": "bg-red-500/20 text-red-400 border-red-500/30",
    }
    return rx.el.span(
        status.capitalize(),
        class_name=f"px-2 py-0.5 text-xs font-medium rounded-full border {color_map.get(status, color_map['pending'])}",
    )


def checkin_type_icon(checkin_type: str) -> rx.Component:
    """Icon for check-in type."""
    icon_map = {
        "voice": "mic",
        "text": "message-square",
        "call": "phone",
    }
    return rx.icon(
        icon_map.get(checkin_type, "message-square"),
        class_name="w-4 h-4 text-teal-400",
    )


def sentiment_indicator(sentiment: str) -> rx.Component:
    """Sentiment indicator dot."""
    color_map = {
        "positive": "bg-emerald-400",
        "negative": "bg-red-400",
        "neutral": "bg-slate-400",
        "concerned": "bg-amber-400",
    }
    return rx.el.div(
        class_name=f"w-2 h-2 rounded-full {color_map.get(sentiment, 'bg-slate-400')}",
    )


def checkin_card(checkin: dict) -> rx.Component:
    """Individual check-in card for admin view."""
    return rx.el.div(
        rx.el.div(
            # Header with patient name and status
            rx.el.div(
                rx.el.div(
                    checkin_type_icon(checkin["type"]),
                    rx.el.span(
                        checkin["patient_name"],
                        class_name="text-white font-medium ml-2",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    sentiment_indicator(checkin["sentiment"]),
                    checkin_status_badge(checkin["status"]),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center justify-between mb-3",
            ),
            # Summary
            rx.el.p(
                checkin["summary"],
                class_name="text-slate-300 text-sm leading-relaxed mb-3",
            ),
            # Topics
            rx.el.div(
                rx.foreach(
                    checkin["key_topics"],
                    lambda topic: rx.el.span(
                        topic,
                        class_name="px-2 py-0.5 bg-slate-700/50 text-slate-400 text-xs rounded-full mr-1",
                    ),
                ),
                class_name="flex flex-wrap gap-1 mb-3",
            ),
            # Footer with timestamp and actions
            rx.el.div(
                rx.el.span(
                    checkin["timestamp"],
                    class_name="text-slate-500 text-xs",
                ),
                rx.el.div(
                    rx.cond(
                        checkin["status"] == "pending",
                        rx.el.button(
                            "Mark Reviewed",
                            on_click=lambda: AdminCheckinsState.mark_as_reviewed(
                                checkin["id"]
                            ),
                            class_name="px-3 py-1 text-xs bg-teal-500/20 text-teal-400 rounded-lg hover:bg-teal-500/30 transition-colors mr-2",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        checkin["status"] != "flagged",
                        rx.el.button(
                            "Flag",
                            on_click=lambda: AdminCheckinsState.flag_checkin(
                                checkin["id"]
                            ),
                            class_name="px-3 py-1 text-xs bg-red-500/10 text-red-400 rounded-lg hover:bg-red-500/20 transition-colors",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between",
            ),
            class_name="p-4",
        ),
        class_name=f"{GlassStyles.CARD} overflow-hidden",
    )


def status_tab_button(label: str, status: str) -> rx.Component:
    """Tab button for filtering by status."""
    return rx.el.button(
        label,
        on_click=lambda: AdminCheckinsState.set_active_status_tab(status),
        class_name=rx.cond(
            AdminCheckinsState.active_status_tab == status,
            "px-4 py-2 text-sm font-medium text-white bg-teal-500/20 border border-teal-500/30 rounded-lg",
            "px-4 py-2 text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors",
        ),
    )


def admin_checkins_page() -> rx.Component:
    """Admin check-ins management page with search and filtering - similar to patient management."""
    logger.info("Rendering admin_checkins_page")

    return authenticated_layout(
        rx.el.div(
            # Page header - similar to section_header in sections.py
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Patient Check-ins",
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.p(
                        "Review and manage patient check-ins across all patients",
                        class_name="text-slate-400 text-sm mt-1",
                    ),
                ),
                # Stats summary
                rx.el.div(
                    rx.el.span(
                        rx.el.span(
                            AdminCheckinsState.pending_count,
                            class_name="text-amber-400 font-semibold",
                        ),
                        " pending",
                        class_name="text-slate-400 text-sm mr-4",
                    ),
                    rx.el.span(
                        rx.el.span(
                            AdminCheckinsState.flagged_count,
                            class_name="text-red-400 font-semibold",
                        ),
                        " flagged",
                        class_name="text-slate-400 text-sm mr-4",
                    ),
                    rx.el.span(
                        rx.el.span(
                            AdminCheckinsState.total_count,
                            class_name="text-teal-400 font-semibold",
                        ),
                        " total",
                        class_name="text-slate-400 text-sm",
                    ),
                ),
                class_name="flex items-start justify-between mb-6",
            ),
            # Search and filter bar - similar to patient management in sections.py
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search by patient name, topics, or summary...",
                        value=AdminCheckinsState.search_query,
                        on_change=AdminCheckinsState.set_search_query,
                        class_name="pl-10 block w-full bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 sm:text-sm py-2.5 focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
                    ),
                    class_name="relative flex-1 max-w-md mr-4",
                ),
                # Status filter tabs inline
                rx.el.div(
                    status_tab_button("All", "all"),
                    status_tab_button("Pending", "pending"),
                    status_tab_button("Reviewed", "reviewed"),
                    status_tab_button("Flagged", "flagged"),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex flex-wrap items-center mb-6",
            ),
            # Check-ins list
            rx.el.div(
                rx.cond(
                    AdminCheckinsState.filtered_checkins.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            AdminCheckinsState.filtered_checkins,
                            checkin_card,
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.icon("inbox", class_name="w-12 h-12 text-slate-600 mb-4"),
                        rx.el.p(
                            "No check-ins found",
                            class_name="text-slate-400 text-sm",
                        ),
                        rx.el.p(
                            "Try adjusting your search or filter criteria",
                            class_name="text-slate-500 text-xs mt-1",
                        ),
                        class_name="flex flex-col items-center justify-center py-12",
                    ),
                ),
            ),
            class_name=f"{GlassStyles.PANEL} p-6",
        ),
        on_mount=[AdminCheckinsState.sync_call_logs_to_admin],
    )
