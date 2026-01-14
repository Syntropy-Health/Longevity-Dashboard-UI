import reflex as rx

# Pages - Admin
from .app.pages.admin import (
    admin_chat_page,
    admin_dashboard,
    patient_health_page,
    treatments_page,
)

# Pages - Patient
from .app.pages.patient import (
    ai_chat_page,
    analytics_page,
    checkins_page,
    checkins_page_wrapper,
    patient_portal,
    settings_page,
    treatment_search_page,
)

# Pages - Shared
from .app.pages.shared import (
    appointments_page,
    auth_page,
    notifications_page,
    register_page,
)

# States
from .app.states import (
    AppointmentState,
    BiomarkerState,
    CheckinState,
    ConditionState,
    DataSourceState,
    FoodState,
    MedicationState,
    NotificationState,
    SymptomState,
    TreatmentSearchState,
    TreatmentState,
)

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
            rel="stylesheet",
        ),
    ],
    # stylesheets=[
    #     "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    #     "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
    # ],
)
app.add_page(auth_page, route="/")
app.add_page(auth_page, route="/login")
app.add_page(register_page, route="/register")

# Admin
app.add_page(admin_dashboard, route="/admin/dashboard")
app.add_page(patient_health_page, route="/admin/patient-health")
app.add_page(
    checkins_page,
    route="/admin/checkins",
    on_load=[CheckinState.load_admin_checkins],
)
app.add_page(
    treatments_page,
    route="/admin/treatments",
    on_load=[TreatmentState.load_protocols],
)
app.add_page(admin_chat_page, route="/admin/chat", title="AI Medical Expert")

# Patient - Load decomposed dashboard states
app.add_page(
    patient_portal,
    route="/patient/portal",
    on_load=[
        BiomarkerState.load_biomarkers,
        FoodState.load_food_data,
        MedicationState.load_medication_data,
        ConditionState.load_condition_data,
        SymptomState.load_symptom_data,
        DataSourceState.load_data_source_data,
        NotificationState.load_medication_notifications,
        AppointmentState.load_appointments,
    ],
)
app.add_page(
    checkins_page_wrapper,
    route="/patient/checkins",
    on_load=[
        BiomarkerState.load_biomarkers,
        FoodState.load_food_data,
        MedicationState.load_medication_data,
        ConditionState.load_condition_data,
        SymptomState.load_symptom_data,
        DataSourceState.load_data_source_data,
        NotificationState.load_medication_notifications,
        CheckinState.start_periodic_call_logs_refresh,
    ],
)
app.add_page(settings_page, route="/patient/settings")
app.add_page(analytics_page, route="/patient/analytics")
app.add_page(ai_chat_page, route="/patient/chat", title="AI Clinician")
app.add_page(
    treatment_search_page,
    route="/patient/treatment-search",
    on_load=[TreatmentSearchState.load_treatments],
)

# Shared
app.add_page(
    notifications_page, route="/notifications", title="Notifications - Longevity Clinic"
)
app.add_page(
    appointments_page,
    route="/appointments",
    title="Appointments | Longevity Clinic",
    on_load=[AppointmentState.load_appointments],
)
