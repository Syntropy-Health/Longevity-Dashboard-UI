"""Catalog state for managing health product catalog with configurable features."""

import logging
from typing import List

import reflex as rx

from ....data.schemas.db.syntropy import CatalogItem, CategoryItem
from ..base import ConfigurableState

logger = logging.getLogger(__name__)


class CatalogState(ConfigurableState, rx.State):
    """Catalog state with configuration loading capabilities."""

    catalog_items: List[CatalogItem] = []
    filtered_items: List[CatalogItem] = []
    current_page: int = 1
    items_per_page: int = 12
    total_items: int = 0
    is_loading: bool = False

    search_query: str = ""
    selected_category: str = "all"
    selected_sort: str = "name"
    show_favorites_only: bool = False

    enable_favorites: bool = True
    enable_ratings: bool = True
    enable_price_filter: bool = True
    enable_category_filter: bool = True
    max_price_range: int = 1000
    min_price_range: int = 0

    categories: List[CategoryItem] = [
        {"id": "all", "name": "All Categories", "icon": "grid"},
        {"id": "supplements", "name": "Supplements", "icon": "pill"},
        {"id": "nutrition", "name": "Nutrition", "icon": "apple"},
        {"id": "fitness", "name": "Fitness", "icon": "dumbbell"},
        {"id": "wellness", "name": "Wellness", "icon": "heart"},
    ]

    _default_catalog_items: List[CatalogItem] = [
        {
            "id": 1,
            "name": "Premium Omega-3 Fish Oil",
            "category": "supplements",
            "price": 29.99,
            "rating": 4.8,
            "description": "High-quality fish oil for brain and heart health",
            "image": "/img/supplement-omega3.jpg",
            "in_stock": True,
            "is_favorite": False,
            "tags": ["brain-health", "heart-health", "premium"]
        },
        {
            "id": 2,
            "name": "Organic Green Superfood Powder",
            "category": "nutrition",
            "price": 45.00,
            "rating": 4.6,
            "description": "Nutrient-dense green superfood blend",
            "image": "/img/nutrition-greens.jpg",
            "in_stock": True,
            "is_favorite": True,
            "tags": ["organic", "superfood", "energy"]
        },
        {
            "id": 3,
            "name": "Smart Fitness Tracker",
            "category": "fitness",
            "price": 199.99,
            "rating": 4.7,
            "description": "Advanced fitness tracking with health insights",
            "image": "/img/fitness-tracker.jpg",
            "in_stock": True,
            "is_favorite": False,
            "tags": ["technology", "tracking", "insights"]
        },
        {
            "id": 4,
            "name": "Meditation & Sleep Support",
            "category": "wellness",
            "price": 34.99,
            "rating": 4.5,
            "description": "Natural sleep aid and stress relief supplement",
            "image": "/img/wellness-sleep.jpg",
            "in_stock": False,
            "is_favorite": True,
            "tags": ["sleep", "stress-relief", "natural"]
        },
    ]

    @rx.event
    async def on_load(self):
        """Load catalog configuration and initialize data on page load."""
        await self.load_catalog_config()
        await self.initialize_catalog()

    @rx.event
    async def load_catalog_config(self):
        """Load catalog configuration from admin config database."""
        config = await self.load_admin_config("catalog_config")

        if config:
            self.enable_favorites = self.get_config_value(
                "app.catalog.features.enable_favorites",
                self.enable_favorites
            )
            self.enable_ratings = self.get_config_value(
                "app.catalog.features.enable_ratings",
                self.enable_ratings
            )
            self.items_per_page = self.get_config_value(
                "app.catalog.settings.items_per_page",
                self.items_per_page
            )

            config_categories = self.get_config_value("app.catalog.categories")
            if config_categories:
                self.categories = config_categories

            logger.info("Loaded catalog configuration from admin config")
        else:
            logger.info("Using default catalog configuration")

    @rx.event
    async def initialize_catalog(self):
        """Initialize catalog with default or database items."""
        self.is_loading = True
        self.catalog_items = self._default_catalog_items.copy()
        self.total_items = len(self.catalog_items)
        await self.apply_filters()
        self.is_loading = False

    @rx.event
    async def apply_filters(self):
        """Apply current search and filter criteria to catalog items."""
        filtered = self.catalog_items.copy()

        if self.search_query.strip():
            query = self.search_query.lower()
            filtered = [
                item for item in filtered
                if query in item["name"].lower()
                or query in item["description"].lower()
                or any(query in tag.lower() for tag in item.get("tags", []))
            ]

        if self.selected_category != "all":
            filtered = [
                item for item in filtered
                if item["category"] == self.selected_category
            ]

        if self.show_favorites_only:
            filtered = [
                item for item in filtered
                if item.get("is_favorite", False)
            ]

        if self.selected_sort == "name":
            filtered.sort(key=lambda x: x["name"])
        elif self.selected_sort == "price_low":
            filtered.sort(key=lambda x: x["price"])
        elif self.selected_sort == "price_high":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif self.selected_sort == "rating":
            filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)

        self.filtered_items = filtered
        self.current_page = 1

    @rx.event
    async def set_search_query(self, query: str):
        """Update search query and apply filters."""
        self.search_query = query
        await self.apply_filters()

    @rx.event
    async def set_category(self, category: str):
        """Update selected category and apply filters."""
        self.selected_category = category
        await self.apply_filters()

    @rx.event
    async def toggle_favorite(self, item_id: int):
        """Toggle favorite status for an item."""
        for item in self.catalog_items:
            if item["id"] == item_id:
                item["is_favorite"] = not item.get("is_favorite", False)
                break
        await self.apply_filters()

    @rx.event
    def set_page(self, page: int):
        """Set current page for pagination."""
        self.current_page = max(1, page)

    @rx.var
    def paginated_items(self) -> List[CatalogItem]:
        """Get items for current page."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_items[start:end]

    @rx.var
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.items_per_page <= 0:
            return 1
        return max(1, (len(self.filtered_items) + self.items_per_page - 1) // self.items_per_page)
