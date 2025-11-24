from typing import Optional
from pydantic import BaseModel
from app.enums import (
    BiomarkerMetricName,
    PatientStatus,
    TreatmentCategory,
    TreatmentFrequency,
    TreatmentStatus,
)


class Patient(BaseModel):
    name: str = ""
    dob: str = ""
    gender: str = ""
    email: str = ""
    phone: str = ""
    medical_history: str = ""
    medications: str = ""
    allergies: str = ""
    exercise_freq: str = ""
    diet_type: str = ""
    sleep_hours: str = ""
    stress_level: str = ""
    status: PatientStatus | str = PatientStatus.ACTIVE


class TreatmentProtocol(BaseModel):
    id: str
    name: str
    category: TreatmentCategory | str
    description: str
    duration: str
    frequency: TreatmentFrequency | str
    biomarker_targets: list[BiomarkerMetricName | str] = []
    status: TreatmentStatus | str = TreatmentStatus.ACTIVE


class ProtocolRequest(BaseModel):
    id: str
    patient_name: str
    protocol_id: str
    protocol_name: str
    status: str = "pending"
    reason: str = ""
    date: str = ""


class CohortPatient(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    status: PatientStatus | str
    age: int
    biological_age: float
    active_protocols: list[str]
    last_visit: str
    longevity_score: int
    img_url: str = "/placeholder.svg"
    joined_date: str
    biomarkers: dict[str, float] = {}


class BiomarkerEntry(BaseModel):
    name: str
    category: str
    value: float
    unit: str
    status: str
    trend: str
    description: str = ""