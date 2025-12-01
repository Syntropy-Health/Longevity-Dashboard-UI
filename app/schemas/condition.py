from pydantic import BaseModel
from app.enums import ConditionStatus, ConditionSeverity


class Condition(BaseModel):
    id: str
    name: str
    description: str
    status: ConditionStatus
    severity: ConditionSeverity
    date_diagnosed: str
    last_updated: str
    icon: str = "activity"