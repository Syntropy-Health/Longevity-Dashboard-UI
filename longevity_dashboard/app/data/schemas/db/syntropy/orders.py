"""Order models for product ordering functionality."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

import reflex as rx
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    pass


def get_utc_now():
    return datetime.now(timezone.utc)


class ProductInfo(rx.Model, table=True):
    """Product information for orderable items."""

    __tablename__ = "syntropy_product_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    asin: str = Field(unique=True)
    title: str
    price: Optional[float] = None
    currency: Optional[str] = None
    affiliate_link: str
    image_url: Optional[str] = None


class Order(rx.Model, table=True):
    """User order record."""

    __tablename__ = "syntropy_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    ordered_at: datetime = Field(default_factory=get_utc_now)
    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(rx.Model, table=True):
    """Individual item within an order."""

    __tablename__ = "syntropy_order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="syntropy_orders.id")
    product_id: int = Field(foreign_key="syntropy_product_info.id")
    quantity: int
    order: Order = Relationship(back_populates="items")
    product: ProductInfo = Relationship()
