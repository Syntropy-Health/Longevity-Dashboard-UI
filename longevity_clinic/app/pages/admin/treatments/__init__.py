"""Treatments page module.

This module provides the treatment protocols management interface with:
- Protocol cards and listing
- Filters for searching protocols
- Editor modal for creating/editing protocols
- Assignment modal for assigning protocols to patients
"""

# Re-export category_badge from shared for backwards compatibility
from ....components.shared.treatment import category_badge
from .components import (
    protocol_card,
    protocol_filters,
)
from .modals import (
    assignment_modal,
    treatment_editor_modal,
)
from .page import treatments_page

__all__ = [
    "assignment_modal",
    # Components
    "category_badge",
    "protocol_card",
    "protocol_filters",
    # Modals
    "treatment_editor_modal",
    "treatments_page",
]
