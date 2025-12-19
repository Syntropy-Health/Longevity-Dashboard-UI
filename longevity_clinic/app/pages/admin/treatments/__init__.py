"""Treatments page module.

This module provides the treatment protocols management interface with:
- Protocol cards and listing
- Filters for searching protocols
- Editor modal for creating/editing protocols
- Assignment modal for assigning protocols to patients
"""

from .page import treatments_page
from .components import (
    category_badge,
    protocol_card,
    protocol_filters,
)
from .modals import (
    treatment_editor_modal,
    assignment_modal,
)

__all__ = [
    "treatments_page",
    # Components
    "category_badge",
    "protocol_card",
    "protocol_filters",
    # Modals
    "treatment_editor_modal",
    "assignment_modal",
]
