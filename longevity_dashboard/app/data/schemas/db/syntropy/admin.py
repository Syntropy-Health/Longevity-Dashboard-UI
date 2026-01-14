"""Admin configuration and subscription models for Syntropy app."""

import datetime
from datetime import timezone
from typing import TYPE_CHECKING, Optional

import reflex as rx
import sqlalchemy
import sqlmodel
from sqlalchemy import JSON, DateTime
from sqlmodel import Column, Field

if TYPE_CHECKING:
    from ..models import User


def get_utc_now():
    return datetime.datetime.now(timezone.utc)


class AdminConfig(rx.Model, table=True):
    """Admin config model that stores workflow configuration as YAML."""

    __tablename__ = "syntropy_admin_config"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    version: float = Field(default=0.1)
    configuration: dict[str, str | int | float | bool | list | dict] = Field(
        default={}, sa_column=Column(JSON)
    )
    is_latest: bool = Field(default=False)
    created_at: datetime.datetime = Field(
        default=None,
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    updated_at: datetime.datetime = Field(
        default=None,
        sa_column=Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )


class SubscriptionFeature(rx.Model, table=True):
    """Subscription feature definition."""

    __tablename__ = "syntropy_subscription_features"

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str
    max_hosts: int = sqlmodel.Field(default=1)
    max_guests: int = sqlmodel.Field(default=1)
    description: Optional[str] = None


class Subscription(rx.Model, table=True):
    """User subscription record."""

    __tablename__ = "syntropy_subscriptions"

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    user_id: int = sqlmodel.Field(foreign_key="users.id")
    feature_id: int = sqlmodel.Field(foreign_key="syntropy_subscription_features.id")
    feature: Optional["SubscriptionFeature"] = sqlmodel.Relationship(back_populates=None)
    start_date: datetime.date
    end_date: datetime.date
    created_at: datetime.datetime = sqlmodel.Field(
        default_factory=get_utc_now,
        sa_column=sqlalchemy.Column(
            "created_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),
    )
    updated_at: datetime.datetime = sqlmodel.Field(
        default_factory=get_utc_now,
        sa_column=sqlalchemy.Column(
            "updated_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
            onupdate=sqlalchemy.func.now(),
        ),
    )
    auto_renew: bool = False
    is_active: bool = True
    cancellation_notes: Optional[str] = None
