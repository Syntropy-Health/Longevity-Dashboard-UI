"""Patient portal tab content components.

This module re-exports all tab components from the modularized tabs/ directory
for backward compatibility.
"""

# Re-export all tab components from the modularized tabs directory
from .tabs import (
    # Main tabs
    overview_tab,
    food_tracker_tab,
    medications_tab,
    conditions_tab,
    symptoms_tab,
    data_sources_tab,
    checkins_tab,
    settings_tab,
    # Individual components (for reuse)
    food_entry_card,
    medication_card,
    condition_card,
    symptom_card,
    symptom_log_item,
    reminder_item,
    symptom_trend_item,
    data_source_card,
    import_drop_zone,
    checkin_card,
)

__all__ = [
    # Main tabs
    "overview_tab",
    "food_tracker_tab",
    "medications_tab",
    "conditions_tab",
    "symptoms_tab",
    "data_sources_tab",
    "checkins_tab",
    "settings_tab",
    # Individual components
    "food_entry_card",
    "medication_card",
    "condition_card",
    "symptom_card",
    "symptom_log_item",
    "reminder_item",
    "symptom_trend_item",
    "data_source_card",
    "import_drop_zone",
    "checkin_card",
]
