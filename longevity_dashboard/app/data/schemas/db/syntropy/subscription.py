"""Subscription plan type definitions."""

from typing import TypedDict


class Plan(TypedDict):
    """Subscription plan definition."""

    name: str
    price: str
    price_id: str  # Stripe price ID
    amount: int  # Price in cents
    features: list[str]
    popular: bool
