"""Treatment state modules.

DEPRECATED: Import from states.shared or states instead.
These re-exports are kept for backwards compatibility.
"""

# Re-export from shared for backwards compatibility
# TreatmentProtocol TypedDict
from ...data.state_schemas import TreatmentProtocol
from ..shared.treatment import TreatmentSearchState, TreatmentState

__all__ = [
    "TreatmentProtocol",
    "TreatmentSearchState",
    "TreatmentState",
]
