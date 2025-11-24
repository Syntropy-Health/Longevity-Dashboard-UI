import reflex as rx
from app.components.navbar import navbar
from app.states.protocol_state import ProtocolState
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles
from app.models import TreatmentProtocol, ProtocolRequest
from app.enums import TreatmentCategory, TreatmentFrequency, _enum_values


def protocol_row(protocol: TreatmentProtocol) -> rx.Component:
    return rx.el.tr(
        rx.el.td(protocol.name, class_name="py-4 px-4 text-white font-medium"),
        rx.el.td(
            rx.el.span(
                protocol.category,
                class_name="px-2 py-1 rounded-full text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20 uppercase",
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(protocol.duration, class_name="py-4 px-4 text-slate-300"),
        rx.el.td(protocol.frequency, class_name="py-4 px-4 text-slate-300"),
        rx.el.td(
            rx.el.button(
                rx.icon(
                    "trash-2", class_name="w-4 h-4 text-red-400 hover:text-red-300"
                ),
                on_click=lambda: ProtocolState.delete_protocol(protocol.id),
                class_name="p-2 hover:bg-white/5 rounded-lg transition-colors",
            ),
            class_name="py-4 px-4 text-right",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors",
    )


def request_card(request: ProtocolRequest) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(request.patient_name, class_name="font-bold text-white"),
                rx.el.p(
                    f"Requested: {request.protocol_name}",
                    class_name="text-sm text-teal-400 mt-1",
                ),
            ),
            rx.el.span(request.date, class_name="text-xs text-slate-500"),
            class_name="flex justify-between items-start mb-3",
        ),
        rx.el.p(
            f"Reason: {request.reason}",
            class_name="text-sm text-slate-400 mb-4 bg-black/20 p-3 rounded-lg",
        ),
        rx.el.div(
            rx.el.button(
                "Reject",
                on_click=lambda: ProtocolState.reject_request(request.id),
                class_name="px-3 py-1.5 text-sm text-red-300 hover:bg-red-500/10 rounded-lg transition-colors border border-transparent hover:border-red-500/30",
            ),
            rx.el.button(
                "Approve",
                on_click=lambda: ProtocolState.approve_request(request.id),
                class_name="px-3 py-1.5 text-sm bg-teal-500/20 text-teal-300 hover:bg-teal-500/30 rounded-lg transition-colors border border-teal-500/30",
            ),
            class_name="flex justify-end gap-2",
        ),
        class_name="bg-white/5 border border-white/10 rounded-xl p-4",
    )


def add_protocol_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.el.span("+", class_name="mr-2 text-lg"),
                "New Protocol",
                class_name=GlassStyles.BUTTON_PRIMARY,
            )
        ),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Create Treatment Protocol",
                    class_name="text-xl font-bold text-white mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            name="name",
                            placeholder="Protocol Name",
                            required=True,
                            class_name="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 mb-4 text-white",
                        ),
                        rx.el.select(
                            rx.foreach(
                                _enum_values(TreatmentCategory),
                                lambda cat: rx.el.option(cat, value=cat),
                            ),
                            name="category",
                            class_name="w-full bg-slate-800 border border-white/10 rounded-lg px-4 py-2 mb-4 text-white",
                        ),
                        rx.el.textarea(
                            name="description",
                            placeholder="Description",
                            class_name="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 mb-4 text-white h-24",
                        ),
                        rx.el.div(
                            rx.el.input(
                                name="duration",
                                placeholder="Duration (e.g. 4 weeks)",
                                class_name="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    _enum_values(TreatmentFrequency),
                                    lambda freq: rx.el.option(freq, value=freq),
                                ),
                                name="frequency",
                                class_name="w-full bg-slate-800 border border-white/10 rounded-lg px-4 py-2 text-white",
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-4",
                        ),
                        rx.el.input(
                            name="biomarker_targets",
                            placeholder="Target Biomarkers (comma separated)",
                            class_name="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 mb-6 text-white",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    class_name="px-4 py-2 text-slate-400 hover:text-white transition-colors",
                                )
                            ),
                            rx.el.button(
                                "Create Protocol",
                                type="submit",
                                class_name=GlassStyles.BUTTON_PRIMARY,
                            ),
                            class_name="flex justify-end gap-2",
                        ),
                    ),
                    on_submit=ProtocolState.add_protocol,
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-lg p-6 {GlassStyles.PANEL} z-50",
            ),
        ),
        open=ProtocolState.is_add_modal_open,
        on_open_change=ProtocolState.handle_add_modal_open_change,
    )


def admin_protocols_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Protocol Management",
                class_name=f"text-3xl font-bold {GlassStyles.HEADING}",
            ),
            add_protocol_modal(),
            class_name="flex justify-between items-center mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Active Protocols",
                    class_name="text-lg font-semibold text-white mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Name",
                                    class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                                ),
                                rx.el.th(
                                    "Category",
                                    class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                                ),
                                rx.el.th(
                                    "Duration",
                                    class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                                ),
                                rx.el.th(
                                    "Frequency",
                                    class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="text-right py-3 px-4 text-slate-400 font-medium text-sm",
                                ),
                            ),
                            class_name="border-b border-white/10",
                        ),
                        rx.el.tbody(rx.foreach(ProtocolState.protocols, protocol_row)),
                        class_name="w-full",
                    ),
                    class_name=f"{GlassStyles.PANEL} overflow-hidden",
                ),
                class_name="col-span-1 lg:col-span-3",
            ),
            rx.el.div(
                rx.el.h2(
                    "Pending Requests",
                    class_name="text-lg font-semibold text-white mb-4",
                ),
                rx.el.div(
                    rx.cond(
                        ProtocolState.pending_requests,
                        rx.foreach(ProtocolState.pending_requests, request_card),
                        rx.el.div(
                            rx.el.p(
                                "No pending requests.",
                                class_name="text-slate-500 text-center italic",
                            )
                        ),
                    ),
                    class_name="space-y-4",
                ),
                class_name="col-span-1 lg:col-span-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-4 gap-8",
        ),
        class_name="max-w-7xl mx-auto",
    )