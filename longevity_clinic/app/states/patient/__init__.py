"""Patient state modules.

This package contains Reflex state classes for patient functionality.
State classes use simplified names (removing 'Patient' prefix where possible).
"""

from .state import PatientState
from .biomarker_state import PatientBiomarkerState
from .analytics_state import PatientAnalyticsState

# Aliases for cleaner imports (backwards compatible)
BiomarkerState = PatientBiomarkerState
AnalyticsState = PatientAnalyticsState

__all__ = [
    "PatientState",
    "PatientBiomarkerState",
    "PatientAnalyticsState",
    # Aliases
    "BiomarkerState",
    "AnalyticsState",
]
