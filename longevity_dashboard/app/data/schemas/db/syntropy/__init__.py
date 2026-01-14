"""Syntropy-specific database models and schemas.

Contains models migrated from Syntropy-Journals:
- Chat models (ChatSession, ChatMessage)
- LangGraph checkpoint models
- Order and product models
- Settings and subscription models
- Admin configuration models
- Notification type definitions
- Catalog type definitions
"""

from .admin import AdminConfig, Subscription, SubscriptionFeature
from .catalog import CatalogItem, CategoryItem
from .chat import (
    ChatMessage,
    ChatSession,
    Conversation,
    Message,
    MessageContent,
    MessageData,
    create_chat_message,
    create_chat_message_data,
    create_message_content,
    create_message_data,
    get_utc_now,
)
from .langgraph import Checkpoint, CheckpointBlob, CheckpointMigration, CheckpointWrite
from .notification import MAX_NOTIFICATIONS, NotificationType, SyntropyNotification
from .orders import Order, OrderItem, ProductInfo
from .settings import SyntropySettings, get_default_order_integrations
from .subscription import Plan

__all__ = [
    # Admin
    "AdminConfig",
    # Catalog
    "CatalogItem",
    "CategoryItem",
    # Chat
    "ChatMessage",
    "ChatSession",
    "Conversation",
    # LangGraph checkpoints
    "Checkpoint",
    "CheckpointBlob",
    "CheckpointMigration",
    "CheckpointWrite",
    # Notifications
    "MAX_NOTIFICATIONS",
    "Message",
    "MessageContent",
    "MessageData",
    "NotificationType",
    # Orders
    "Order",
    "OrderItem",
    # Subscription
    "Plan",
    "ProductInfo",
    "Subscription",
    "SubscriptionFeature",
    "SyntropyNotification",
    # Settings
    "SyntropySettings",
    # Utilities
    "create_chat_message",
    "create_chat_message_data",
    "create_message_content",
    "create_message_data",
    "get_default_order_integrations",
    "get_utc_now",
]
