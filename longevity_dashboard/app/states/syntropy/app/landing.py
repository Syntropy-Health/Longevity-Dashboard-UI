"""Landing page state for Syntropy app."""

import os

import httpx
import reflex as rx

from ..base import ConfigurableState


class LandingState(ConfigurableState, rx.State):
    """Landing page state with configuration loading capabilities."""

    email: str = ""
    logo_tagline: str = "Where Wellness Meets Intelligence"
    landing_tagline: str = "Your AI-powered health companion"
    subscription_form_url: str = ""
    connect_form_url: str = ""
    presentation_url: str = ""
    is_submitting: bool = False
    chat_placeholder: str = "Ask me anything about your health..."
    preset_questions: list[dict[str, str]] = []

    @rx.event
    async def on_load(self):
        """Load dynamic content from admin config on page load."""
        config = await self.load_admin_config("syntropy_config")

        if config:
            self.logo_tagline = self.get_config_value(
                "app.content.branding.logo_tagline",
                self.logo_tagline
            )
            self.landing_tagline = self.get_config_value(
                "app.content.branding.tagline",
                self.landing_tagline
            )
            self.subscription_form_url = self.get_config_value(
                "app.content.landing.subscription_form_url",
                self.subscription_form_url
            )
            self.connect_form_url = self.get_config_value(
                "app.content.landing.connect_form_url",
                self.connect_form_url
            )
            self.presentation_url = self.get_config_value(
                "app.content.landing.presentation_url",
                self.presentation_url
            )
            self.chat_placeholder = self.get_config_value(
                "app.content.landing.chat_placeholder",
                self.chat_placeholder
            )

            preset_q = self.get_config_value("app.content.landing.preset_questions")
            if preset_q:
                self.preset_questions = preset_q

    @rx.event(background=True)
    async def subscribe(self, form_data: dict):
        async with self:
            self.is_submitting = True
            self.email = form_data.get("email", "")
        async with self:
            if "@" not in self.email:
                yield rx.toast.error("Please enter a valid email.")
                self.is_submitting = False
                return
        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            async with self:
                yield rx.toast.error("Subscription service unavailable.")
                self.is_submitting = False
            return
        url = "https://api.brevo.com/v3/contacts"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        }
        data = {"email": self.email, "updateEnabled": False}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
        async with self:
            if response.status_code in (200, 201):
                yield rx.toast.success("Thank you for subscribing!")
                self.email = ""
            elif response.status_code == 400:
                yield rx.toast.info("You're already subscribed!")
            else:
                yield rx.toast.error("Subscription failed. Please try again.")
            self.is_submitting = False
