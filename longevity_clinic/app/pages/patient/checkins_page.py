"""Unified Check-ins page with role-based views."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...components.modals import transcript_modal
from ...data.demo import DEMO_PHONE_NUMBER
from ...states import AuthState
from ...states.checkins import CheckinState
from ...styles.constants import GlassStyles
from .tabs.checkins import checkin_card
from .modals import checkin_modal


# =============================================================================
# Shared Components
# =============================================================================


def status_badge(status: str) -> rx.Component:
    """Reusable status badge component."""
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "pending",
            "px-2 py-0.5 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 capitalize",
            rx.cond(
                status == "flagged",
                "px-2 py-0.5 rounded-full text-xs bg-red-500/10 text-red-400 border border-red-500/20 capitalize",
                "px-2 py-0.5 rounded-full text-xs bg-teal-500/10 text-teal-400 border border-teal-500/20 capitalize",
            ),
        ),
    )


def type_icon(checkin_type: str) -> rx.Component:
    """Icon based on check-in type."""
    return rx.match(
        checkin_type,
        ("voice", rx.icon("mic", class_name="w-3 h-3 ml-2 inline text-teal-400")),
        ("call", rx.icon("phone", class_name="w-3 h-3 ml-2 inline text-purple-400")),
        rx.icon("message-square", class_name="w-3 h-3 ml-2 inline text-blue-400"),
    )


def topics_list(topics: list) -> rx.Component:
    """Reusable topics display."""
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


def status_filter_button(
    label: str, status: str, count: rx.Var, color: str
) -> rx.Component:
    """Reusable status filter tab button."""
    return rx.el.button(
        rx.el.span(label, class_name="mr-2"),
        rx.el.span(
            count,
            class_name=f"px-2 py-0.5 rounded-full text-xs bg-{color}-500/20 text-{color}-400",
        ),
        on_click=lambda: CheckinState.set_active_status_tab(status),
        class_name=rx.cond(
            CheckinState.active_status_tab == status,
            "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
            "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
        ),
    )


# =============================================================================
# Admin Components
# =============================================================================


def admin_checkin_card(checkin: dict) -> rx.Component:
    """Admin check-in card showing patient info and status."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        checkin["patient_name"], class_name="font-semibold text-white"
                    ),
                    type_icon(checkin["type"]),
                    class_name="flex items-center",
                ),
                rx.el.span(checkin["timestamp"], class_name="text-xs text-slate-500"),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.p(
                checkin["summary"],
                class_name="text-sm text-slate-300 line-clamp-2 mb-3",
            ),
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
        on_click=lambda: CheckinState.open_checkin_detail(checkin),
    )


def admin_checkin_detail_modal() -> rx.Component:
    """Modal for viewing check-in details using computed vars."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Check-in Details",
                                class_name="text-xl font-bold text-white",
                            ),
                            status_badge(CheckinState.selected_checkin_status),
                            class_name="flex items-center gap-3",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Info grid
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Patient",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                CheckinState.selected_checkin_patient_name,
                                class_name="text-white font-medium",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Submitted",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                CheckinState.selected_checkin_timestamp,
                                class_name="text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Type",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.div(
                                rx.cond(
                                    CheckinState.selected_checkin_type == "voice",
                                    rx.el.div(
                                        rx.icon(
                                            "mic",
                                            class_name="w-4 h-4 text-teal-400 mr-1",
                                        ),
                                        "Voice",
                                        class_name="flex items-center text-white",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "message-square",
                                            class_name="w-4 h-4 text-blue-400 mr-1",
                                        ),
                                        "Text",
                                        class_name="flex items-center text-white",
                                    ),
                                ),
                            ),
                        ),
                        class_name=f"grid grid-cols-3 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Content
                    rx.el.div(
                        rx.el.p(
                            "Check-in Content",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.p(
                            CheckinState.selected_checkin_summary,
                            class_name="text-sm text-white leading-relaxed",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Topics
                    rx.el.div(
                        rx.el.p(
                            "Topics",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                CheckinState.selected_checkin_topics,
                                lambda t: rx.el.span(
                                    t,
                                    class_name="px-3 py-1 rounded-full text-xs bg-teal-500/10 text-teal-300 border border-teal-500/20",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close", class_name=GlassStyles.BUTTON_SECONDARY
                            ),
                        ),
                        rx.cond(
                            CheckinState.selected_checkin_status == "pending",
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("flag", class_name="w-4 h-4 mr-2"),
                                    "Flag",
                                    on_click=lambda: CheckinState.flag_checkin(
                                        CheckinState.selected_checkin_id
                                    ),
                                    class_name="px-4 py-2 rounded-xl text-sm font-medium bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all flex items-center",
                                ),
                                rx.el.button(
                                    rx.icon("check", class_name="w-4 h-4 mr-2"),
                                    "Mark Reviewed",
                                    on_click=lambda: CheckinState.mark_as_reviewed(
                                        CheckinState.selected_checkin_id
                                    ),
                                    class_name=f"{GlassStyles.BUTTON_PRIMARY} flex items-center",
                                ),
                                class_name="flex gap-3",
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex justify-between",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg {GlassStyles.MODAL} z-50",
            ),
        ),
        open=CheckinState.show_checkin_detail_modal,
        on_open_change=CheckinState.set_show_checkin_detail_modal,
    )


# =============================================================================
# Admin View
# =============================================================================


def admin_checkins_view() -> rx.Component:
    """Admin view for managing all patient check-ins."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h1(
                "Patient Check-ins",
                class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
            ),
            rx.el.p(
                "Review and manage patient voice and text logs",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Search
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search by patient name, topic, or content...",
                    value=CheckinState.search_query,
                    on_change=CheckinState.set_search_query,
                    class_name="w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                ),
                class_name="relative",
            ),
            class_name="mb-6",
        ),
        # Status Tabs
        rx.el.div(
            status_filter_button(
                "Pending", "pending", CheckinState.pending_count, "amber"
            ),
            status_filter_button(
                "Reviewed", "reviewed", CheckinState.reviewed_count, "teal"
            ),
            status_filter_button(
                "Flagged", "flagged", CheckinState.flagged_count, "red"
            ),
            status_filter_button("All", "all", CheckinState.total_count, "white"),
            class_name="flex gap-2 mb-6",
        ),
        # List
        rx.cond(
            CheckinState.filtered_checkins.length() > 0,
            rx.el.div(
                rx.foreach(CheckinState.filtered_checkins, admin_checkin_card),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.icon("inbox", class_name="w-12 h-12 text-slate-600 mb-4"),
                rx.el.p("No check-ins found", class_name="text-slate-400"),
                class_name="flex flex-col items-center justify-center py-12",
            ),
        ),
        admin_checkin_detail_modal(),
    )


# =============================================================================
# Patient View
# =============================================================================


def stat_card(
    icon_name: str, icon_color: str, label: str, value: rx.Var, suffix: str = ""
) -> rx.Component:
    """Reusable stat card."""
    return rx.el.div(
        rx.icon(icon_name, class_name=f"w-6 h-6 text-{icon_color}-400 mb-2"),
        rx.el.p(label, class_name="text-xs text-slate-400 uppercase tracking-wider"),
        rx.el.span(value, class_name="text-2xl font-bold text-white"),
        rx.cond(
            suffix != "",
            rx.el.span(suffix, class_name="text-sm text-slate-400 ml-1"),
            rx.fragment(),
        ),
        class_name=f"{GlassStyles.PANEL} p-4",
    )


def patient_checkins_view() -> rx.Component:
    """Patient view for their own check-ins."""
    return rx.el.div(
        # Header with Phone Number Info
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Self Check-ins",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
                ),
                rx.el.p(
                    "Voice and text logs between visits",
                    class_name="text-slate-400 text-sm",
                ),
            ),
            # Right side: Phone number badge + Refresh button
            rx.el.div(
                # Demo Phone Number Badge
                rx.el.div(
                    rx.icon("phone", class_name="w-4 h-4 text-purple-400 mr-2"),
                    rx.el.span("Voice Line: ", class_name="text-xs text-slate-500"),
                    rx.el.span(DEMO_PHONE_NUMBER, class_name="text-sm font-mono text-purple-300"),
                    class_name=f"{GlassStyles.PANEL} px-3 py-2 flex items-center mr-3",
                ),
                rx.button(
                    rx.cond(
                        CheckinState.call_logs_syncing,
                        rx.icon("loader-circle", class_name="w-4 h-4 animate-spin mr-2"),
                        rx.icon("refresh-cw", class_name="w-4 h-4 mr-2"),
                    ),
                    rx.cond(CheckinState.call_logs_syncing, "Syncing...", "Refresh"),
                    on_click=CheckinState.refresh_call_logs,
                    disabled=CheckinState.call_logs_syncing,
                    class_name=f"{GlassStyles.BUTTON_SECONDARY} flex items-center text-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-start mb-6",
        ),
        # Action Button
        rx.el.div(
            rx.el.button(
                rx.icon("circle-plus", class_name="w-5 h-5 mr-2"),
                "Check-in Now",
                on_click=CheckinState.open_checkin_modal,
                class_name=f"{GlassStyles.BUTTON_PRIMARY} flex items-center",
            ),
            class_name="mb-6",
        ),
        # Stats
        rx.el.div(
            stat_card(
                "mic", "teal", "This Week", CheckinState.checkins.length(), " check-ins"
            ),
            stat_card(
                "phone",
                "purple",
                "Voice Calls",
                CheckinState.voice_call_checkins_count,
                " logged",
            ),
            stat_card(
                "clock",
                "amber",
                "Pending Review",
                CheckinState.unreviewed_checkins_count,
            ),
            class_name="grid grid-cols-3 gap-4 mb-6",
        ),
        # Sync Status
        rx.cond(
            CheckinState.call_logs_syncing,
            rx.el.div(
                rx.icon(
                    "loader-circle",
                    class_name="w-5 h-5 text-teal-400 animate-spin mr-2",
                ),
                rx.el.span(
                    "Fetching call logs...", class_name="text-sm text-slate-400"
                ),
                class_name="flex items-center mb-4",
            ),
            rx.fragment(),
        ),
        rx.cond(
            CheckinState.call_logs_sync_error != "",
            rx.el.div(
                rx.icon("circle-alert", class_name="w-4 h-4 text-red-400 mr-2"),
                rx.el.span(
                    CheckinState.call_logs_sync_error, class_name="text-sm text-red-400"
                ),
                class_name="flex items-center mb-4 p-2 bg-red-500/10 rounded-lg",
            ),
            rx.fragment(),
        ),
        rx.cond(
            CheckinState.last_sync_time != "",
            rx.el.p(
                rx.el.span("Last synced: ", class_name="text-slate-500"),
                rx.el.span(CheckinState.last_sync_time, class_name="text-slate-400"),
                class_name="text-xs mb-4",
            ),
            rx.fragment(),
        ),
        # Check-ins List
        rx.el.div(
            rx.el.h3(
                rx.icon(
                    "message-square", class_name="w-5 h-5 text-teal-400 mr-2 inline"
                ),
                "Recent Check-ins",
                class_name="text-lg font-semibold text-white mb-4 flex items-center",
            ),
            rx.el.div(
                rx.foreach(CheckinState.checkins, checkin_card), class_name="space-y-4"
            ),
        ),
        checkin_modal(),
        transcript_modal(
            show_modal=CheckinState.show_transcript_modal,
            transcript_text=CheckinState.selected_checkin_transcript,
            on_close=CheckinState.close_transcript_modal,
            title="Full Transcript",
        ),
    )


# =============================================================================
# Main Page
# =============================================================================


def checkins_page() -> rx.Component:
    """Unified check-ins page with role-based view."""
    return authenticated_layout(
        rx.cond(AuthState.is_admin, admin_checkins_view(), patient_checkins_view())
    )
