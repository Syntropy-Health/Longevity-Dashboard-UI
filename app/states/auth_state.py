import reflex as rx
from app.states.global_state import GlobalState


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""
    login_mode: str = "patient"

    @rx.event
    def set_login_mode(self, mode: str):
        self.login_mode = mode
        self.error_message = ""
        self.username = ""
        self.password = ""

    @rx.event
    async def login(self, form_data: dict):
        """
        Handle login logic based on mode and dummy credentials.
        """
        self.username = form_data.get("username", "")
        self.password = form_data.get("password", "")
        if self.login_mode == "patient":
            if self.username.lower() == "patient" and self.password == "password":
                self.error_message = ""
                state = await self.get_state(GlobalState)
                state.set_role_patient()
                return rx.redirect("/")
            else:
                self.error_message = "Invalid Patient credentials."
        elif self.login_mode == "admin":
            if self.username.lower() == "admin" and self.password == "password":
                self.error_message = ""
                state = await self.get_state(GlobalState)
                state.set_role_admin()
                return rx.redirect("/")
            else:
                self.error_message = "Invalid Clinician credentials."