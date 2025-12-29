"""Patient portal tab components.

Tab modules provide the tab content views.
Card/item components are imported from components/tabs for reuse.
"""

# Re-export card/item components from centralized location
from ....components.tabs import (
    condition_card,
    data_source_card,
    food_entry_card,
    import_drop_zone,
    medication_entry_card,
    medication_subscription_card,
    symptom_card,
    symptom_log_item,
    symptom_trend_item,
)

# Tab content views
from .checkins import checkins_tab, patient_checkin_card
from .conditions import conditions_tab
from .data_sources import data_sources_tab
from .food_tracker import food_tracker_tab
from .medications import medications_tab
from .overview import overview_tab
from .settings import settings_tab
from .symptoms import symptoms_tab

__all__ = [
    # Tab views
    "checkins_tab",
    # Card components (from components/tabs)
    "condition_card",
    "conditions_tab",
    "data_source_card",
    "data_sources_tab",
    "food_entry_card",
    "food_tracker_tab",
    "import_drop_zone",
    "medication_entry_card",
    "medication_subscription_card",
    "medications_tab",
    "overview_tab",
    "patient_checkin_card",
    "settings_tab",
    "symptom_card",
    "symptom_log_item",
    "symptom_trend_item",
    "symptoms_tab",
]
