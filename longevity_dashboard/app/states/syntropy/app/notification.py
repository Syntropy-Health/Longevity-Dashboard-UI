"""Notification state for Syntropy app alerts, suggestions, and tips."""

import asyncio
import datetime
import logging
import random
from typing import List

import reflex as rx

from ....data.schemas.db.syntropy import (
    MAX_NOTIFICATIONS,
    NotificationType,
    SyntropyNotification,
)
from ..base import ConfigurableState

logger = logging.getLogger(__name__)


class SyntropyNotificationState(ConfigurableState, rx.State):
    """Notification state with configuration loading capabilities."""

    notifications: List[SyntropyNotification] = []
    _next_id: int = 0
    _last_tip_suggestion_time: float = 0
    _last_alert_time: float = 0

    tips_messages: List[str] = [
        "Stretching for a few minutes can help relieve muscle tension given that you've stressed your muscles recently.",
    ]
    suggestion_messages: List[str] = [
        "Based on your recent entries, consider adding magnesium-rich foods or supplements to your diet."
    ]
    alert_messages: List[str] = [
        "You're suggested to consult a healthcare professional given your persistent symptoms of fatigue.",
    ]

    alerts_collapsed: bool = False
    suggestions_collapsed: bool = False
    tips_collapsed: bool = False

    alerts_display_count: int = 10
    suggestions_display_count: int = 10
    tips_display_count: int = 10

    show_alert: bool = False
    latest_message_text: str = ""

    tip_suggestion_interval: int = 30
    alert_interval: int = 60
    alert_display_duration: int = 4
    auto_hide_alerts: bool = True
    enable_background_notifications: bool = True
    notification_sound_enabled: bool = False

    @rx.event
    async def on_load(self):
        """Load notification configuration on state initialization."""
        await self.load_notification_config()
        if self.enable_background_notifications:
            return SyntropyNotificationState.health_alert_system

    @rx.event
    async def load_notification_config(self):
        """Load notification configuration from admin config database."""
        config = await self.load_admin_config("notification_config")

        if config:
            self.tip_suggestion_interval = self.get_config_value(
                "app.notifications.timing.tip_suggestion_interval",
                self.tip_suggestion_interval
            )
            self.alert_interval = self.get_config_value(
                "app.notifications.timing.alert_interval",
                self.alert_interval
            )

            config_tips = self.get_config_value("app.notifications.messages.tips")
            if config_tips:
                self.tips_messages = config_tips

            logger.info("Loaded notification configuration from admin config")
        else:
            logger.info("Using default notification configuration")

    def _add_notification(
        self,
        notification_type: NotificationType,
        title: str,
        message: str,
    ):
        now = datetime.datetime.now().isoformat()
        notification = SyntropyNotification(
            id=self._next_id,
            notification_type=notification_type,
            title=title,
            message=message,
            timestamp=now,
            read=False,
        )
        self.notifications.insert(0, notification)
        self._next_id += 1
        if len(self.notifications) > MAX_NOTIFICATIONS:
            self.notifications.pop()

    @rx.event
    def remove_notification(self, notification_id: int):
        self.notifications = [
            n for n in self.notifications if n["id"] != notification_id
        ]

    @rx.event
    def mark_as_read(self, notification_id: int):
        for i, notification in enumerate(self.notifications):
            if notification["id"] == notification_id:
                self.notifications[i]["read"] = True
                break

    @rx.var
    def unread_count(self) -> int:
        return sum((1 for n in self.notifications if not n["read"]))

    @rx.event(background=True)
    async def hide_alert_after_delay(self):
        await asyncio.sleep(4)
        async with self:
            self.show_alert = False

    @rx.event(background=True)
    async def health_alert_system(self):
        async with self:
            current_time = asyncio.get_event_loop().time()
            self._last_tip_suggestion_time = current_time
            self._last_alert_time = current_time
        notification_type = title = message = None
        while True:
            await asyncio.sleep(1)
            current_time = asyncio.get_event_loop().time()
            async with self:
                if current_time - self._last_tip_suggestion_time >= 30:
                    self._last_tip_suggestion_time = current_time
                    rand_val = random.random()
                    if rand_val < 0.5:
                        notification_type = NotificationType.TIPS
                        title = "Mindful Tip"
                        message = random.choice(self.tips_messages)
                    else:
                        notification_type = NotificationType.SUGGESTION
                        title = "Health Suggestion"
                        message = random.choice(self.suggestion_messages)
                    yield
                if current_time - self._last_alert_time >= 60:
                    self._last_alert_time = current_time
                    notification_type = NotificationType.ALERT
                    title = "Health Alert"
                    message = random.choice(self.alert_messages)
                    self.show_alert = True
                if notification_type and title and message:
                    self._add_notification(notification_type, title, message)
                    self.latest_message_text = message
                yield SyntropyNotificationState.hide_alert_after_delay

    @rx.event
    def dismiss_alert(self):
        self.show_alert = False

    @rx.var
    def tips(self) -> List[SyntropyNotification]:
        return [n for n in self.notifications if n["notification_type"] == NotificationType.TIPS]

    @rx.var
    def suggestions(self) -> List[SyntropyNotification]:
        return [n for n in self.notifications if n["notification_type"] == NotificationType.SUGGESTION]

    @rx.var
    def alerts(self) -> List[SyntropyNotification]:
        return [n for n in self.notifications if n["notification_type"] == NotificationType.ALERT]

    @rx.event
    def toggle_collapse(self, section: str):
        if section == "alerts":
            self.alerts_collapsed = not self.alerts_collapsed
        elif section == "suggestions":
            self.suggestions_collapsed = not self.suggestions_collapsed
        elif section == "tips":
            self.tips_collapsed = not self.tips_collapsed

    @rx.event
    def show_more(self, section: str):
        if section == "alerts":
            self.alerts_display_count += 10
        elif section == "suggestions":
            self.suggestions_display_count += 10
        elif section == "tips":
            self.tips_display_count += 10

    @rx.var
    def paginated_alerts(self) -> List[SyntropyNotification]:
        return self.alerts[: self.alerts_display_count]

    @rx.var
    def has_more_alerts(self) -> bool:
        return len(self.alerts) > self.alerts_display_count

    @rx.var
    def paginated_suggestions(self) -> List[SyntropyNotification]:
        return self.suggestions[: self.suggestions_display_count]

    @rx.var
    def has_more_suggestions(self) -> bool:
        return len(self.suggestions) > self.suggestions_display_count

    @rx.var
    def paginated_tips(self) -> List[SyntropyNotification]:
        return self.tips[: self.tips_display_count]

    @rx.var
    def has_more_tips(self) -> bool:
        return len(self.tips) > self.tips_display_count
