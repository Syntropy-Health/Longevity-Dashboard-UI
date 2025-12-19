"""Patient Check-ins page with unified role-based routing."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...components.modals import transcript_modal
from ...components.shared import patient_checkin_card as _patient_checkin_card, stat_card
from ...states import AuthState
from ...states.shared.checkin import CheckinState
from ...styles.constants import GlassStyles
from .modals import checkin_modal

# Import admin view from admin module
from ..admin.checkins import admin_checkins_view


# =============================================================================
# Page Wrapper (for on_mount/on_unmount lifecycle)
# =============================================================================


def checkins_page_wrapper():
    """Wrapper for checkins page with background processing lifecycle."""
    return rx.fragment(
        checkins_page(),
        on_mount=CheckinState.start_background_processing,
        on_unmount=CheckinState.stop_background_processing,
    )


# =============================================================================
# Patient Components
# =============================================================================


def patient_checkin_card(checkin: dict) -> rx.Component:
    """Patient check-in card (no patient name shown)."""
    return _patient_checkin_card(
        checkin=checkin,
        on_click=CheckinState.open_transcript_modal,
    )


# =============================================================================
# Patient View
# =============================================================================


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
                rx.el.div(
                    rx.icon("phone", class_name="w-4 h-4 text-purple-400 mr-2"),
                    rx.el.span(
                        "Voice Line:", class_name="text-xs text-slate-500 mr-1.5"
                    ),
                    rx.el.span(
                        AuthState.user_phone_formatted,
                        class_name="text-sm font-mono text-purple-300",
                    ),
                    class_name=f"{GlassStyles.PANEL} px-3 py-2 flex items-center mr-3",
                ),
                rx.button(
                    rx.cond(
                        CheckinState.call_logs_syncing,
                        rx.icon(
                            "loader-circle", class_name="w-4 h-4 animate-spin mr-2"
                        ),
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
        ),
        rx.cond(
            CheckinState.last_sync_time != "",
            rx.el.p(
                rx.el.span("Last synced: ", class_name="text-slate-500"),
                rx.el.span(CheckinState.last_sync_time, class_name="text-slate-400"),
                class_name="text-xs mb-4",
            ),
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
                rx.foreach(CheckinState.checkins, patient_checkin_card),
                class_name="space-y-4",
            ),
        ),
        # Modals
        checkin_modal(),
        transcript_modal(
            show_modal=CheckinState.show_transcript_modal,
            transcript_text=CheckinState.selected_checkin_transcript,
            on_close=CheckinState.close_transcript_modal,
            title="Full Transcript",
        ),
    )


# =============================================================================
# Main Page (Role-based routing)
# =============================================================================


def checkins_page() -> rx.Component:
    """Unified check-ins page with role-based view."""
    return authenticated_layout(
        rx.cond(AuthState.is_admin, admin_checkins_view(), patient_checkins_view())
    )
