"""Admin check-ins page - manages all patient check-ins."""

import reflex as rx

from ...components.layout import authenticated_layout
from ...components.modals import checkin_detail_modal
from ...components.paginated_view import paginated_list_with_filters
from ...components.shared import (
    admin_checkin_card as _admin_checkin_card,
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
        on_close=CheckinState.close_checkin_detail,
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
    # Define filter tabs: (label, value, count, color)
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
        # Paginated list with filter tabs
        rx.el.div(
            paginated_list_with_filters(
                items=CheckinState.paginated_checkins,
                item_renderer=admin_checkin_card,
                filter_tabs=status_tabs,
                active_filter=CheckinState.active_status_tab,
                on_filter_change=CheckinState.set_active_status_tab,
                has_previous=CheckinState.has_previous_page,
                has_next=CheckinState.has_next_page,
                page_info=CheckinState.page_info,
                showing_info=CheckinState.showing_info,
                on_previous=CheckinState.previous_page,
                on_next=CheckinState.next_page,
                empty_icon="inbox",
                empty_message="No check-ins found",
                filter_class="flex gap-2 mt-6 mb-6",
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
