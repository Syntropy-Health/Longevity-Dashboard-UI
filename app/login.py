import reflex as rx
from app.states.auth_state import AuthState
from app.styles.glass_styles import GlassStyles


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="fixed top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-teal-900/20 via-slate-900/0 to-slate-900/0 pointer-events-none"
        ),
        rx.el.div(
            class_name="fixed bottom-0 left-0 w-[500px] h-[500px] bg-teal-500/5 rounded-full blur-[100px] pointer-events-none"
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-12 h-12 text-teal-400 mb-4 mx-auto"),
                rx.el.h1(
                    "Aether Longevity",
                    class_name=f"text-4xl font-bold text-center {GlassStyles.HEADING} mb-2",
                ),
                rx.el.p(
                    "Access your biological optimization portal.",
                    class_name="text-slate-400 text-center mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        "Patient Portal",
                        on_click=lambda: AuthState.set_login_mode("patient"),
                        class_name=rx.cond(
                            AuthState.login_mode == "patient",
                            "flex-1 py-2 text-sm font-medium rounded-lg bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
                            "flex-1 py-2 text-sm font-medium rounded-lg text-slate-500 hover:text-slate-300 transition-all",
                        ),
                    ),
                    rx.el.button(
                        "Clinician Portal",
                        on_click=lambda: AuthState.set_login_mode("admin"),
                        class_name=rx.cond(
                            AuthState.login_mode == "admin",
                            "flex-1 py-2 text-sm font-medium rounded-lg bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
                            "flex-1 py-2 text-sm font-medium rounded-lg text-slate-500 hover:text-slate-300 transition-all",
                        ),
                    ),
                    class_name="flex p-1 bg-slate-900/50 rounded-xl mb-8 border border-white/5",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            class_name="block text-xs uppercase text-slate-500 font-bold mb-2 tracking-wider",
                        ),
                        rx.el.input(
                            name="username",
                            placeholder="Enter username",
                            class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all",
                            default_value=AuthState.username,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-xs uppercase text-slate-500 font-bold mb-2 tracking-wider",
                        ),
                        rx.el.input(
                            name="password",
                            type="password",
                            placeholder="Enter password",
                            class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 transition-all",
                            default_value=AuthState.password,
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.icon("badge_alert", class_name="w-4 h-4 mr-2"),
                            AuthState.error_message,
                            class_name="flex items-center text-sm text-red-400 bg-red-400/10 border border-red-400/20 rounded-lg p-3 mb-6",
                        ),
                    ),
                    rx.el.button(
                        "Sign In",
                        type="submit",
                        class_name=f"w-full {GlassStyles.BUTTON_PRIMARY} py-3 flex justify-center items-center",
                    ),
                    on_submit=AuthState.login,
                ),
                rx.el.div(
                    rx.el.p(
                        "Demo Credentials:",
                        class_name="text-slate-600 text-xs font-medium uppercase mb-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Patient: patient / password",
                            class_name="text-slate-500 text-xs mr-4",
                        ),
                        rx.el.span(
                            "Clinician: admin / password",
                            class_name="text-slate-500 text-xs",
                        ),
                        class_name="flex justify-center",
                    ),
                    class_name="mt-8 text-center border-t border-white/5 pt-6",
                ),
                class_name=f"{GlassStyles.PANEL} p-8 md:p-10 w-full max-w-md relative z-10",
            ),
            class_name="min-h-screen flex items-center justify-center px-4",
        ),
        class_name=GlassStyles.PAGE_BG,
    )