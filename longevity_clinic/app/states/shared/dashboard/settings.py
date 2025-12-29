"""Settings state for user preferences.

Handles notification settings, user preferences, timezone, and tab navigation.
"""

from zoneinfo import ZoneInfo

import reflex as rx

from ....config import current_config, get_logger

logger = get_logger("longevity_clinic.dashboard.settings")

# Common timezones for dropdown selection
TIMEZONE_OPTIONS: list[dict[str, str]] = [
    {"value": "America/Los_Angeles", "label": "Pacific Time (PT)"},
    {"value": "America/Denver", "label": "Mountain Time (MT)"},
    {"value": "America/Chicago", "label": "Central Time (CT)"},
    {"value": "America/New_York", "label": "Eastern Time (ET)"},
    {"value": "America/Anchorage", "label": "Alaska Time (AKT)"},
    {"value": "Pacific/Honolulu", "label": "Hawaii Time (HT)"},
    {"value": "Europe/London", "label": "London (GMT/BST)"},
    {"value": "Europe/Paris", "label": "Paris (CET/CEST)"},
    {"value": "Asia/Tokyo", "label": "Tokyo (JST)"},
    {"value": "Asia/Shanghai", "label": "Shanghai (CST)"},
    {"value": "Australia/Sydney", "label": "Sydney (AEST/AEDT)"},
    {"value": "UTC", "label": "UTC"},
]


class SettingsState(rx.State):
    """State for user settings, preferences, and UI navigation."""

    # Tab navigation for patient portal
    active_tab: str = "overview"

    # Notification settings
    email_notifications: bool = True
    push_notifications: bool = True

    # Timezone setting (IANA timezone name)
    user_timezone: str = current_config.default_timezone

    # =========================================================================
    # Computed Variables - Timezone
    # =========================================================================

    @rx.var
    def timezone_options(self) -> list[dict[str, str]]:
        """Available timezone options for dropdown."""
        return TIMEZONE_OPTIONS

    @rx.var
    def timezone_label(self) -> str:
        """Human-readable label for current timezone."""
        for tz in TIMEZONE_OPTIONS:
            if tz["value"] == self.user_timezone:
                return tz["label"]
        return self.user_timezone

    @rx.var
    def zoneinfo(self) -> ZoneInfo:
        """Get ZoneInfo object for current user timezone."""
        try:
            return ZoneInfo(self.user_timezone)
        except Exception:
            return ZoneInfo(current_config.default_timezone)

    # =========================================================================
    # Tab Navigation Handlers
    # =========================================================================

    def set_active_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab
        logger.debug("Active tab set to: %s", tab)

    # =========================================================================
    # Toggle Handlers
    # =========================================================================

    def toggle_email_notifications(self):
        """Toggle email notification preference."""
        self.email_notifications = not self.email_notifications
        logger.info("Email notifications set to: %s", self.email_notifications)

    def toggle_push_notifications(self):
        """Toggle push notification preference."""
        self.push_notifications = not self.push_notifications
        logger.info("Push notifications set to: %s", self.push_notifications)

    def set_user_timezone(self, timezone: str):
        """Set user's preferred timezone."""
        self.user_timezone = timezone
        logger.info("User timezone set to: %s", timezone)

    # =========================================================================
    # Data Management
    # =========================================================================

    def clear_data(self):
        """Reset settings to defaults."""
        self.active_tab = "overview"
        self.email_notifications = True
        self.push_notifications = True
        self.user_timezone = current_config.default_timezone
