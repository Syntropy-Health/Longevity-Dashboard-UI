from pydantic import BaseModel
from app.enums import TreatmentFrequency


class Medication(BaseModel):
    id: str
    name: str
    dosage: str
    frequency: TreatmentFrequency | str
    efficacy_rating: int
    is_active: bool = True
    next_refill: str
    adherence_score: int