import reflex as rx
from app.schemas.nutrition import DailyNutrition, Meal, FoodItem
from app.enums import MealType


class NutritionState(rx.State):
    current_day: DailyNutrition = DailyNutrition(
        date="Today",
        meals=[
            Meal(
                id="m1",
                type=MealType.BREAKFAST,
                time="08:00 AM",
                food_items=[
                    FoodItem(name="Oatmeal", calories=150, protein=5, carbs=27, fat=3),
                    FoodItem(name="Berries", calories=50, protein=1, carbs=12, fat=0),
                ],
                total_calories=200,
            ),
            Meal(
                id="m2",
                type=MealType.LUNCH,
                time="12:30 PM",
                food_items=[
                    FoodItem(
                        name="Grilled Chicken Salad",
                        calories=350,
                        protein=30,
                        carbs=10,
                        fat=15,
                    )
                ],
                total_calories=350,
            ),
        ],
        nutrition_score=76,
    )

    @rx.var
    def total_calories(self) -> int:
        return sum((m.total_calories for m in self.current_day.meals))

    @rx.event
    def log_meal(self):
        return rx.toast("Meal logging coming soon.")