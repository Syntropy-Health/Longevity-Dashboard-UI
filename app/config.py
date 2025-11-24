from pydantic import BaseModel, Field
from app.enums import BiomarkerMetricName, MeasurementUnit


class BiomarkerConfig(BaseModel):
    name: BiomarkerMetricName | str
    unit: MeasurementUnit | str
    optimal_range_min: float
    optimal_range_max: float
    description: str


class TreatmentCategoryConfig(BaseModel):
    id: str
    name: str
    description: str


class RoleConfig(BaseModel):
    role_name: str
    permissions: list[str]


class AppSettings(BaseModel):
    clinic_name: str = "Aether Longevity Institute"
    version: str = "1.0.0"
    supported_biomarkers: list[BiomarkerConfig] = [
        BiomarkerConfig(
            name=BiomarkerMetricName.NAD_PLUS,
            unit=MeasurementUnit.MICROMOLAR,
            optimal_range_min=20.0,
            optimal_range_max=40.0,
            description="Cellular energy and repair",
        ),
        BiomarkerConfig(
            name=BiomarkerMetricName.HS_CRP,
            unit=MeasurementUnit.MILLIGRAMS_PER_LITER,
            optimal_range_min=0.0,
            optimal_range_max=1.0,
            description="Inflammation marker",
        ),
        BiomarkerConfig(
            name=BiomarkerMetricName.CORTISOL_AM,
            unit="µg/dL",
            optimal_range_min=6.0,
            optimal_range_max=23.0,
            description="Stress hormone",
        ),
        BiomarkerConfig(
            name=BiomarkerMetricName.VITAMIN_D,
            unit=MeasurementUnit.NANOGRAMS_PER_ML,
            optimal_range_min=40.0,
            optimal_range_max=80.0,
            description="Immune function and bone health",
        ),
    ]
    treatment_categories: list[TreatmentCategoryConfig] = [
        TreatmentCategoryConfig(
            id="peptides",
            name="Peptide Therapy",
            description="Signaling molecules for cellular repair",
        ),
        TreatmentCategoryConfig(
            id="iv", name="IV Nutraceuticals", description="Direct nutrient delivery"
        ),
        TreatmentCategoryConfig(
            id="hb", name="Hyperbaric Oxygen", description="Oxygen saturation therapy"
        ),
    ]
    roles: dict[str, RoleConfig] = {
        "admin": RoleConfig(
            role_name="Admin",
            permissions=["manage_protocols", "view_all_patients", "approve_requests"],
        ),
        "patient": RoleConfig(
            role_name="Patient", permissions=["view_own_data", "request_protocol"]
        ),
        "guest": RoleConfig(role_name="Guest", permissions=[]),
    }


settings = AppSettings()