"""Reusable tab components for patient portal.

This module contains card components, item renderers, and shared tab elements
that can be used across different views (patient portal, admin dashboard).

Cards:
- medication_log_card: Log of medication taken
- medication_subscription_card: Prescription with adherence
- food_entry_card: Food/nutrition entry
- condition_card: Health condition card
- symptom_card: Symptom card with logging
- data_source_card: Device/API connection card

Items:
- symptom_log_item: Symptom log entry
- symptom_trend_item: Trend visualization
- reminder_item: Reminder/notification item
"""

from .cards import (
    condition_card,
    data_source_card,
    food_entry_card,
    medication_log_card,
    medication_subscription_card,
    symptom_card,
)
from .items import (
    reminder_item,
    symptom_log_item,
    symptom_trend_item,
)
from .shared import import_drop_zone

__all__ = [
    # Medication cards
    "medication_log_card",
    "medication_subscription_card",
    # Health cards
    "condition_card",
    "symptom_card",
    "food_entry_card",
    "data_source_card",
    # Items
    "symptom_log_item",
    "symptom_trend_item",
    "reminder_item",
    # Shared
    "import_drop_zone",
]
