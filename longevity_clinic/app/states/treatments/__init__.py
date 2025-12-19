"""Treatment state modules.

DEPRECATED: Import from states.shared or states instead.
These re-exports are kept for backwards compatibility.
"""

# Re-export from shared for backwards compatibility
from ..shared.treatment import TreatmentState, TreatmentSearchState

# TreatmentProtocol TypedDict
from ...data.state_schemas import TreatmentProtocol

__all__ = [
    "TreatmentState",
    "TreatmentSearchState",
    "TreatmentProtocol",
]
