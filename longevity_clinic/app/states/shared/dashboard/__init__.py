"""Dashboard states for health data management.

This module provides decomposed dashboard states for different health categories:
- FoodState: Nutrition and food tracking
- MedicationState: Medication entries and subscriptions
- ConditionState: Health conditions/diagnoses
- SymptomState: Symptoms, logs, and trends
- DataSourceState: Connected devices and apps
- SettingsState: User preferences and UI navigation
- TreatmentPortalState: Active treatments/protocols with pagination

Admin-specific state:
- AdminDashboardState: Admin tab navigation (in states/admin/)
- AdminPatientHealthState: Admin viewing patient data (in states/admin/)

Usage:
    from longevity_clinic.app.states.shared.dashboard import (
        FoodState,
        MedicationState,
        ConditionState,
        SymptomState,
        DataSourceState,
        SettingsState,
        TreatmentPortalState,
    )

"""

# Full dashboard states (decomposed)
# Admin state (from admin module)
from ...admin import AdminDashboardState
from .condition import ConditionState
from .data_source import DataSourceState
from .food import FoodState, calculate_nutrition
from .medication import MedicationState
from .settings import SettingsState
from .symptom import SymptomState
from .treatment import TreatmentPortalState

__all__ = [
    # Admin
    "AdminDashboardState",
    # Full dashboard (decomposed)
    "ConditionState",
    "DataSourceState",
    "FoodState",
    "MedicationState",
    "SettingsState",
    "SymptomState",
    "TreatmentPortalState",
    "calculate_nutrition",
]
