"""Patient treatment search page module.

This module provides the treatment search interface for patients with:
- Treatment cards with details
- Search and category filters
- Treatment details modal with request submission
"""

from .page import treatment_search_page
from .components import (
    treatment_card,
)
from .modals import (
    treatment_details_modal,
)

__all__ = [
    "treatment_search_page",
    # Components
    "treatment_card",
    # Modals
    "treatment_details_modal",
]
