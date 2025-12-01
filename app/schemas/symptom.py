from pydantic import BaseModel
from app.enums import ConditionSeverity


class Symptom(BaseModel):
    id: str
    name: str
    severity: int
    timestamp: str
    notes: str = ""
    associated_conditions: list[str] = []
    is_reminder_enabled: bool = False