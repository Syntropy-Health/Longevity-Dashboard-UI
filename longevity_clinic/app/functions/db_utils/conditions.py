"""Condition, SymptomTrend, DataSource, Medication notification database operations."""

from __future__ import annotations

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    Condition as ConditionDB,
    DataSource as DataSourceDB,
    SymptomTrend as SymptomTrendDB,
)
from longevity_clinic.app.data.schemas.llm import (
    Condition,
    DataSource,
    SymptomTrend,
)

logger = get_logger("longevity_clinic.db_utils.conditions")


# ============================================================================
# CONDITIONS
# ============================================================================


def get_conditions_sync(
    user_id: int,
    status: str | None = None,
    limit: int = 100,
) -> list[Condition]:
    """Get conditions for a user from database."""
    try:
        with rx.session() as session:
            query = select(ConditionDB).where(ConditionDB.user_id == user_id)
            if status:
                query = query.where(ConditionDB.status == status)
            query = query.order_by(ConditionDB.created_at.desc()).limit(limit)
            conditions = session.exec(query).all()

            return [
                Condition(
                    id=str(c.id),
                    name=c.name,
                    icd_code=c.icd_code or "",
                    diagnosed_date=c.diagnosed_date or "",
                    status=c.status or "active",
                    severity=c.severity or "mild",
                    treatments=c.treatments or "",
                )
                for c in conditions
            ]
    except Exception as e:
        logger.error("Failed to get conditions for user %s: %s", user_id, e)
        return []


def create_condition_sync(
    user_id: int,
    name: str,
    icd_code: str = "",
    diagnosed_date: str = "",
    status: str = "active",
    severity: str = "mild",
    treatments: str = "",
    source: str = "manual",
) -> ConditionDB | None:
    """Create a condition entry for a user."""
    try:
        with rx.session() as session:
            condition = ConditionDB(
                user_id=user_id,
                name=name,
                icd_code=icd_code,
                diagnosed_date=diagnosed_date,
                status=status,
                severity=severity,
                treatments=treatments,
                source=source,
            )
            session.add(condition)
            session.commit()
            session.refresh(condition)
            return condition
    except Exception as e:
        logger.error("Failed to create condition: %s", e)
        return None


def update_condition_status_sync(
    condition_id: int,
    status: str,
) -> bool:
    """Update condition status (active/managed/resolved)."""
    try:
        with rx.session() as session:
            condition = session.get(ConditionDB, condition_id)
            if condition:
                condition.status = status
                session.add(condition)
                session.commit()
                return True
            return False
    except Exception as e:
        logger.error("Failed to update condition status: %s", e)
        return False


# ============================================================================
# SYMPTOM TRENDS
# ============================================================================


def get_symptom_trends_sync(
    user_id: int,
    limit: int = 50,
) -> list[SymptomTrend]:
    """Get symptom trends for a user from database."""
    try:
        with rx.session() as session:
            trends = session.exec(
                select(SymptomTrendDB)
                .where(SymptomTrendDB.user_id == user_id)
                .order_by(SymptomTrendDB.calculated_at.desc())
                .limit(limit)
            ).all()

            return [
                SymptomTrend(
                    id=str(t.id),
                    symptom_name=t.symptom_name,
                    current_severity=t.current_severity,
                    previous_severity=t.previous_severity,
                    trend=t.trend or "stable",
                    change_percent=t.change_percent or 0.0,
                    period=t.period or "Last 7 days",
                )
                for t in trends
            ]
    except Exception as e:
        logger.error("Failed to get symptom trends for user %s: %s", user_id, e)
        return []


def create_symptom_trend_sync(
    user_id: int,
    symptom_name: str,
    current_severity: int,
    previous_severity: int,
    trend: str = "stable",
    change_percent: float = 0.0,
    period: str = "Last 7 days",
) -> SymptomTrendDB | None:
    """Create a symptom trend entry for a user."""
    try:
        with rx.session() as session:
            trend_entry = SymptomTrendDB(
                user_id=user_id,
                symptom_name=symptom_name,
                current_severity=current_severity,
                previous_severity=previous_severity,
                trend=trend,
                change_percent=change_percent,
                period=period,
            )
            session.add(trend_entry)
            session.commit()
            session.refresh(trend_entry)
            return trend_entry
    except Exception as e:
        logger.error("Failed to create symptom trend: %s", e)
        return None


# ============================================================================
# DATA SOURCES
# ============================================================================


def get_data_sources_sync(
    user_id: int,
    source_type: str | None = None,
    limit: int = 50,
) -> list[DataSource]:
    """Get connected data sources for a user from database."""
    try:
        with rx.session() as session:
            query = select(DataSourceDB).where(DataSourceDB.user_id == user_id)
            if source_type:
                query = query.where(DataSourceDB.source_type == source_type)
            query = query.order_by(DataSourceDB.name).limit(limit)
            sources = session.exec(query).all()

            return [
                DataSource(
                    id=str(s.id),
                    name=s.name,
                    type=s.source_type,
                    status=s.status or "disconnected",
                    icon=s.icon or "",
                    image=s.image or "",
                    last_sync=s.last_sync or "Never",
                    connected=s.connected or False,
                )
                for s in sources
            ]
    except Exception as e:
        logger.error("Failed to get data sources for user %s: %s", user_id, e)
        return []


def create_data_source_sync(
    user_id: int,
    name: str,
    source_type: str = "wearable",
    icon: str = "",
    image: str = "",
) -> DataSourceDB | None:
    """Create a data source entry for a user."""
    try:
        with rx.session() as session:
            source = DataSourceDB(
                user_id=user_id,
                name=name,
                source_type=source_type,
                status="disconnected",
                icon=icon,
                image=image,
                connected=False,
            )
            session.add(source)
            session.commit()
            session.refresh(source)
            return source
    except Exception as e:
        logger.error("Failed to create data source: %s", e)
        return None


def toggle_data_source_connection_sync(
    source_id: int,
) -> DataSourceDB | None:
    """Toggle a data source connection status."""
    try:
        with rx.session() as session:
            source = session.get(DataSourceDB, source_id)
            if source:
                source.connected = not source.connected
                source.status = "connected" if source.connected else "disconnected"
                source.last_sync = "Just now" if source.connected else "Disconnected"
                session.add(source)
                session.commit()
                session.refresh(source)
                return source
            return None
    except Exception as e:
        logger.error("Failed to toggle data source: %s", e)
        return None


# ============================================================================
# MEDICATION NOTIFICATIONS (formerly Reminders)
# ============================================================================


def get_medication_notifications_sync(
    user_id: int,
    include_completed: bool = True,
    limit: int = 50,
) -> list[dict]:
    """Get medication notifications for a user from database.

    These are notifications with notification_type='medication'.
    Returns dicts compatible with Notification TypedDict.
    """
    from longevity_clinic.app.data.schemas.db import Notification as NotificationDB

    try:
        with rx.session() as session:
            query = select(NotificationDB).where(
                NotificationDB.user_id == user_id,
                NotificationDB.notification_type == "medication",
            )
            if not include_completed:
                query = query.where(NotificationDB.completed == False)  # noqa: E712
            query = query.order_by(NotificationDB.created_at.desc()).limit(limit)
            notifications = session.exec(query).all()

            return [
                {
                    "id": str(n.id),
                    "title": n.title,
                    "message": n.message,
                    "type": n.notification_type,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat() if n.created_at else "",
                    "recipient_role": n.recipient_role,
                    "patient_id": n.patient_id,
                    "time": n.time or "",
                    "completed": n.completed,
                    "recurring": n.recurring,
                }
                for n in notifications
            ]
    except Exception as e:
        logger.error(
            "Failed to get medication notifications for user %s: %s", user_id, e
        )
        return []


def create_medication_notification_sync(
    user_id: int,
    title: str,
    time: str,
    message: str = "",
    recurring: bool = False,
) -> "NotificationDB | None":
    """Create a medication notification for a user."""
    from uuid import uuid4

    from longevity_clinic.app.data.schemas.db import Notification as NotificationDB

    try:
        with rx.session() as session:
            notification = NotificationDB(
                notification_id=f"MED-{uuid4().hex[:8].upper()}",
                user_id=user_id,
                title=title,
                message=message,
                notification_type="medication",
                time=time,
                completed=False,
                recurring=recurring,
                recipient_role="patient",
            )
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification
    except Exception as e:
        logger.error("Failed to create medication notification: %s", e)
        return None


def toggle_medication_completed_sync(notification_id: int) -> bool:
    """Toggle a medication notification's completed status."""
    from datetime import UTC, datetime

    from longevity_clinic.app.data.schemas.db import Notification as NotificationDB

    try:
        with rx.session() as session:
            notification = session.get(NotificationDB, notification_id)
            if notification and notification.notification_type == "medication":
                notification.completed = not notification.completed
                notification.completed_at = (
                    datetime.now(UTC) if notification.completed else None
                )
                session.add(notification)
                session.commit()
                return True
            return False
    except Exception as e:
        logger.error("Failed to toggle medication notification: %s", e)
        return False


__all__ = [
    # Conditions
    "get_conditions_sync",
    "create_condition_sync",
    "update_condition_status_sync",
    # Symptom trends
    "get_symptom_trends_sync",
    "create_symptom_trend_sync",
    # Data sources
    "get_data_sources_sync",
    "create_data_source_sync",
    "toggle_data_source_connection_sync",
    # Medication notifications (formerly reminders)
    "get_medication_notifications_sync",
    "create_medication_notification_sync",
    "toggle_medication_completed_sync",
]
