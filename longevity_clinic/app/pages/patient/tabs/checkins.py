"""Check-ins tab component for patient portal."""

import reflex as rx
from ....states.patient_checkin_state import PatientCheckinState
from ....styles.constants import GlassStyles


def checkin_card(checkin: dict) -> rx.Component:
    """Check-in card."""
    type_icons = {
        "voice": "mic",
        "text": "message-square",
        "call": "phone",
    }
    sentiment_colors = {
        "positive": "teal",
        "neutral": "slate",
        "negative": "amber",
    }
    icon = type_icons.get(checkin.get("type", "text"), "message-square")
    color = sentiment_colors.get(checkin.get("sentiment", "neutral"), "slate")

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-5 h-5 text-{color}-400"),
                class_name=f"w-12 h-12 rounded-xl bg-{color}-500/10 flex items-center justify-center mr-4 border border-{color}-500/20",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        checkin["type"].capitalize(),
                        class_name="text-xs font-medium text-teal-400 mr-2",
                    ),
                    rx.el.span(
                        checkin["timestamp"], class_name="text-xs text-slate-400"
                    ),
                    class_name="flex items-center mb-1",
                ),
                rx.el.p(
                    checkin["summary"], class_name="text-sm text-white line-clamp-2"
                ),
                rx.cond(
                    checkin["key_topics"].length() > 0,
                    rx.el.div(
                        rx.foreach(
                            checkin["key_topics"],
                            lambda topic: rx.el.span(
                                topic,
                                class_name="px-2 py-0.5 bg-white/5 rounded text-[10px] text-slate-400 mr-1",
                            ),
                        ),
                        class_name="mt-2 flex flex-wrap gap-1",
                    ),
                    rx.fragment(),
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start",
        ),
        rx.el.div(
            rx.cond(
                checkin["provider_reviewed"],
                rx.el.span(
                    "Reviewed",
                    class_name="px-2 py-1 rounded text-[10px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                ),
                rx.el.span(
                    "Pending",
                    class_name="px-2 py-1 rounded text-[10px] font-medium bg-amber-500/10 text-amber-300 border border-amber-500/20",
                ),
            ),
            class_name="ml-4",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
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
                on_click=PatientCheckinState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            rx.el.button(
                rx.icon("message-square", class_name="w-5 h-5 mr-2"),
                "Text Note",
                on_click=PatientCheckinState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_SECONDARY,
            ),
            class_name="flex gap-3 mb-6",
        ),
        # Summary Cards
        rx.el.div(
            rx.el.div(
                rx.icon("mic", class_name="w-6 h-6 text-teal-400 mb-2"),
                rx.el.p(
                    "This Week",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.span(
                    PatientCheckinState.checkins.length(),
                    class_name="text-2xl font-bold text-white",
                ),
                rx.el.span(" check-ins", class_name="text-sm text-slate-400 ml-1"),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            rx.el.div(
                rx.icon("clock", class_name="w-6 h-6 text-amber-400 mb-2"),
                rx.el.p(
                    "Pending Review",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.span(
                    PatientCheckinState.unreviewed_checkins_count,
                    class_name="text-2xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            class_name="grid grid-cols-2 gap-4 mb-6",
        ),
        # Check-ins List
        rx.el.div(
            rx.el.h3(
                "Recent Check-ins", class_name="text-lg font-semibold text-white mb-4"
            ),
            rx.el.div(
                rx.foreach(PatientCheckinState.checkins, checkin_card),
                class_name="space-y-4",
            ),
        ),
    )
