"""Admin check-ins page - manages all patient check-ins."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...components.modals import checkin_detail_modal
from ...components.shared import (
    admin_checkin_card as _admin_checkin_card,
    status_filter_button,
    search_input,
)
from ...states.shared.checkin import CheckinState
from ...styles.constants import GlassStyles


# =====================================
# Admin Components
# =====================================

def admin_checkin_card(checkin: dict) -> rx.Component:
    """Admin check-in card using centralized component."""
    return _admin_checkin_card(
        checkin=checkin,
        on_click=CheckinState.open_checkin_detail,
    )


def admin_checkin_detail_modal() -> rx.Component:
    """Admin check-in detail modal using centralized component."""
    return checkin_detail_modal(
        show_modal=CheckinState.show_checkin_detail_modal,
        checkin_status=CheckinState.selected_checkin_status,
        checkin_patient_name=CheckinState.selected_checkin_patient_name,
        checkin_timestamp=CheckinState.selected_checkin_timestamp,
        checkin_type=CheckinState.selected_checkin_type,
        checkin_summary=CheckinState.selected_checkin_summary,
        checkin_topics=CheckinState.selected_checkin_topics,
        checkin_id=CheckinState.selected_checkin_id,
        on_close=CheckinState.set_show_checkin_detail_modal,
        on_flag=CheckinState.flag_checkin,
        on_mark_reviewed=CheckinState.mark_as_reviewed,
        show_patient_name=True,
        show_actions=True,
        checkin_raw_transcript=CheckinState.selected_checkin_raw_transcript,
    )


# =============================================================================
# Admin View
# =============================================================================


def admin_checkins_view() -> rx.Component:
    """Admin view for managing all patient check-ins."""
    status_tabs = [
        ("Pending", "pending", CheckinState.pending_count, "amber"),
        ("Reviewed", "reviewed", CheckinState.reviewed_count, "teal"),
        ("Flagged", "flagged", CheckinState.flagged_count, "red"),
        ("All", "all", CheckinState.total_count, "white"),
    ]
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
        search_input(
            placeholder="Search by patient name, topic, or content...",
            value=CheckinState.search_query,
            on_change=CheckinState.set_search_query,
        ),
        # Status Tabs
        rx.el.div(
            *[
                status_filter_button(
                    label, status, count, color,
                    CheckinState.active_status_tab,
                    CheckinState.set_active_status_tab,
                )
                for label, status, count, color in status_tabs
            ],
            class_name="flex gap-2 mt-6 mb-6",
        ),
        # Check-ins List
        rx.match(
            CheckinState.filtered_checkins.length() > 0,
            (True, rx.el.div(
                rx.foreach(CheckinState.filtered_checkins, admin_checkin_card),
                class_name="space-y-4",
            )),
            rx.el.div(
                rx.icon("inbox", class_name="w-12 h-12 text-slate-600 mb-4"),
                rx.el.p("No check-ins found", class_name="text-slate-400"),
                class_name="flex flex-col items-center justify-center py-12",
            ),
        ),
        admin_checkin_detail_modal(),
    )


# =============================================================================
# Admin Check-ins Page
# =============================================================================


def admin_checkins_page() -> rx.Component:
    """Standalone admin check-ins page."""
    return authenticated_layout(admin_checkins_view())
