from pydantic import BaseModel
from app.enums import MealType


class FoodItem(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float


class Meal(BaseModel):
    id: str
    type: MealType
    food_items: list[FoodItem]
    total_calories: int = 0
    time: str
    image_url: str = "/placeholder.svg"


class DailyNutrition(BaseModel):
    date: str
    meals: list[Meal]
    nutrition_score: int