"""Reusable tab components for patient portal.

This module contains card components, item renderers, and shared tab elements
that can be used across different views (patient portal, admin dashboard).

Cards:
- medication_entry_card: Log of medication taken
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
    medication_entry_card,
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
    # Health cards
    "condition_card",
    "data_source_card",
    "food_entry_card",
    # Shared
    "import_drop_zone",
    # Medication cards
    "medication_entry_card",
    "medication_subscription_card",
    "reminder_item",
    "symptom_card",
    # Items
    "symptom_log_item",
    "symptom_trend_item",
]
