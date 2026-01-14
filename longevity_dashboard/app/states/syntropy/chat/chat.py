"""Main chat state for Syntropy AI chat sessions."""

import os
from typing import Optional

import httpx
import reflex as rx
from sqlmodel import select

from ....data.schemas.db.syntropy import ChatMessage, ChatSession
from ...auth.base import AuthState
from ..base import ConfigurableState


class SyntropyChatState(ConfigurableState, rx.State):
    """Main chat state managing chat sessions and messages."""

    AIName: str = "DietonAI"
    sessions: list[dict] = []
    active_session: Optional[dict] = None
    active_session_id: Optional[str] = None
    active_session_messages: list[dict] = []
    is_loading_sessions: bool = True
    streaming_response: str = ""
    is_streaming: bool = False
    user_input_text: str = ""
    sidebar_collapsed: bool = False
    typing_user_input: str = ""

    chat_model: str = "deepseek/deepseek-r1-0528-qwen3-8b:free"
    system_prompt: str = (
        "You are DietonAI, a knowledgeable health and nutrition assistant. "
        "Provide helpful, accurate information about diet, nutrition, and wellness. "
        "Always recommend consulting healthcare professionals for medical advice."
    )

    @rx.event
    async def on_load(self):
        """Load chat configuration and sessions on page load."""
        config = await self.load_admin_config("syntropy_config")
        if config:
            self.AIName = self.get_config_value("app.chat.ai_name", self.AIName)
            self.chat_model = self.get_config_value("app.chat.model", self.chat_model)
            self.system_prompt = self.get_config_value(
                "app.chat.system_prompt", self.system_prompt
            )
        return SyntropyChatState.load_sessions

    @rx.event(background=True)
    async def load_sessions(self):
        """Load chat sessions for the current user."""
        async with self:
            self.is_loading_sessions = True

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or not auth_state.user_id:
            async with self:
                self.is_loading_sessions = False
                self.sessions = []
            return

        try:
            with rx.session() as session:
                stmt = select(ChatSession).where(
                    ChatSession.user_id == auth_state.user_id
                ).order_by(ChatSession.updated_at.desc())
                db_sessions = session.exec(stmt).all()

                async with self:
                    self.sessions = [
                        {
                            "id": str(s.id),
                            "title": s.title or "New Chat",
                            "created_at": s.created_at.isoformat() if s.created_at else "",
                            "updated_at": s.updated_at.isoformat() if s.updated_at else "",
                        }
                        for s in db_sessions
                    ]

                    if self.sessions and not self.active_session_id:
                        self.active_session_id = self.sessions[0]["id"]
                        self.active_session = self.sessions[0]

        except Exception as e:
            print(f"Error loading sessions: {e}")
            async with self:
                self.sessions = []
        finally:
            async with self:
                self.is_loading_sessions = False

        if self.active_session_id:
            yield SyntropyChatState.load_messages

    @rx.event(background=True)
    async def load_messages(self):
        """Load messages for the active session."""
        async with self:
            if not self.active_session_id:
                self.active_session_messages = []
                return

        try:
            with rx.session() as session:
                stmt = select(ChatMessage).where(
                    ChatMessage.session_id == self.active_session_id
                ).order_by(ChatMessage.created_at.asc())
                db_messages = session.exec(stmt).all()

                async with self:
                    self.active_session_messages = [
                        {
                            "id": str(m.id),
                            "content": m.content,
                            "is_ai": m.sender == "ai",
                            "created_at": m.created_at.isoformat() if m.created_at else "",
                        }
                        for m in db_messages
                    ]
        except Exception as e:
            print(f"Error loading messages: {e}")
            async with self:
                self.active_session_messages = []

    @rx.event
    def select_session(self, session_id: str):
        """Select a chat session."""
        self.active_session_id = session_id
        for s in self.sessions:
            if s["id"] == session_id:
                self.active_session = s
                break
        self.streaming_response = ""
        return SyntropyChatState.load_messages

    @rx.event
    async def create_new_session(self):
        """Create a new chat session."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or not auth_state.user_id:
            yield rx.toast.error("Please log in to start a new chat.")
            return

        try:
            with rx.session() as session:
                new_session = ChatSession(
                    user_id=auth_state.user_id,
                    title="New Chat",
                )
                session.add(new_session)
                session.commit()
                session.refresh(new_session)

                self.active_session_id = str(new_session.id)
                self.active_session = {
                    "id": str(new_session.id),
                    "title": new_session.title or "New Chat",
                    "created_at": new_session.created_at.isoformat() if new_session.created_at else "",
                    "updated_at": new_session.updated_at.isoformat() if new_session.updated_at else "",
                }
                self.sessions.insert(0, self.active_session)
                self.active_session_messages = []
                self.streaming_response = ""
        except Exception as e:
            print(f"Error creating session: {e}")
            yield rx.toast.error("Failed to create new chat session.")

    @rx.event
    def set_user_input(self, value: str):
        """Update user input text."""
        self.user_input_text = value

    @rx.event
    async def send_message(self):
        """Send user message and get AI response."""
        if not self.user_input_text.strip():
            return

        if not self.active_session_id:
            yield SyntropyChatState.create_new_session
            return

        user_message = self.user_input_text.strip()
        self.user_input_text = ""

        self.active_session_messages.append({
            "id": f"temp-{len(self.active_session_messages)}",
            "content": user_message,
            "is_ai": False,
            "created_at": "",
        })

        self.is_streaming = True
        self.streaming_response = ""
        yield

        yield SyntropyChatState.stream_bot_response(user_message)

    @rx.event(background=True)
    async def stream_bot_response(self, user_message: str):
        """Stream AI response."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            async with self:
                self.active_session_messages.append({
                    "id": f"ai-{len(self.active_session_messages)}",
                    "content": "AI service is currently unavailable.",
                    "is_ai": True,
                    "created_at": "",
                })
                self.is_streaming = False
            return

        try:
            async with self:
                conversation = [{"role": "system", "content": self.system_prompt}]
                for msg in self.active_session_messages[:-1]:
                    role = "assistant" if msg.get("is_ai") else "user"
                    conversation.append({"role": role, "content": msg.get("content", "")})
                conversation.append({"role": "user", "content": user_message})

            async with httpx.AsyncClient(timeout=60.0) as client:
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
                        "stream": False,
                    },
                )

            if response.status_code == 200:
                data = response.json()
                ai_message = data["choices"][0]["message"]["content"]
                async with self:
                    self.streaming_response = ai_message
                    self.active_session_messages.append({
                        "id": f"ai-{len(self.active_session_messages)}",
                        "content": ai_message,
                        "is_ai": True,
                        "created_at": "",
                    })
            else:
                async with self:
                    self.active_session_messages.append({
                        "id": f"ai-{len(self.active_session_messages)}",
                        "content": "Sorry, I couldn't process that request.",
                        "is_ai": True,
                        "created_at": "",
                    })
        except Exception as e:
            async with self:
                self.active_session_messages.append({
                    "id": f"ai-{len(self.active_session_messages)}",
                    "content": f"An error occurred: {str(e)}",
                    "is_ai": True,
                    "created_at": "",
                })
        finally:
            async with self:
                self.is_streaming = False
                self.streaming_response = ""

    @rx.event
    def toggle_sidebar(self):
        """Toggle sidebar collapsed state."""
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.var
    def has_messages(self) -> bool:
        """Check if there are any messages in the active session."""
        return len(self.active_session_messages) > 0
