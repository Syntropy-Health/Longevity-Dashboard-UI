"""Reusable tab components for patient portal.

This module contains card components, item renderers, and shared tab elements
that can be used across different views (patient portal, admin dashboard).

Cards:
- health_card: Generic standardized health card with theming
- medication_entry_card: Log of medication taken
- medication_subscription_card: Prescription with adherence
- medication_notification_card: Medication reminder/notification
- food_entry_card: Food/nutrition entry
- condition_card: Health condition card
- symptom_card: Symptom card with logging
- symptom_log_card: Symptom log entry card
- data_source_card: Device/API connection card

Biomarker Components:
- biomarker_card: Compact biomarker metric card
- biomarker_detail_panel: Expanded detail panel with chart
- status_badge: Status indicator badge
- trend_indicator: Trend arrow with label

Items:
- symptom_log_item: Symptom log entry
- symptom_trend_item: Trend visualization
"""

from .biomarkers import (
    biomarker_card,
    biomarker_detail_panel,
    status_badge,
    trend_indicator,
)
from .cards import (
    condition_card,
    data_source_card,
    food_entry_card,
    health_card,
    medication_entry_card,
    medication_notification_card,
    medication_subscription_card,
    symptom_card,
    symptom_log_card,
)
from .items import (
    symptom_log_item,
    symptom_trend_item,
)
from .shared import import_drop_zone

__all__ = [
    # Biomarker components
    "biomarker_card",
    "biomarker_detail_panel",
    # Health cards
    "condition_card",
    "data_source_card",
    "food_entry_card",
    # Generic card
    "health_card",
    # Shared
    "import_drop_zone",
    # Medication cards
    "medication_entry_card",
    "medication_notification_card",
    "medication_subscription_card",
    # Status/trend indicators
    "status_badge",
    "symptom_card",
    "symptom_log_card",
    # Items
    "symptom_log_item",
    "symptom_trend_item",
    "trend_indicator",
]
