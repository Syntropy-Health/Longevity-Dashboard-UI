"""Food state for nutrition tracking.

Handles food entries, nutrition summary, and related pagination.
Separates today's meals from past meals with timezone-aware date comparison.
"""

import asyncio
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import reflex as rx

from ....config import current_config, get_logger
from ....data.schemas.llm import FoodEntryModel as FoodEntry
from ....data.schemas.state import NutritionSummary
from ....functions.db_utils import get_food_entries_sync
from ...auth.base import AuthState
from .settings import SettingsState

logger = get_logger("longevity_clinic.dashboard.food")

# Default nutrition
DEFAULT_NUTRITION: NutritionSummary = {
    "total_calories": 0,
    "goal_calories": 2000,
    "total_protein": 0.0,
    "total_carbs": 0.0,
    "total_fat": 0.0,
    "water_intake": 0.0,
}


def calculate_nutrition(food_entries: list[FoodEntry]) -> dict[str, Any]:
    """Calculate nutrition summary from food entries."""
    if not food_entries:
        return dict(DEFAULT_NUTRITION)

    total_calories = sum(entry.get("calories", 0) for entry in food_entries)
    total_protein = sum(float(entry.get("protein", 0)) for entry in food_entries)
    total_carbs = sum(float(entry.get("carbs", 0)) for entry in food_entries)
    total_fat = sum(float(entry.get("fat", 0)) for entry in food_entries)

    return {
        "total_calories": total_calories,
        "goal_calories": 2000,  # Default daily goal
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat,
        "water_intake": 0.0,  # Not tracked in food entries
    }


def parse_logged_at(entry: FoodEntry) -> datetime | None:
    """Parse the logged_at timestamp from a food entry.

    The entry may have 'logged_at' as a datetime or ISO string.
    Returns None if parsing fails.
    """
    logged_at = entry.get("logged_at")
    if logged_at is None:
        return None
    if isinstance(logged_at, datetime):
        return logged_at
    if isinstance(logged_at, str):
        try:
            # Try ISO format first
            return datetime.fromisoformat(logged_at.replace("Z", "+00:00"))
        except ValueError:
            pass
    return None


class FoodState(rx.State):
    """State for food and nutrition tracking."""

    # Data - all food entries (raw from DB)
    food_entries: list[FoodEntry] = []
    # Nutrition summary computed from TODAY's meals only
    nutrition_summary: dict[str, Any] = dict(DEFAULT_NUTRITION)

    # Add food modal state
    show_add_food_modal: bool = False
    new_food_name: str = ""
    new_food_calories: str = ""
    new_food_protein: str = ""
    new_food_carbs: str = ""
    new_food_fat: str = ""
    new_food_meal_type: str = "snack"

    # Detail modal state
    show_food_detail_modal: bool = False
    selected_food_entry: dict[str, Any] = {}

    # Pagination - page size from config
    _FOOD_PAGE_SIZE: int = current_config.food_page_size
    # Separate pagination for today and past
    todays_meals_page: int = 1
    past_meals_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Data Loading Config
    # =========================================================================

    @rx.var
    def data_limit(self) -> int:
        """Preemptive data limit based on page_size * preload_pages."""
        return self._FOOD_PAGE_SIZE * current_config.preload_pages

    # =========================================================================
    # Computed Variables - Timezone-aware filtering
    # =========================================================================

    @rx.var
    def _user_timezone(self) -> str:
        """Get user's timezone from SettingsState."""
        # Default to config timezone - will be updated when SettingsState is available
        return current_config.default_timezone

    @rx.var
    def todays_meals(self) -> list[FoodEntry]:
        """Filter food entries to only today's meals (user's timezone)."""
        try:
            tz = ZoneInfo(self._user_timezone)
        except Exception:
            tz = ZoneInfo(current_config.default_timezone)

        now = datetime.now(tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        result = []
        for entry in self.food_entries:
            logged_at = parse_logged_at(entry)
            if logged_at is None:
                # If no timestamp, assume it's from today (for manual entries)
                result.append(entry)
                continue

            # Make timezone-aware if naive
            if logged_at.tzinfo is None:
                logged_at = logged_at.replace(tzinfo=ZoneInfo("UTC"))

            # Convert to user's timezone and compare dates
            logged_local = logged_at.astimezone(tz)
            if logged_local >= today_start:
                result.append(entry)

        return result

    @rx.var
    def past_meals(self) -> list[FoodEntry]:
        """Filter food entries to past meals (before today in user's timezone)."""
        try:
            tz = ZoneInfo(self._user_timezone)
        except Exception:
            tz = ZoneInfo(current_config.default_timezone)

        now = datetime.now(tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        result = []
        for entry in self.food_entries:
            logged_at = parse_logged_at(entry)
            if logged_at is None:
                # Skip entries without timestamp for past meals
                continue

            # Make timezone-aware if naive
            if logged_at.tzinfo is None:
                logged_at = logged_at.replace(tzinfo=ZoneInfo("UTC"))

            # Convert to user's timezone and compare dates
            logged_local = logged_at.astimezone(tz)
            if logged_local < today_start:
                result.append(entry)

        return result

    @rx.var
    def past_meals_count(self) -> str:
        """Count of past meals for badge display."""
        count = len(self.past_meals)
        return f"{count} meal{'s' if count != 1 else ''}"

    # =========================================================================
    # Computed Variables - Selected Food Entry
    # =========================================================================

    @rx.var
    def selected_food_name(self) -> str:
        """Name of selected food entry."""
        return self.selected_food_entry.get("name", "")

    @rx.var
    def selected_food_calories(self) -> int:
        """Calories of selected food entry."""
        return int(self.selected_food_entry.get("calories", 0))

    @rx.var
    def selected_food_protein(self) -> float:
        """Protein of selected food entry."""
        return float(self.selected_food_entry.get("protein", 0.0))

    @rx.var
    def selected_food_carbs(self) -> float:
        """Carbs of selected food entry."""
        return float(self.selected_food_entry.get("carbs", 0.0))

    @rx.var
    def selected_food_fat(self) -> float:
        """Fat of selected food entry."""
        return float(self.selected_food_entry.get("fat", 0.0))

    @rx.var
    def selected_food_time(self) -> str:
        """Time of selected food entry."""
        return self.selected_food_entry.get("time", "")

    @rx.var
    def selected_food_meal_type(self) -> str:
        """Meal type of selected food entry."""
        return self.selected_food_entry.get("meal_type", "").capitalize()

    # =========================================================================
    # Computed Variables - Today's Meals Pagination
    # =========================================================================

    @rx.var
    def todays_meals_paginated(self) -> list[FoodEntry]:
        """Paginated slice of today's meals."""
        start = (self.todays_meals_page - 1) * self._FOOD_PAGE_SIZE
        end = start + self._FOOD_PAGE_SIZE
        return self.todays_meals[start:end]

    @rx.var
    def todays_meals_total_pages(self) -> int:
        return max(
            1,
            (len(self.todays_meals) + self._FOOD_PAGE_SIZE - 1) // self._FOOD_PAGE_SIZE,
        )

    @rx.var
    def todays_meals_has_previous(self) -> bool:
        return self.todays_meals_page > 1

    @rx.var
    def todays_meals_has_next(self) -> bool:
        return self.todays_meals_page < self.todays_meals_total_pages

    @rx.var
    def todays_meals_page_info(self) -> str:
        return f"Page {self.todays_meals_page} of {self.todays_meals_total_pages}"

    @rx.var
    def todays_meals_showing_info(self) -> str:
        total = len(self.todays_meals)
        if total == 0:
            return "No meals today"
        start = (self.todays_meals_page - 1) * self._FOOD_PAGE_SIZE + 1
        end = min(self.todays_meals_page * self._FOOD_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Computed Variables - Past Meals Pagination
    # =========================================================================

    @rx.var
    def past_meals_paginated(self) -> list[FoodEntry]:
        """Paginated slice of past meals."""
        start = (self.past_meals_page - 1) * self._FOOD_PAGE_SIZE
        end = start + self._FOOD_PAGE_SIZE
        return self.past_meals[start:end]

    @rx.var
    def past_meals_total_pages(self) -> int:
        return max(
            1,
            (len(self.past_meals) + self._FOOD_PAGE_SIZE - 1) // self._FOOD_PAGE_SIZE,
        )

    @rx.var
    def past_meals_has_previous(self) -> bool:
        return self.past_meals_page > 1

    @rx.var
    def past_meals_has_next(self) -> bool:
        return self.past_meals_page < self.past_meals_total_pages

    @rx.var
    def past_meals_page_info(self) -> str:
        return f"Page {self.past_meals_page} of {self.past_meals_total_pages}"

    @rx.var
    def past_meals_showing_info(self) -> str:
        total = len(self.past_meals)
        if total == 0:
            return "No past meals"
        start = (self.past_meals_page - 1) * self._FOOD_PAGE_SIZE + 1
        end = min(self.past_meals_page * self._FOOD_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    @rx.var
    def has_past_meals(self) -> bool:
        """Check if there are any past meals to display."""
        return len(self.past_meals) > 0

    # =========================================================================
    # Legacy Computed Variables (for backward compatibility)
    # =========================================================================

    @rx.var
    def food_entries_paginated(self) -> list[FoodEntry]:
        """Paginated slice of food entries (legacy - now uses todays_meals)."""
        return self.todays_meals_paginated

    @rx.var
    def food_entries_total_pages(self) -> int:
        return self.todays_meals_total_pages

    @rx.var
    def food_entries_has_previous(self) -> bool:
        return self.todays_meals_has_previous

    @rx.var
    def food_entries_has_next(self) -> bool:
        return self.todays_meals_has_next

    @rx.var
    def food_entries_page_info(self) -> str:
        return self.todays_meals_page_info

    @rx.var
    def food_entries_showing_info(self) -> str:
        return self.todays_meals_showing_info

    # =========================================================================
    # Data Loading
    # =========================================================================

    def _compute_todays_nutrition(
        self, entries: list[FoodEntry], timezone: str
    ) -> dict[str, Any]:
        """Compute nutrition from today's meals only."""
        try:
            tz = ZoneInfo(timezone)
        except Exception:
            tz = ZoneInfo(current_config.default_timezone)

        now = datetime.now(tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        todays_entries = []
        for entry in entries:
            logged_at = parse_logged_at(entry)
            if logged_at is None:
                # Assume entries without timestamp are from today
                todays_entries.append(entry)
                continue

            if logged_at.tzinfo is None:
                logged_at = logged_at.replace(tzinfo=ZoneInfo("UTC"))

            logged_local = logged_at.astimezone(tz)
            if logged_local >= today_start:
                todays_entries.append(entry)

        return calculate_nutrition(todays_entries)

    @rx.event(background=True)
    async def load_food_data(self):
        """Load food data from database."""
        user_id = 0
        timezone = current_config.default_timezone
        # Calculate limit from config: page_size * preload_pages
        limit = self._FOOD_PAGE_SIZE * current_config.preload_pages
        async with self:
            if self._data_loaded:
                return
            self.is_loading = True
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            # Get user's timezone from settings
            settings_state = await self.get_state(SettingsState)
            timezone = settings_state.user_timezone

        if not user_id:
            async with self:
                self.is_loading = False
            return

        try:
            food_entries = await asyncio.to_thread(
                get_food_entries_sync, user_id, limit=limit
            )
            logger.info(
                "Loaded %d food entries for user_id=%s", len(food_entries), user_id
            )
            # Compute nutrition from today's meals only
            nutrition = self._compute_todays_nutrition(food_entries, timezone)
            async with self:
                self.food_entries = food_entries
                self.nutrition_summary = nutrition
                self.is_loading = False
                self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load food data: %s", e)
            async with self:
                self.is_loading = False

    async def load_food_data_for_patient(self, user_id: int, limit: int = 100):
        """Load food data for a specific patient (admin view)."""
        try:
            food_entries = await asyncio.to_thread(
                get_food_entries_sync, user_id, limit=limit
            )
            logger.info(
                "Loaded %d food entries for patient user_id=%s",
                len(food_entries),
                user_id,
            )
            self.food_entries = food_entries
            # Use default timezone for admin view
            self.nutrition_summary = self._compute_todays_nutrition(
                food_entries, current_config.default_timezone
            )
            self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load food data for patient: %s", e)

    # =========================================================================
    # Pagination - Today's Meals
    # =========================================================================

    def todays_meals_previous_page(self):
        if self.todays_meals_page > 1:
            self.todays_meals_page -= 1

    def todays_meals_next_page(self):
        if self.todays_meals_page < self.todays_meals_total_pages:
            self.todays_meals_page += 1

    # =========================================================================
    # Pagination - Past Meals
    # =========================================================================

    def past_meals_previous_page(self):
        if self.past_meals_page > 1:
            self.past_meals_page -= 1

    def past_meals_next_page(self):
        if self.past_meals_page < self.past_meals_total_pages:
            self.past_meals_page += 1

    # =========================================================================
    # Legacy Pagination (backward compatibility)
    # =========================================================================

    def food_entries_previous_page(self):
        self.todays_meals_previous_page()

    def food_entries_next_page(self):
        self.todays_meals_next_page()

    # =========================================================================
    # Modal Handlers
    # =========================================================================

    def open_add_food_modal(self):
        self.show_add_food_modal = True
        self.new_food_name = ""
        self.new_food_calories = ""
        self.new_food_protein = ""
        self.new_food_carbs = ""
        self.new_food_fat = ""
        self.new_food_meal_type = "snack"

    def select_food_entry(self, entry: dict[str, Any]):
        """Select a food entry for viewing details."""
        self.selected_food_entry = entry
        self.show_food_detail_modal = True

    def close_food_detail_modal(self, _value: bool = False):
        """Close the food detail modal."""
        self.show_food_detail_modal = False

    def set_show_add_food_modal(self, value: bool):
        self.show_add_food_modal = value

    def set_new_food_name(self, value: str):
        self.new_food_name = value

    def set_new_food_calories(self, value: float):
        self.new_food_calories = str(value) if value else ""

    def set_new_food_protein(self, value: float):
        self.new_food_protein = str(value) if value else ""

    def set_new_food_carbs(self, value: float):
        self.new_food_carbs = str(value) if value else ""

    def set_new_food_fat(self, value: float):
        self.new_food_fat = str(value) if value else ""

    def set_new_food_meal_type(self, value: str):
        self.new_food_meal_type = value

    def save_food_entry(self):
        """Save a new food entry."""
        import uuid

        # Set logged_at to current time in ISO format
        now = datetime.now(ZoneInfo("UTC"))

        new_entry = FoodEntry(
            id=str(uuid.uuid4())[:8],
            name=self.new_food_name,
            calories=int(self.new_food_calories) if self.new_food_calories else 0,
            protein=float(self.new_food_protein) if self.new_food_protein else 0.0,
            carbs=float(self.new_food_carbs) if self.new_food_carbs else 0.0,
            fat=float(self.new_food_fat) if self.new_food_fat else 0.0,
            time=now.strftime("%I:%M %p"),
            meal_type=self.new_food_meal_type,
            logged_at=now.isoformat(),
        )
        self.food_entries = [new_entry, *self.food_entries]
        # Recompute nutrition from today's meals
        self.nutrition_summary = self._compute_todays_nutrition(
            self.food_entries, self._user_timezone
        )
        self.show_add_food_modal = False

    def clear_data(self):
        """Clear all food data."""
        self.food_entries = []
        self.nutrition_summary = {}
        self._data_loaded = False
        self.food_entries_page = 1
