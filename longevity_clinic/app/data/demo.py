"""Demo datasets used across the Longevity Clinic application."""

from .biomarkers import (
    BiomarkerCategoryEnum,
    BiomarkerMetricName,
    BiomarkerMetricSeed,
    BiomarkerStatus,
    MeasurementUnit,
)


BIOMARKER_METRIC_DEMO_DATA: dict[BiomarkerCategoryEnum, list[BiomarkerMetricSeed]] = {
    BiomarkerCategoryEnum.CBC: [
        {
            "metric": BiomarkerMetricName.RED_BLOOD_CELLS,
            "value": 4.8,
            "unit": MeasurementUnit.MILLIONS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "4.5 - 5.9",
            "history_seed": (4.8, 0.2),
        },
        {
            "metric": BiomarkerMetricName.WHITE_BLOOD_CELLS,
            "value": 6.2,
            "unit": MeasurementUnit.THOUSANDS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "4.0 - 11.0",
            "history_seed": (6.2, 0.5),
        },
        {
            "metric": BiomarkerMetricName.HEMOGLOBIN,
            "value": 14.5,
            "unit": MeasurementUnit.GRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "13.5 - 17.5",
            "history_seed": (14.5, 0.3),
        },
        {
            "metric": BiomarkerMetricName.HEMATOCRIT,
            "value": 42.0,
            "unit": MeasurementUnit.PERCENT,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "37.0 - 50.0",
            "history_seed": (42.0, 1.5),
        },
        {
            "metric": BiomarkerMetricName.PLATELETS,
            "value": 250.0,
            "unit": MeasurementUnit.THOUSANDS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "150 - 450",
            "history_seed": (250.0, 20.0),
        },
    ],
    BiomarkerCategoryEnum.METABOLIC_PANEL: [
        {
            "metric": BiomarkerMetricName.GLUCOSE_FASTING,
            "value": 92.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "65 - 99",
            "history_seed": (90.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.HBA1C,
            "value": 5.7,
            "unit": MeasurementUnit.PERCENT,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "< 5.7",
            "history_seed": (5.6, 0.1),
        },
        {
            "metric": BiomarkerMetricName.INSULIN,
            "value": 6.5,
            "unit": MeasurementUnit.MICROINTERNATIONAL_UNITS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "2.6 - 24.9",
            "history_seed": (6.5, 1.2),
        },
        {
            "metric": BiomarkerMetricName.CREATININE,
            "value": 0.9,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "0.7 - 1.3",
            "history_seed": (0.9, 0.1),
        },
    ],
    BiomarkerCategoryEnum.LIPID_PANEL: [
        {
            "metric": BiomarkerMetricName.TOTAL_CHOLESTEROL,
            "value": 185.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 200",
            "history_seed": (180.0, 10.0),
        },
        {
            "metric": BiomarkerMetricName.LDL_CHOLESTEROL,
            "value": 115.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "< 100",
            "history_seed": (110.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.HDL_CHOLESTEROL,
            "value": 55.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "> 40",
            "history_seed": (55.0, 2.0),
        },
        {
            "metric": BiomarkerMetricName.TRIGLYCERIDES,
            "value": 95.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 150",
            "history_seed": (95.0, 15.0),
        },
    ],
    BiomarkerCategoryEnum.HORMONES: [
        {
            "metric": BiomarkerMetricName.TESTOSTERONE_TOTAL,
            "value": 550.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "300 - 1000",
            "history_seed": (550.0, 30.0),
        },
        {
            "metric": BiomarkerMetricName.ESTRADIOL,
            "value": 25.0,
            "unit": MeasurementUnit.PICOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "10 - 40",
            "history_seed": (25.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.CORTISOL_AM,
            "value": 18.5,
            "unit": MeasurementUnit.MICROGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "10 - 20",
            "history_seed": (18.0, 3.0),
        },
        {
            "metric": BiomarkerMetricName.TSH,
            "value": 1.8,
            "unit": MeasurementUnit.MILLIINTERNATIONAL_UNITS_PER_L,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "0.4 - 4.0",
            "history_seed": (1.8, 0.2),
        },
    ],
    BiomarkerCategoryEnum.VITAMINS_MINERALS: [
        {
            "metric": BiomarkerMetricName.VITAMIN_D,
            "value": 28.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.CRITICAL,
            "reference_range": "30 - 100",
            "history_seed": (28.0, 2.0),
        },
        {
            "metric": BiomarkerMetricName.VITAMIN_B12,
            "value": 450.0,
            "unit": MeasurementUnit.PICOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "200 - 900",
            "history_seed": (450.0, 50.0),
        },
        {
            "metric": BiomarkerMetricName.FERRITIN,
            "value": 45.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "30 - 400",
            "history_seed": (45.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.MAGNESIUM,
            "value": 2.1,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "1.7 - 2.2",
            "history_seed": (2.1, 0.1),
        },
    ],
    BiomarkerCategoryEnum.INFLAMMATION: [
        {
            "metric": BiomarkerMetricName.HS_CRP,
            "value": 0.8,
            "unit": MeasurementUnit.MILLIGRAMS_PER_LITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 1.0",
            "history_seed": (0.8, 0.3),
        },
        {
            "metric": BiomarkerMetricName.HOMOCYSTEINE,
            "value": 8.5,
            "unit": MeasurementUnit.MICROMOLES_PER_LITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 10.0",
            "history_seed": (8.5, 1.0),
        },
    ],
}


# Demo phone number for call logs API
DEMO_PHONE_NUMBER = "+12126804645"

__all__ = [
    "BIOMARKER_METRIC_DEMO_DATA",
    "ADMIN_NOTIFICATIONS_DEMO",
    "PATIENT_NOTIFICATIONS_DEMO",
    "DEMO_PATIENTS",
    "DEMO_PHONE_NUMBER",
]


# =============================================================================
# Notification Demo Data
# =============================================================================

ADMIN_NOTIFICATIONS_DEMO: list[dict] = [
    {
        "id": "1",
        "title": "New Patient Registration",
        "message": "Sarah Chen has completed registration and requires initial assessment scheduling.",
        "type": "info",
        "is_read": False,
        "created_at": "2025-01-15T09:30:00",
        "recipient_role": "admin",
        "patient_id": "P001"
    },
    {
        "id": "2",
        "title": "Lab Results Ready",
        "message": "Comprehensive metabolic panel results for Marcus Williams are now available for review.",
        "type": "lab",
        "is_read": False,
        "created_at": "2025-01-15T08:45:00",
        "recipient_role": "admin",
        "patient_id": "P002"
    },
    {
        "id": "3",
        "title": "Treatment Protocol Update Required",
        "message": "NMN + Resveratrol protocol needs adjustment based on latest research findings.",
        "type": "treatment",
        "is_read": True,
        "created_at": "2025-01-14T16:20:00",
        "recipient_role": "admin",
        "patient_id": None
    },
    {
        "id": "4",
        "title": "Appointment Rescheduling Request",
        "message": "Elena Rodriguez requested to reschedule tomorrow's hyperbaric oxygen session.",
        "type": "appointment",
        "is_read": False,
        "created_at": "2025-01-15T07:00:00",
        "recipient_role": "admin",
        "patient_id": "P003"
    },
    {
        "id": "5",
        "title": "Critical: Low Inventory Alert",
        "message": "NAD+ IV therapy supplies are running low. Reorder recommended within 48 hours.",
        "type": "warning",
        "is_read": False,
        "created_at": "2025-01-15T06:00:00",
        "recipient_role": "admin",
        "patient_id": None
    },
    {
        "id": "6",
        "title": "Monthly Report Generated",
        "message": "December 2024 clinical efficiency report is ready for download.",
        "type": "success",
        "is_read": True,
        "created_at": "2025-01-01T00:00:00",
        "recipient_role": "admin",
        "patient_id": None
    }
]

PATIENT_NOTIFICATIONS_DEMO: list[dict] = [
    {
        "id": "101",
        "title": "Upcoming Appointment Reminder",
        "message": "Your NAD+ IV Therapy session is scheduled for tomorrow at 10:00 AM.",
        "type": "appointment",
        "is_read": False,
        "created_at": "2025-01-15T09:00:00",
        "recipient_role": "patient",
        "patient_id": "current"
    },
    {
        "id": "102",
        "title": "Lab Results Available",
        "message": "Your comprehensive metabolic panel results are now ready. Click to view detailed analysis.",
        "type": "lab",
        "is_read": False,
        "created_at": "2025-01-14T14:30:00",
        "recipient_role": "patient",
        "patient_id": "current"
    },
    {
        "id": "103",
        "title": "Treatment Plan Updated",
        "message": "Dr. Johnson has updated your longevity protocol. Review the changes in your treatment plan.",
        "type": "treatment",
        "is_read": True,
        "created_at": "2025-01-13T11:00:00",
        "recipient_role": "patient",
        "patient_id": "current"
    },
    {
        "id": "104",
        "title": "Biomarker Improvement",
        "message": "Great news! Your telomere length has improved by 8% since your last assessment.",
        "type": "success",
        "is_read": True,
        "created_at": "2025-01-10T15:45:00",
        "recipient_role": "patient",
        "patient_id": "current"
    },
    {
        "id": "105",
        "title": "Supplement Reminder",
        "message": "Don't forget to take your NMN and Resveratrol supplements with breakfast.",
        "type": "info",
        "is_read": True,
        "created_at": "2025-01-15T07:00:00",
        "recipient_role": "patient",
        "patient_id": "current"
    }
]


# =============================================================================
# Patient Demo Data
# =============================================================================

DEMO_PATIENTS: list[dict] = [
    {"id": "P001", "name": "Sarah Chen", "email": "sarah.chen@example.com"},
    {"id": "P002", "name": "Marcus Williams", "email": "marcus.w@example.com"},
    {"id": "P003", "name": "Elena Rodriguez", "email": "elena.r@example.com"},
    {"id": "P004", "name": "James Miller", "email": "james.m@example.com"},
    {"id": "P005", "name": "Emily Wong", "email": "emily.w@example.com"},
]
