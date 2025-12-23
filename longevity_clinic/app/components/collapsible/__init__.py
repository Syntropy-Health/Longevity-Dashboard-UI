"""Collapsible section components.

Generic wrapper to turn any card/content into a collapsible accordion section.

Usage:
    from longevity_clinic.app.components.collapsible import (
        collapsible_section,
        collapsible_container,
    )

    # Single collapsible section
    collapsible_section(
        title="My Section",
        content=my_content_component,
        icon="layers",  # Default icon, or use category-specific icons
        badge_count=5,
    )

    # Multiple sections in accordion
    collapsible_container(
        sections=[
            {"title": "Section 1", "value": "s1", "content": content1},
            {"title": "Section 2", "value": "s2", "content": content2},
        ],
        default_expanded=["s1"],
    )
"""

from .section import (
    collapsible_container,
    collapsible_grid,
    collapsible_section,
)

__all__ = [
    "collapsible_container",
    "collapsible_grid",
    "collapsible_section",
]
