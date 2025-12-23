"""Check-ins tab component for patient portal.

This tab uses the centralized checkin components from components/shared/.
"""

import reflex as rx

from ....components.modals import checkin_detail_modal
from ....components.shared import (
    pagination_controls,
    patient_checkin_card as _patient_checkin_card,
    stat_card,
)
from ....states.shared.checkin import CheckinState
from ....styles.constants import GlassStyles


def patient_checkin_card(checkin: dict) -> rx.Component:
    """Patient check-in card using centralized component (no patient name)."""
    return _patient_checkin_card(
        checkin=checkin,
        on_click=CheckinState.open_checkin_detail,
    )


def checkins_tab() -> rx.Component:
    """Check-ins tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Self Check-ins", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Voice and text logs between visits.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Quick action buttons
        rx.el.div(
            rx.el.button(
                rx.icon("mic", class_name="w-5 h-5 mr-2"),
                "Voice Check-in",
                on_click=CheckinState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            rx.el.button(
                rx.icon("message-square", class_name="w-5 h-5 mr-2"),
                "Text Note",
                on_click=CheckinState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_SECONDARY,
            ),
            class_name="flex gap-3 mb-6",
        ),
        # Summary Cards - using centralized stat_card
        rx.el.div(
            stat_card(
                "mic",
                "teal",
                "This Week",
                CheckinState.checkins.length(),
                " check-ins",
            ),
            stat_card(
                "clock",
                "amber",
                "Pending Review",
                CheckinState.unreviewed_checkins_count,
            ),
            class_name="grid grid-cols-2 gap-4 mb-6",
        ),
        # Check-ins List with Pagination
        rx.el.div(
            rx.el.h3(
                "Recent Check-ins", class_name="text-lg font-semibold text-white mb-4"
            ),
            rx.match(
                CheckinState.filtered_checkins.length() > 0,
                (
                    True,
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(
                                CheckinState.paginated_checkins, patient_checkin_card
                            ),
                            class_name="space-y-4",
                        ),
                        # Pagination controls
                        pagination_controls(
                            has_previous=CheckinState.has_previous_page,
                            has_next=CheckinState.has_next_page,
                            page_info=CheckinState.page_info,
                            showing_info=CheckinState.showing_info,
                            on_previous=CheckinState.previous_page,
                            on_next=CheckinState.next_page,
                        ),
                    ),
                ),
                rx.el.div(
                    rx.icon("inbox", class_name="w-10 h-10 text-slate-600 mb-3"),
                    rx.el.p("No check-ins yet", class_name="text-slate-400 text-sm"),
                    class_name="flex flex-col items-center justify-center py-8",
                ),
            ),
        ),
        # Check-in Detail Modal (patient view - no patient name, no actions)
        checkin_detail_modal(
            show_modal=CheckinState.show_checkin_detail_modal,
            checkin_status=CheckinState.selected_checkin_status,
            checkin_patient_name=CheckinState.selected_checkin_patient_name,
            checkin_timestamp=CheckinState.selected_checkin_timestamp,
            checkin_type=CheckinState.selected_checkin_type,
            checkin_summary=CheckinState.selected_checkin_summary,
            checkin_topics=CheckinState.selected_checkin_topics,
            checkin_id=CheckinState.selected_checkin_id,
            checkin_raw_transcript=CheckinState.selected_checkin_transcript,
            on_close=CheckinState.set_show_checkin_detail_modal(False),
            show_patient_name=False,  # Patient view doesn't need their own name
            show_actions=False,  # Patient view doesn't need admin actions
        ),
    )
