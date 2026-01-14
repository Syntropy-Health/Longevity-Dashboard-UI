"""User settings model for Syntropy app preferences."""

from typing import TYPE_CHECKING, Optional

import reflex as rx
from sqlmodel import JSON, Column, Field, Relationship

if TYPE_CHECKING:
    from ..models import User


def get_default_order_integrations():
    """Return default order integration settings."""
    return {
        "amazon": False,
        "cookunity": False,
        "doordash": False,
        "instacart": False,
        "thrive_market": False,
        "hellofresh": False,
        "blue_apron": False,
        "uber_eats": False,
    }


class SyntropySettings(rx.Model, table=True):
    """User settings for Syntropy app features."""

    __tablename__ = "syntropy_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    order_integrations: dict[str, bool] = Field(
        default_factory=get_default_order_integrations,
        sa_column=Column(JSON),
    )
    include_herbal_supplement: bool = Field(default=False)
    notification_frequency: int = Field(default=1)
    notification_aggressiveness: int = Field(default=0)
    payment_info_stored: bool = Field(default=False)
    subscription_plan: str = Field(default="Free")
