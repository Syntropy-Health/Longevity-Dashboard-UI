"""Landing chat state for Syntropy landing page chat interactions."""

import os
from typing import Optional

import httpx
import reflex as rx

from ..base import ConfigurableState


class Message(rx.Base):
    """Chat message model."""
    text: str
    is_ai: bool


class LandingChatState(ConfigurableState, rx.State):
    """Chat state for landing page interactions."""

    messages: list[Message] = []
    typing: bool = False
    chat_model: str = "deepseek/deepseek-r1-0528-qwen3-8b:free"
    system_prompt: str = (
        "You are DietonAI, a friendly health and nutrition assistant. "
        "Provide helpful, concise responses about diet, nutrition, and wellness. "
        "Always recommend consulting healthcare professionals for medical advice."
    )
    mock_response: str = (
        "I'm DietonAI, your health assistant! I can help with nutrition questions, "
        "meal planning ideas, and general wellness tips. What would you like to know?"
    )
    use_mock: bool = False

    @rx.event
    async def on_load(self):
        """Load chat configuration on page load."""
        config = await self.load_admin_config("syntropy_config")
        if config:
            self.chat_model = self.get_config_value(
                "app.chat.model", self.chat_model
            )
            self.system_prompt = self.get_config_value(
                "app.chat.system_prompt", self.system_prompt
            )
            self.mock_response = self.get_config_value(
                "app.chat.mock_response", self.mock_response
            )
            self.use_mock = self.get_config_value(
                "app.chat.use_mock", self.use_mock
            )

    @rx.event
    async def send_message(self, form_data: dict):
        """Send a user message and generate AI response."""
        user_message = form_data.get("message", "").strip()
        if not user_message:
            return

        self.messages.append(Message(text=user_message, is_ai=False))
        self.typing = True
        yield

        yield LandingChatState.generate_response

    @rx.event(background=True)
    async def generate_response(self):
        """Generate AI response using OpenRouter or mock."""
        async with self:
            if not self.messages:
                self.typing = False
                return

        if self.use_mock:
            async with self:
                self.messages.append(Message(text=self.mock_response, is_ai=True))
                self.typing = False
            return

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            async with self:
                self.messages.append(
                    Message(text="AI service is currently unavailable.", is_ai=True)
                )
                self.typing = False
            return

        try:
            async with self:
                conversation = [{"role": "system", "content": self.system_prompt}]
                for msg in self.messages:
                    role = "assistant" if msg.is_ai else "user"
                    conversation.append({"role": role, "content": msg.text})

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": os.getenv("SITE_URL", "https://syntropyhealth.bio"),
                        "X-Title": os.getenv("SITE_NAME", "SyntropyHealthAI"),
                    },
                    json={
                        "model": self.chat_model,
                        "messages": conversation,
                    },
                )

            if response.status_code == 200:
                data = response.json()
                ai_message = data["choices"][0]["message"]["content"]
                async with self:
                    self.messages.append(Message(text=ai_message, is_ai=True))
            else:
                async with self:
                    self.messages.append(
                        Message(text="Sorry, I couldn't process that request.", is_ai=True)
                    )
        except Exception as e:
            async with self:
                self.messages.append(
                    Message(text=f"An error occurred: {str(e)}", is_ai=True)
                )
        finally:
            async with self:
                self.typing = False

    @rx.event
    def clear_chat(self):
        """Clear all messages."""
        self.messages = []
        self.typing = False
