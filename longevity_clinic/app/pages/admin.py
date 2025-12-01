import reflex as rx
from ..components.layout import authenticated_layout
from ..components.page_components import section_header
from ..states.auth_state import AuthState
from ..states.patient_state import PatientState, Patient
from ..components.charts import (
    overview_trend_chart,
    treatment_distribution_chart,
    biomarker_improvement_chart,
)
from ..styles import styles, GlassStyles
from ..config import current_config


# Admin state for tab management
class AdminDashboardState(rx.State):
    """State for admin dashboard tab management."""
    active_tab: str = "overview"
    
    def set_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab


def stat_card(
    title: str, value: str, trend: str, trend_up: bool, icon: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500 truncate"),
                rx.el.p(
                    value,
                    class_name="mt-1 text-3xl font-bold text-gray-800 tracking-tight",
                ),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-teal-600"),
                class_name="p-3 bg-teal-50/50 rounded-2xl border border-teal-100/50",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                trend,
                class_name=rx.cond(
                    trend_up,
                    "text-teal-600 text-sm font-medium",
                    "text-red-600 text-sm font-medium",
                ),
            ),
            rx.el.span(" from last month", class_name="text-sm text-gray-500 ml-2"),
            class_name="mt-4",
        ),
        class_name=f"{GlassStyles.STAT_CARD_LIGHT} {current_config.glass_card_hover}",
    )


def efficiency_stat_card(
    title: str, value: str, subtitle: str, icon: str, color: str = "teal"
) -> rx.Component:
    """Stat card for clinical efficiency metrics."""
    color_classes = {
        "teal": "text-teal-600 bg-teal-50/50 border-teal-100/50",
        "blue": "text-blue-600 bg-blue-50/50 border-blue-100/50",
        "purple": "text-purple-600 bg-purple-50/50 border-purple-100/50",
        "amber": "text-amber-600 bg-amber-50/50 border-amber-100/50",
        "emerald": "text-emerald-600 bg-emerald-50/50 border-emerald-100/50",
    }
    
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 {color_classes.get(color, color_classes['teal']).split()[0]}"),
            class_name=f"p-2.5 rounded-xl border {color_classes.get(color, color_classes['teal'])}",
        ),
        rx.el.div(
            rx.el.p(
                value,
                class_name="text-2xl font-bold text-gray-800 mt-3",
            ),
            rx.el.p(title, class_name="text-sm font-medium text-gray-700 mt-1"),
            rx.el.p(subtitle, class_name="text-xs text-gray-500 mt-0.5"),
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-4 hover:shadow-md transition-all",
    )


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-800 mb-6"),
        rx.el.div(chart, class_name="w-full h-64"),
        class_name=f"{current_config.glass_panel_style} p-6 rounded-2xl",
    )


def efficiency_chart_placeholder(title: str, description: str) -> rx.Component:
    """Placeholder for efficiency charts."""
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-500 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    lambda day: rx.el.div(
                        rx.el.div(
                            class_name="w-full bg-gradient-to-t from-teal-500 to-teal-300 rounded-t",
                            style={"height": f"{60 + (hash(day) % 40)}%"}
                        ),
                        rx.el.span(day, class_name="text-xs text-gray-500 mt-2"),
                        class_name="flex flex-col items-center justify-end h-40 w-1/5",
                    ),
                ),
                class_name="flex items-end justify-between h-48 px-4",
            ),
            class_name="bg-gray-50/50 rounded-xl p-4",
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
    )


def patient_table_row(patient: Patient) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span("P", class_name="text-xs font-bold text-teal-700"),
                    class_name="w-8 h-8 rounded-full bg-teal-100 flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        patient["full_name"],
                        class_name="text-sm font-medium text-gray-900",
                    ),
                    rx.el.p(
                        patient["email"], class_name="text-xs text-gray-500 truncate"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["age"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["last_visit"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                patient["status"],
                class_name=rx.cond(
                    patient["status"] == "Active",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-teal-100 text-teal-800",
                    rx.cond(
                        patient["status"] == "Inactive",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800",
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-2 rounded-full bg-teal-500",
                    style={"width": f"{patient['biomarker_score']}%%"},
                ),
                class_name="w-20 h-2 bg-gray-200 rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: PatientState.open_view_patient(patient),
                class_name="text-teal-600 hover:text-teal-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def patient_management_section() -> rx.Component:
    return rx.el.div(
        section_header(
            title="Patient Management",
            button_text="Add Patient",
            button_icon="plus",
            button_onclick=PatientState.open_add_patient,
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-5 h-5 text-gray-400 absolute left-3"),
                rx.el.input(
                    placeholder="Search patients...",
                    on_change=PatientState.set_search_query,
                    class_name=f"pl-10 block w-full {current_config.glass_input_style} sm:text-sm py-2",
                    default_value=PatientState.search_query,
                ),
                class_name="relative flex-1 max-w-xs mr-4",
            ),
            rx.el.select(
                rx.el.option("All Statuses", value="All"),
                rx.el.option("Active", value="Active"),
                rx.el.option("Inactive", value="Inactive"),
                rx.el.option("Onboarding", value="Onboarding"),
                value=PatientState.status_filter,
                on_change=PatientState.set_status_filter,
                class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm mr-4",
            ),
            rx.el.select(
                rx.el.option("Sort by Name", value="name"),
                rx.el.option("Recent Visit", value="recent"),
                rx.el.option("Biomarker Score", value="score"),
                value=PatientState.sort_key,
                on_change=PatientState.set_sort_key,
                class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm",
            ),
            class_name="flex flex-wrap items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Patient",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Age",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Last Visit",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Wellness Score",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            rx.el.span("Actions", class_name="sr-only"),
                            class_name="px-6 py-3 relative",
                        ),
                    ),
                    class_name="bg-gray-50/30 backdrop-blur-sm",
                ),
                rx.el.tbody(
                    rx.foreach(PatientState.filtered_patients, patient_table_row),
                    class_name="bg-white/20 divide-y divide-gray-100/50",
                ),
                class_name="min-w-full divide-y divide-gray-200/50",
            ),
            class_name="shadow-sm overflow-hidden border border-white/50 sm:rounded-2xl overflow-x-auto",
        ),
        class_name=f"{current_config.glass_panel_style} p-6",
    )


def add_patient_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "New Patient Intake",
                            class_name=GlassStyles.MODAL_TITLE,
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name=GlassStyles.CLOSE_BUTTON,
                            )
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    # Form fields
                    rx.el.div(
                        # Name and Email row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Full Name", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="text",
                                    value=PatientState.new_patient_name,
                                    on_change=PatientState.set_new_patient_name,
                                    placeholder="Enter patient name",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Email Address", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="email",
                                    value=PatientState.new_patient_email,
                                    on_change=PatientState.set_new_patient_email,
                                    placeholder="email@example.com",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-4",
                        ),
                        # Phone, Age, Gender row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Phone Number", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="tel",
                                    value=PatientState.new_patient_phone,
                                    on_change=PatientState.set_new_patient_phone,
                                    placeholder="(555) 123-4567",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Age", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="number",
                                    value=PatientState.new_patient_age,
                                    on_change=PatientState.set_new_patient_age,
                                    placeholder="30",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Gender", class_name=GlassStyles.LABEL),
                                rx.el.select(
                                    rx.el.option("Select...", value=""),
                                    rx.el.option("Male", value="Male"),
                                    rx.el.option("Female", value="Female"),
                                    rx.el.option("Other", value="Other"),
                                    value=PatientState.new_patient_gender,
                                    on_change=PatientState.set_new_patient_gender,
                                    class_name=GlassStyles.MODAL_SELECT,
                                ),
                            ),
                            class_name="grid grid-cols-3 gap-4 mb-4",
                        ),
                        # Medical History
                        rx.el.div(
                            rx.el.label("Medical History Summary", class_name=GlassStyles.LABEL),
                            rx.el.textarea(
                                rows="3",
                                value=PatientState.new_patient_history,
                                on_change=PatientState.set_new_patient_history,
                                placeholder="Enter relevant medical history...",
                                class_name=GlassStyles.MODAL_TEXTAREA,
                            ),
                            class_name="mb-4",
                        ),
                    ),
                    # Footer buttons
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            )
                        ),
                        rx.el.button(
                            "Create Patient Profile",
                            on_click=PatientState.add_patient,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name=GlassStyles.MODAL_FOOTER,
                    ),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_LG} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=PatientState.is_add_patient_open,
        on_open_change=PatientState.handle_add_patient_open_change,
    )


def view_patient_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    PatientState.selected_patient,
                    rx.el.div(
                        # Header
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Patient Profile",
                                class_name=GlassStyles.MODAL_TITLE,
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    rx.icon("x", class_name="w-5 h-5"),
                                    class_name=GlassStyles.CLOSE_BUTTON,
                                )
                            ),
                            class_name="flex justify-between items-center mb-6",
                        ),
                        # Patient avatar and name
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "P",
                                    class_name="text-2xl font-bold text-teal-700",
                                ),
                                class_name="h-16 w-16 rounded-full bg-teal-100 flex items-center justify-center mb-4 mx-auto",
                            ),
                            rx.el.h4(
                                PatientState.selected_patient["full_name"],
                                class_name="text-xl font-bold text-gray-900 text-center",
                            ),
                            rx.el.p(
                                PatientState.selected_patient["status"],
                                class_name="text-sm text-center text-teal-600 font-medium mt-1",
                            ),
                            class_name="mb-6",
                        ),
                        # Contact and Medical info
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Contact Information",
                                    class_name="font-semibold text-gray-900 mb-2",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "mail", class_name="w-4 h-4 text-gray-400 mr-2"
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["email"],
                                        class_name="text-sm text-gray-600",
                                    ),
                                    class_name="flex items-center mb-1",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "phone", class_name="w-4 h-4 text-gray-400 mr-2"
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["phone"],
                                        class_name="text-sm text-gray-600",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Medical Details",
                                    class_name="font-semibold text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    f"Age: {PatientState.selected_patient['age']} • Gender: {PatientState.selected_patient['gender']}",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                rx.el.p(
                                    f"History: {PatientState.selected_patient['medical_history']}",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="mb-4",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-teal-50/50 p-4 rounded-xl border border-teal-100/50",
                        ),
                        # Assigned Treatments section
                        rx.el.div(
                            rx.el.h4(
                                "Assigned Treatments",
                                class_name="text-md font-semibold text-gray-900 mb-3 mt-2",
                            ),
                            rx.cond(
                                PatientState.selected_patient["assigned_treatments"].length() > 0,
                                rx.el.div(
                                    rx.foreach(
                                        PatientState.selected_patient["assigned_treatments"],
                                        lambda t: rx.el.div(
                                            rx.el.div(
                                                rx.el.p(
                                                    t["name"],
                                                    class_name="font-medium text-gray-900 text-sm",
                                                ),
                                                rx.el.p(
                                                    f"{t['frequency']} • {t['duration']}",
                                                    class_name="text-xs text-gray-500",
                                                ),
                                            ),
                                            rx.el.button(
                                                rx.icon(
                                                    "trash-2",
                                                    class_name="w-4 h-4 text-red-400",
                                                ),
                                                on_click=lambda: PatientState.remove_treatment_from_patient(
                                                    PatientState.selected_patient["id"],
                                                    t["id"],
                                                ),
                                                class_name="p-1 hover:bg-red-50 rounded-full transition-colors",
                                            ),
                                            class_name="flex justify-between items-center p-3 bg-white border border-teal-100/50 rounded-xl shadow-sm",
                                        ),
                                    ),
                                    class_name="space-y-2",
                                ),
                                rx.el.p(
                                    "No active treatments assigned.",
                                    class_name="text-sm text-gray-500 italic",
                                ),
                            ),
                            class_name="bg-teal-50/30 p-4 rounded-xl border border-teal-100/30 mt-4",
                        ),
                        # Footer
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Close",
                                    class_name=f"w-full {GlassStyles.BUTTON_SECONDARY}",
                                )
                            ),
                            class_name="mt-6",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_LG} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=PatientState.is_view_patient_open,
        on_open_change=PatientState.handle_view_patient_open_change,
    )


def dashboard_tabs() -> rx.Component:
    """Dashboard tab navigation."""
    return rx.el.div(
        rx.el.button(
            rx.icon("layout-dashboard", class_name="w-4 h-4 mr-2"),
            "Overview",
            on_click=lambda: AdminDashboardState.set_tab("overview"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "overview",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        rx.el.button(
            rx.icon("users", class_name="w-4 h-4 mr-2"),
            "Patients",
            on_click=lambda: AdminDashboardState.set_tab("patients"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "patients",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        rx.el.button(
            rx.icon("gauge", class_name="w-4 h-4 mr-2"),
            "Clinical Efficiency",
            on_click=lambda: AdminDashboardState.set_tab("efficiency"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "efficiency",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        class_name=f"{GlassStyles.TAB_LIST_LIGHT} mb-6",
    )


def overview_tab() -> rx.Component:
    """Overview dashboard tab content."""
    return rx.el.div(
        # Stats row
        rx.el.div(
            stat_card("Total Patients", "1,284", "+12%", True, "users"),
            stat_card("Active Protocols", "42", "+4%", True, "activity"),
            stat_card("Appointments Today", "18", "-2%", False, "calendar"),
            stat_card("Avg. Appt. Duration", "45min", "+8%", True, "clock"),
            class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8",
        ),
        # Charts row
        rx.el.div(
            chart_card("Patient Growth Trends", overview_trend_chart()),
            chart_card("Treatment Protocol Distribution", treatment_distribution_chart()),
            chart_card("Avg. Biomarker Improvements", biomarker_improvement_chart()),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
    )


def efficiency_tab() -> rx.Component:
    """Clinical efficiency dashboard tab content."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h2(
                "Clinical Operational Efficiency",
                class_name=f"text-xl {GlassStyles.HEADING_LIGHT}",
            ),
            rx.el.p(
                "Monitor and optimize clinic performance metrics",
                class_name=GlassStyles.SUBHEADING_LIGHT,
            ),
            class_name="mb-6",
        ),
        
        # Key metrics row
        rx.el.div(
            efficiency_stat_card(
                "Patient Throughput",
                "24.5",
                "patients/day this week",
                "users",
                "teal"
            ),
            efficiency_stat_card(
                "Avg Wait Time",
                "12 min",
                "8% improvement from last week",
                "clock",
                "blue"
            ),
            efficiency_stat_card(
                "Room Utilization",
                "87%",
                "across all treatment rooms",
                "door-open",
                "purple"
            ),
            efficiency_stat_card(
                "Staff Efficiency",
                "94%",
                "appointments on schedule",
                "user-check",
                "emerald"
            ),
            efficiency_stat_card(
                "Treatment Completion",
                "96.2%",
                "protocols completed successfully",
                "circle-check",
                "teal"
            ),
            efficiency_stat_card(
                "Revenue/Hour",
                "$847",
                "+12% from last month",
                "dollar-sign",
                "amber"
            ),
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8",
        ),
        
        # Charts row
        rx.el.div(
            efficiency_chart_placeholder(
                "Daily Patient Flow",
                "Appointment volume and wait times throughout the day"
            ),
            efficiency_chart_placeholder(
                "Treatment Room Utilization",
                "Room occupancy rates by time slot"
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
        ),
        
        # Additional metrics
        rx.el.div(
            rx.el.div(
                rx.el.h3("Provider Performance", class_name="text-lg font-bold text-gray-800 mb-4"),
                rx.el.div(
                    rx.foreach(
                        [
                            {"name": "Dr. Johnson", "patients": 156, "efficiency": 98},
                            {"name": "Dr. Chen", "patients": 142, "efficiency": 95},
                            {"name": "Dr. Patel", "patients": 138, "efficiency": 97},
                            {"name": "Dr. Williams", "patients": 128, "efficiency": 92},
                        ],
                        lambda p: rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span("D", class_name="text-sm font-bold text-teal-600"),
                                    class_name="w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center",
                                ),
                                rx.el.div(
                                    rx.el.p(p["name"], class_name="font-medium text-gray-900"),
                                    rx.el.p(
                                        f"{p['patients']} patients this month",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="ml-3",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        class_name="h-2 rounded-full bg-teal-500",
                                        style={"width": f"{p['efficiency']}%"},
                                    ),
                                    class_name="flex-1 h-2 bg-gray-200 rounded-full mr-3",
                                ),
                                rx.el.span(
                                    f"{p['efficiency']}%",
                                    class_name="text-sm font-medium text-gray-700",
                                ),
                                class_name="flex items-center w-32",
                            ),
                            class_name="flex items-center justify-between py-3",
                        ),
                    ),
                    class_name="divide-y divide-gray-100",
                ),
                class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
            ),
            rx.el.div(
                rx.el.h3("Treatment Completion Rates", class_name="text-lg font-bold text-gray-800 mb-4"),
                rx.el.div(
                    rx.foreach(
                        [
                            {"treatment": "NAD+ IV Therapy", "rate": 98, "color": "teal"},
                            {"treatment": "HBOT Sessions", "rate": 95, "color": "blue"},
                            {"treatment": "Stem Cell", "rate": 92, "color": "purple"},
                            {"treatment": "Peptide Therapy", "rate": 97, "color": "emerald"},
                        ],
                        lambda t: rx.el.div(
                            rx.el.div(
                                rx.el.p(t["treatment"], class_name="font-medium text-gray-900"),
                                rx.el.div(
                                    rx.el.div(
                                        class_name=f"h-3 rounded-full bg-{t['color']}-500",
                                        style={"width": f"{t['rate']}%"},
                                    ),
                                    class_name="flex-1 h-3 bg-gray-200 rounded-full mt-2",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.span(
                                f"{t['rate']}%",
                                class_name="text-lg font-bold text-gray-800 ml-4",
                            ),
                            class_name="flex items-center py-3",
                        ),
                    ),
                    class_name="divide-y divide-gray-100",
                ),
                class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
    )


def admin_dashboard() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.h1(
                "Dashboard", class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-6"
            ),
            
            # Tab navigation
            dashboard_tabs(),
            
            # Tab content
            rx.match(
                AdminDashboardState.active_tab,
                ("overview", overview_tab()),
                ("patients", rx.el.div(
                    patient_management_section(),
                    add_patient_modal(),
                    view_patient_modal(),
                )),
                ("efficiency", efficiency_tab()),
                overview_tab(),  # Default
            ),
        )
    )