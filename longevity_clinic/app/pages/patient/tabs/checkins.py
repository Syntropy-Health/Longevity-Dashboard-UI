"""Check-ins tab component for patient portal.

This tab uses the centralized checkin components from components/shared/.
"""

import reflex as rx
from ....states.shared.checkin import CheckinState
from ....styles.constants import GlassStyles
from ....components.modals import transcript_modal
from ....components.shared import patient_checkin_card as _patient_checkin_card, stat_card


def patient_checkin_card(checkin: dict) -> rx.Component:
    """Patient check-in card using centralized component (no patient name)."""
    return _patient_checkin_card(
        checkin=checkin,
        on_click=CheckinState.open_transcript_modal,
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
        # Check-ins List
        rx.el.div(
            rx.el.h3(
                "Recent Check-ins", class_name="text-lg font-semibold text-white mb-4"
            ),
            rx.el.div(
                rx.foreach(CheckinState.checkins, patient_checkin_card),
                class_name="space-y-4",
            ),
        ),
        # Transcript Modal
        transcript_modal(
            show_modal=CheckinState.show_transcript_modal,
            transcript_text=CheckinState.selected_checkin_transcript,
            on_close=CheckinState.close_transcript_modal,
            title="Full Transcript",
        ),
    )
