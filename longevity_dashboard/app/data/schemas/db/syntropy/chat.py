"""Chat data models for Syntropy chat functionality."""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import reflex as rx
from sqlmodel import JSON, Column, Field, Relationship
from typing_extensions import TypedDict

# import all langgraph checkpoint models for schema generation
from .langgraph import *

if TYPE_CHECKING:
    from .user import User


def get_utc_now():
    return datetime.now(timezone.utc)


class MessageData(TypedDict, total=False):
    """Structure for the inner message data."""

    id: Optional[str]
    name: Optional[str]
    type: str  # "human", "ai", "system", etc.
    content: str
    additional_kwargs: Dict[str, Any]
    response_metadata: Dict[str, Any]


class MessageContent(TypedDict):
    """Structure for the complete message content."""

    data: MessageData
    type: str  # "human", "ai", "system", etc.


class Message(TypedDict):
    """Legacy message format - kept for backward compatibility."""

    user: str
    text: str
    is_streaming: bool


class Conversation(TypedDict):
    id: str
    title: str
    messages: list[Message]
    timestamp: str


class ChatMessage(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(foreign_key="chatsession.id")
    message: MessageContent = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=get_utc_now)
    session: Optional["ChatSession"] = Relationship(back_populates="messages")

    def dict(self, **kwargs):
        """Override dict method to exclude relationships for Reflex serialization."""
        # Get the base dict but exclude the session relationship
        data = super().dict(exclude={"session"}, **kwargs)
        return data


class ChatSession(rx.Model, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    client_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)
    messages: List["ChatMessage"] = Relationship(back_populates="session")

    def dict(self, **kwargs):
        """Override dict method to exclude relationships for Reflex serialization."""
        # Get the base dict but exclude the messages relationship
        data = super().dict(exclude={"messages"}, **kwargs)
        return data


# --- Concise message creation utilities ---
def create_message_data(message_type: str, content: str, **kwargs) -> MessageData:
    """Create a MessageData object with default values. Accepts all MessageData fields as kwargs."""
    return MessageData(
        type=message_type,
        content=content,
        **{k: v for k, v in kwargs.items() if v is not None},
    )


def create_message_content(message_type: str, content: str, **kwargs) -> MessageContent:
    """Create a MessageContent object with default values. Accepts all MessageData fields as kwargs."""
    return MessageContent(
        data=create_message_data(message_type, content, **kwargs), type=message_type
    )


def create_chat_message(
    session_id: str, message_type: str, content: str, **kwargs
) -> "ChatMessage":
    """Create a ChatMessage object with default values. Accepts all MessageData fields as kwargs."""
    return ChatMessage(
        session_id=session_id,
        message=create_message_content(message_type, content, **kwargs),
    )


def create_chat_message_data(
    session_id: str, message_type: str, content: str, **kwargs
) -> tuple[str, MessageContent]:
    """Create ChatMessage data without instantiating the SQLAlchemy object. Accepts all MessageData fields as kwargs."""
    return session_id, create_message_content(message_type, content, **kwargs)
