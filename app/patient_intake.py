import reflex as rx
from app.components.navbar import navbar
from app.states.patient_state import PatientState
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles


def form_field(
    label: str,
    name: str,
    type: str = "text",
    placeholder: str = "",
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-300 mb-2"),
        rx.el.input(
            type=type,
            name=name,
            placeholder=placeholder,
            required=required,
            class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all",
        ),
        class_name="mb-6",
    )


def form_textarea(label: str, name: str, placeholder: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-300 mb-2"),
        rx.el.textarea(
            name=name,
            placeholder=placeholder,
            class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all h-32 resize-none",
        ),
        class_name="mb-6",
    )


def form_select(label: str, name: str, options: list[tuple[str, str]]) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-slate-300 mb-2"),
        rx.el.select(
            rx.foreach(options, lambda opt: rx.el.option(opt[0], value=opt[1])),
            name=name,
            class_name="w-full bg-slate-800 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all",
        ),
        class_name="mb-6",
    )


def patient_intake_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Patient Intake Assessment",
                class_name=f"text-3xl font-bold {GlassStyles.HEADING} mb-2",
            ),
            rx.el.p(
                "Complete your biological profile to generate personalized longevity protocols.",
                class_name="text-slate-400 mb-8",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Personal Demographics",
                            class_name="text-xl font-semibold text-white mb-6 flex items-center gap-2",
                        ),
                        rx.el.div(
                            form_field(
                                "Date of Birth", "dob", type="date", required=True
                            ),
                            form_select(
                                "Gender",
                                "gender",
                                [
                                    ("Select Gender", ""),
                                    ("Male", "male"),
                                    ("Female", "female"),
                                    ("Other", "other"),
                                ],
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                        ),
                        rx.el.div(
                            form_field(
                                "Email Address", "email", type="email", required=True
                            ),
                            form_field("Phone Number", "phone", type="tel"),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                        ),
                        class_name="mb-10",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Medical History",
                            class_name="text-xl font-semibold text-white mb-6",
                        ),
                        form_textarea(
                            "Current Medications & Supplements",
                            "medications",
                            "List all current prescriptions and supplements...",
                        ),
                        form_textarea(
                            "Known Allergies",
                            "allergies",
                            "List any drug or food allergies...",
                        ),
                        form_textarea(
                            "Medical Conditions",
                            "medical_history",
                            "Describe any diagnosed medical conditions...",
                        ),
                        class_name="mb-10",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Lifestyle Factors",
                            class_name="text-xl font-semibold text-white mb-6",
                        ),
                        rx.el.div(
                            form_select(
                                "Exercise Frequency",
                                "exercise_freq",
                                [
                                    ("Sedentary", "sedentary"),
                                    ("1-2x/week", "light"),
                                    ("3-4x/week", "moderate"),
                                    ("5+x/week", "active"),
                                ],
                            ),
                            form_select(
                                "Diet Type",
                                "diet_type",
                                [
                                    ("Standard", "standard"),
                                    ("Keto", "keto"),
                                    ("Paleo", "paleo"),
                                    ("Vegan", "vegan"),
                                    ("Mediterranean", "mediterranean"),
                                ],
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                        ),
                        rx.el.div(
                            form_field(
                                "Average Sleep (Hours)", "sleep_hours", type="number"
                            ),
                            form_select(
                                "Stress Level (1-10)",
                                "stress_level",
                                [(str(i), str(i)) for i in range(1, 11)],
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                        ),
                        class_name="mb-10",
                    ),
                ),
                rx.el.button(
                    "Submit Health Profile",
                    type="submit",
                    class_name=f"{GlassStyles.BUTTON_PRIMARY} w-full md:w-auto",
                ),
                on_submit=PatientState.submit_intake,
                reset_on_submit=True,
            ),
            class_name=f"{GlassStyles.PANEL} p-8 max-w-4xl mx-auto",
        ),
        class_name="max-w-4xl mx-auto",
    )