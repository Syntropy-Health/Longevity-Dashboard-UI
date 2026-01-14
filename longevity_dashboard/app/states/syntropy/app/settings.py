"""Settings state for Syntropy user preferences and integrations."""

from typing import Literal

import reflex as rx
from sqlmodel import select

from ....data.schemas.db.syntropy import SyntropySettings
from ...auth.base import AuthState


class SyntropySettingsState(rx.State):
    """Settings state for Syntropy app user preferences (order integrations, dietary)."""

    is_order_integration_open: bool = True
    is_dietary_preference_open: bool = True
    is_notifications_open: bool = True
    is_payment_open: bool = True
    partners: list[dict[str, str]] = [
        {"name": "Amazon", "key": "amazon", "logo": "/partners/amazon.svg"},
        {"name": "CookUnity", "key": "cookunity", "logo": "/partners/cookunity.svg"},
        {"name": "DoorDash", "key": "doordash", "logo": "/partners/doordash.svg"},
        {"name": "Instacart", "key": "instacart", "logo": "/partners/instacart.svg"},
        {"name": "Thrive Market", "key": "thrive_market", "logo": "/partners/thrive-market.svg"},
        {"name": "HelloFresh", "key": "hellofresh", "logo": "/partners/hello-fresh.svg"},
        {"name": "Blue Apron", "key": "blue_apron", "logo": "/partners/blue-apron.svg"},
        {"name": "Uber Eats", "key": "uber_eats", "logo": "/partners/uber-eats.svg"},
    ]
    order_integrations: dict[str, bool] = {
        "amazon": False,
        "cookunity": False,
        "doordash": False,
        "instacart": False,
        "thrive_market": False,
        "hellofresh": False,
        "blue_apron": False,
        "uber_eats": False,
    }
    include_herbal_supplement: bool = False
    frequency: int = 1
    aggressiveness: int = 0
    frequency_options: list[str] = ["low", "medium", "high"]
    aggressiveness_options: list[str] = ["gentle", "moderate", "assertive"]
    is_loading: bool = True
    show_coming_soon_dialog: bool = False
    coming_soon_feature_name: str = ""

    def set_show_coming_soon_dialog(self, value: bool):
        self.show_coming_soon_dialog = value

    @rx.event(background=True)
    async def load_settings(self):
        async with self:
            self.is_loading = True
        auth_s = await self.get_state(AuthState)
        if not auth_s or not auth_s.is_authenticated:
            async with self:
                self.is_loading = False
            return
        async with self:
            self.is_loading = False

    @rx.event(background=True)
    async def save_settings(self):
        auth_s = await self.get_state(AuthState)
        if not auth_s.is_authenticated:
            yield rx.toast.error("You must be logged in to save settings.")
            return
        with rx.session() as session:
            if not auth_s.is_authenticated or not auth_s.user:
                async with self:
                    self.is_loading = False
                return

            settings = session.exec(
                select(SyntropySettings).where(
                    SyntropySettings.user_id == auth_s.user_id
                )
            ).first()
            if settings:
                async with self:
                    settings.order_integrations = self.order_integrations
                    settings.include_herbal_supplement = self.include_herbal_supplement
                    settings.notification_frequency = self.frequency
                    settings.notification_aggressiveness = self.aggressiveness
                session.add(settings)
                session.commit()
                yield rx.toast.success("Settings saved successfully!")
            else:
                yield rx.toast.error("Could not find settings to update.")

    @rx.event
    def toggle_section(
        self,
        section: Literal["order", "dietary", "notifications", "payment"],
    ):
        if section == "order":
            self.is_order_integration_open = not self.is_order_integration_open
        elif section == "dietary":
            self.is_dietary_preference_open = not self.is_dietary_preference_open
        elif section == "notifications":
            self.is_notifications_open = not self.is_notifications_open
        elif section == "payment":
            self.is_payment_open = not self.is_payment_open

    @rx.event
    def toggle_integration(self, partner_key: str):
        is_currently_setup = self.order_integrations.get(partner_key, False)
        if not is_currently_setup:
            self.coming_soon_feature_name = partner_key.replace("_", " ").title()
            self.show_coming_soon_dialog = True
        else:
            self.order_integrations[partner_key] = False
            return SyntropySettingsState.save_settings

    @rx.event
    def toggle_herbal_supplement(self, value: bool):
        self.include_herbal_supplement = value
        return SyntropySettingsState.save_settings

    @rx.var
    def frequency_label(self) -> str:
        return self.frequency_options[self.frequency]

    @rx.var
    def aggressiveness_label(self) -> str:
        return self.aggressiveness_options[self.aggressiveness]

    @rx.event
    def handle_frequency_change(self, value: float | int):
        self.frequency = int(float(value))

    @rx.event
    def handle_aggressiveness_change(self, value: float | int):
        self.aggressiveness = int(float(value))

    @rx.event
    def save_notification_settings(self):
        return SyntropySettingsState.save_settings
