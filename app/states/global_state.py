import reflex as rx
from app.config import settings


class GlobalState(rx.State):
    """
    Manages global application state, specifically role-based access and user session.
    """

    current_role: str = "guest"
    user_name: str = "Guest User"
    is_role_selector_open: bool = False

    @rx.var
    def is_admin(self) -> bool:
        return self.current_role == "admin"

    @rx.var
    def is_patient(self) -> bool:
        return self.current_role == "patient"

    @rx.var
    def clinic_name(self) -> str:
        return settings.clinic_name

    @rx.var
    def role_display_name(self) -> str:
        return self.current_role.capitalize()

    @rx.event
    def set_role_admin(self):
        self.current_role = "admin"
        self.user_name = "Dr. Alistair Vance"
        self.is_role_selector_open = False
        return rx.toast("Welcome, Dr. Vance", position="top-center")

    @rx.event
    def set_role_patient(self):
        self.current_role = "patient"
        self.user_name = "Elena Fisher"
        self.is_role_selector_open = False
        return rx.toast("Welcome, Elena", position="top-center")

    @rx.event
    def open_role_selector(self):
        self.is_role_selector_open = True

    @rx.event
    def close_role_selector(self):
        if self.current_role != "guest":
            self.is_role_selector_open = False
        else:
            return rx.toast("Please login to continue.", position="top-center")

    @rx.event
    def handle_role_selector_open_change(self, is_open: bool):
        if not is_open:
            self.close_role_selector()

    @rx.event
    def logout(self):
        self.current_role = "guest"
        self.user_name = "Guest"
        self.is_role_selector_open = False
        return rx.redirect("/login")

    @rx.event
    def check_auth(self):
        """Redirect to login if not authenticated."""
        if self.current_role == "guest":
            return rx.redirect("/login")