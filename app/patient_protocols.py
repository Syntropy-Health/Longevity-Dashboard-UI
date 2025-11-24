import reflex as rx
from app.components.navbar import navbar
from app.states.protocol_state import ProtocolState
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles
from app.models import TreatmentProtocol


def protocol_card(protocol: TreatmentProtocol) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(protocol.name, class_name="text-xl font-bold text-white mb-1"),
                rx.el.span(
                    protocol.category,
                    class_name="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-500/10 text-teal-300 border border-teal-500/20 uppercase tracking-wide",
                ),
                class_name="mb-4",
            ),
            rx.el.p(
                protocol.description,
                class_name="text-slate-400 text-sm mb-6 h-10 line-clamp-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Duration",
                        class_name="text-xs text-slate-500 uppercase tracking-wider",
                    ),
                    rx.el.p(
                        protocol.duration,
                        class_name="text-sm text-slate-300 font-medium",
                    ),
                    class_name="",
                ),
                rx.el.div(
                    rx.el.p(
                        "Frequency",
                        class_name="text-xs text-slate-500 uppercase tracking-wider",
                    ),
                    rx.el.p(
                        protocol.frequency,
                        class_name="text-sm text-slate-300 font-medium",
                    ),
                    class_name="text-right",
                ),
                class_name="flex justify-between border-t border-white/10 pt-4 mb-6",
            ),
            rx.el.div(
                rx.el.p(
                    "Targets",
                    class_name="text-xs text-slate-500 uppercase tracking-wider mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        protocol.biomarker_targets,
                        lambda tag: rx.el.span(
                            tag,
                            class_name="px-2 py-1 bg-white/5 rounded text-xs text-slate-300 border border-white/5",
                        ),
                    ),
                    class_name="flex flex-wrap gap-2",
                ),
                class_name="mb-6",
            ),
            class_name="flex-1",
        ),
        rx.el.button(
            "Request Protocol",
            on_click=lambda: ProtocolState.open_request_modal(protocol),
            class_name="w-full mt-auto px-4 py-2 rounded-lg bg-white/5 hover:bg-teal-500/20 hover:text-teal-300 text-slate-300 border border-white/10 transition-all duration-200",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} h-full flex flex-col",
    )


def request_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    ProtocolState.selected_protocol,
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            f"Request {ProtocolState.selected_protocol.name}",
                            class_name="text-xl font-bold text-white mb-2",
                        ),
                        rx.radix.primitives.dialog.description(
                            "Please provide a reason for this protocol request. A clinician will review your profile.",
                            class_name="text-slate-400 mb-6 text-sm",
                        ),
                        rx.el.form(
                            rx.el.textarea(
                                name="reason",
                                placeholder="I am interested in this protocol because...",
                                required=True,
                                class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 mb-6 h-32 resize-none",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    on_click=ProtocolState.close_request_modal,
                                    class_name="px-4 py-2 text-slate-400 hover:text-white transition-colors mr-2",
                                ),
                                rx.el.button(
                                    "Submit Request",
                                    type="submit",
                                    class_name=GlassStyles.BUTTON_PRIMARY,
                                ),
                                class_name="flex justify-end items-center",
                            ),
                            on_submit=ProtocolState.submit_request,
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-md p-6 {GlassStyles.PANEL} z-50",
            ),
        ),
        open=ProtocolState.is_request_modal_open,
        on_open_change=ProtocolState.handle_request_modal_open_change,
    )


def patient_protocols_page() -> rx.Component:
    return rx.el.div(
        request_modal(),
        rx.el.div(
            rx.el.h1(
                "Available Treatments",
                class_name=f"text-3xl font-bold {GlassStyles.HEADING} mb-2",
            ),
            rx.el.p(
                "Explore longevity protocols tailored to optimize your biological age.",
                class_name="text-slate-400 mb-10",
            ),
            rx.el.div(
                rx.foreach(ProtocolState.protocols, protocol_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        ),
        class_name="max-w-7xl mx-auto",
    )