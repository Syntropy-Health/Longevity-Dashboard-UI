"""Treatment seed data for the Longevity Clinic.

Uses dict format compatible with SQLModel.model_validate() for type safety.
"""

from __future__ import annotations

# =============================================================================
# Treatment Catalog - Compatible with Treatment.model_validate()
# =============================================================================

TREATMENT_CATALOG_SEED: list[dict] = [
    {
        "treatment_id": "T001",
        "name": "Vitamin C IV Mega-Dose",
        "category": "IV Therapy",
        "description": "High-dose Vitamin C infusion to boost immune system and antioxidant levels.",
        "duration": "60 mins",
        "frequency": "Weekly",
        "cost": 150.0,
        "status": "Active",
    },
    {
        "treatment_id": "T002",
        "name": "Whole Body Cryotherapy",
        "category": "Cryotherapy",
        "description": "Exposure to ultra-low temperatures to reduce inflammation and improve recovery.",
        "duration": "3 mins",
        "frequency": "Daily",
        "cost": 45.0,
        "status": "Active",
    },
    {
        "treatment_id": "T003",
        "name": "NAD+ Optimization",
        "category": "Supplements",
        "description": "Supplement protocol to enhance cellular energy and DNA repair.",
        "duration": "N/A",
        "frequency": "Daily",
        "cost": 120.0,
        "status": "Active",
    },
    {
        "treatment_id": "T004",
        "name": "Testosterone Replacement",
        "category": "Hormone Therapy",
        "description": "Bio-identical hormone replacement for optimal levels.",
        "duration": "15 mins",
        "frequency": "Monthly",
        "cost": 200.0,
        "status": "Active",
    },
    {
        "treatment_id": "T005",
        "name": "Deep Tissue Massage",
        "category": "Spa Services",
        "description": "Therapeutic massage focusing on realigning deeper layers of muscles.",
        "duration": "60 mins",
        "frequency": "As-needed",
        "cost": 90.0,
        "status": "Active",
    },
    {
        "treatment_id": "T006",
        "name": "Hyperbaric Oxygen Therapy (HBOT)",
        "category": "Oxygen Therapy",
        "description": "Breathing pure oxygen in a pressurized chamber to enhance tissue healing.",
        "duration": "90 mins",
        "frequency": "Weekly",
        "cost": 250.0,
        "status": "Active",
    },
    {
        "treatment_id": "T007",
        "name": "Ozone Therapy",
        "category": "IV Therapy",
        "description": "Medical ozone infusion to support immune function and oxygenation.",
        "duration": "45 mins",
        "frequency": "Bi-weekly",
        "cost": 175.0,
        "status": "Active",
    },
    {
        "treatment_id": "T008",
        "name": "Magnesium Glycinate Protocol",
        "category": "Supplements",
        "description": "High-absorption magnesium supplementation for stress and sleep support.",
        "duration": "N/A",
        "frequency": "Daily",
        "cost": 45.0,
        "status": "Active",
    },
    {
        "treatment_id": "T009",
        "name": "Peptide Therapy - BPC-157",
        "category": "Peptide Therapy",
        "description": "Regenerative peptide protocol for tissue repair and gut health.",
        "duration": "15 mins",
        "frequency": "Daily",
        "cost": 300.0,
        "status": "Active",
    },
    {
        "treatment_id": "T010",
        "name": "Red Light Therapy Panel",
        "category": "Light Therapy",
        "description": "Near-infrared and red light exposure for cellular regeneration.",
        "duration": "20 mins",
        "frequency": "Daily",
        "cost": 35.0,
        "status": "Active",
    },
    # =========================================================================
    # Medications (Rx) - category = "Medications"
    # =========================================================================
    {
        "treatment_id": "T011",
        "name": "Metformin",
        "category": "Medications",
        "description": "Biguanide medication for blood sugar control and longevity benefits.",
        "duration": "N/A",
        "frequency": "Twice daily with meals",
        "cost": 15.0,
        "status": "Active",
    },
    {
        "treatment_id": "T012",
        "name": "Lisinopril",
        "category": "Medications",
        "description": "ACE inhibitor for blood pressure management and cardiovascular protection.",
        "duration": "N/A",
        "frequency": "Once daily in morning",
        "cost": 12.0,
        "status": "Active",
    },
    {
        "treatment_id": "T013",
        "name": "Vitamin D3",
        "category": "Medications",
        "description": "High-dose vitamin D supplementation for bone health and immune function.",
        "duration": "N/A",
        "frequency": "Once daily with food",
        "cost": 20.0,
        "status": "Active",
    },
    {
        "treatment_id": "T014",
        "name": "Omega-3 Fish Oil",
        "category": "Medications",
        "description": "Essential fatty acid supplementation for cardiovascular and brain health.",
        "duration": "N/A",
        "frequency": "Twice daily",
        "cost": 25.0,
        "status": "Active",
    },
    {
        "treatment_id": "T015",
        "name": "Magnesium Glycinate (Rx)",
        "category": "Medications",
        "description": "High-dose magnesium for sleep, relaxation, and muscle function.",
        "duration": "N/A",
        "frequency": "Once daily at bedtime",
        "cost": 18.0,
        "status": "Active",
    },
    {
        "treatment_id": "T016",
        "name": "CoQ10",
        "category": "Medications",
        "description": "Coenzyme Q10 for cellular energy production and heart health.",
        "duration": "N/A",
        "frequency": "Once daily with food",
        "cost": 35.0,
        "status": "Active",
    },
    {
        "treatment_id": "T017",
        "name": "Atorvastatin",
        "category": "Medications",
        "description": "Statin medication for cholesterol management and cardiovascular protection.",
        "duration": "N/A",
        "frequency": "Once daily at bedtime",
        "cost": 22.0,
        "status": "Active",
    },
]

# =============================================================================
# Treatment Protocol Metrics - Compatible with TreatmentProtocolMetric.model_validate()
# =============================================================================

TREATMENT_PROTOCOL_METRICS_SEED: list[dict] = [
    {
        "name": "IV Therapy",
        "category": "infusion",
        "active_count": 45,
        "completed_count": 120,
        "success_rate": 98.0,
        "avg_duration_days": 14,
    },
    {
        "name": "Cryo",
        "category": "therapy",
        "active_count": 30,
        "completed_count": 85,
        "success_rate": 95.0,
        "avg_duration_days": 7,
    },
    {
        "name": "Supplements",
        "category": "nutrition",
        "active_count": 85,
        "completed_count": 200,
        "success_rate": 97.0,
        "avg_duration_days": 90,
    },
    {
        "name": "Hormone",
        "category": "therapy",
        "active_count": 25,
        "completed_count": 60,
        "success_rate": 92.0,
        "avg_duration_days": 60,
    },
    {
        "name": "Physio",
        "category": "therapy",
        "active_count": 15,
        "completed_count": 45,
        "success_rate": 96.0,
        "avg_duration_days": 30,
    },
]

# =============================================================================
# Treatment Chart Data (for admin dashboard)
# =============================================================================

TREATMENT_CHART_SEED: list[dict] = [
    {"name": "IV Therapy", "count": 45},
    {"name": "Cryo", "count": 30},
    {"name": "Supplements", "count": 85},
    {"name": "Hormone", "count": 25},
    {"name": "Physio", "count": 15},
]

# =============================================================================
# Portal Treatments (patient portal display)
# =============================================================================

PORTAL_TREATMENTS_SEED: list[dict] = [
    {
        "id": "t1",
        "name": "Vitamin C IV Drip",
        "frequency": "Weekly",
        "duration": "45 mins",
        "category": "IV Therapy",
        "status": "Active",
    },
    {
        "id": "t2",
        "name": "Cryotherapy Session",
        "frequency": "Bi-Weekly",
        "duration": "10 mins",
        "category": "Recovery",
        "status": "Active",
    },
    {
        "id": "t3",
        "name": "Magnesium Supplementation",
        "frequency": "Daily",
        "duration": "Ongoing",
        "category": "Supplements",
        "status": "Active",
    },
]

# =============================================================================
# Patient Treatment Assignments - Compatible with PatientTreatment.model_validate()
# Note: user_id and treatment_id (DB FKs) resolved at load time from external IDs
# =============================================================================

PATIENT_TREATMENT_ASSIGNMENTS_SEED: list[dict] = [
    # Sarah Chen (P001) - 3 active treatments
    {
        "patient_external_id": "P001",
        "treatment_id": "T001",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Weekly sessions for immune support",
        "sessions_completed": 6,
        "sessions_total": 12,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T003",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Daily supplementation for cellular energy",
        "sessions_completed": 30,
        "sessions_total": 90,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T008",
        "assigned_by": "Dr. Williams",
        "status": "active",
        "notes": "For stress management and sleep quality",
        "sessions_completed": 45,
        "sessions_total": None,
    },
    # Marcus Williams (P002) - 2 active treatments
    {
        "patient_external_id": "P002",
        "treatment_id": "T002",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Post-workout recovery sessions",
        "sessions_completed": 12,
        "sessions_total": 24,
    },
    {
        "patient_external_id": "P002",
        "treatment_id": "T004",
        "assigned_by": "Dr. Williams",
        "status": "active",
        "notes": "Monthly hormone optimization",
        "sessions_completed": 3,
        "sessions_total": 12,
    },
    # Elena Rodriguez (P003) - 3 active treatments
    {
        "patient_external_id": "P003",
        "treatment_id": "T006",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Cognitive enhancement protocol",
        "sessions_completed": 8,
        "sessions_total": 20,
    },
    {
        "patient_external_id": "P003",
        "treatment_id": "T010",
        "assigned_by": "Dr. Williams",
        "status": "active",
        "notes": "Daily skin and cellular regeneration",
        "sessions_completed": 28,
        "sessions_total": 60,
    },
    {
        "patient_external_id": "P003",
        "treatment_id": "T003",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Anti-aging and energy protocol",
        "sessions_completed": 60,
        "sessions_total": 90,
    },
    # James Miller (P004) - 2 active treatments (diabetes pre-cursor focus)
    {
        "patient_external_id": "P004",
        "treatment_id": "T001",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Metabolic support and antioxidant therapy",
        "sessions_completed": 4,
        "sessions_total": 12,
    },
    {
        "patient_external_id": "P004",
        "treatment_id": "T008",
        "assigned_by": "Dr. Williams",
        "status": "active",
        "notes": "Blood sugar regulation support",
        "sessions_completed": 21,
        "sessions_total": None,
    },
    # Emily Wong (P005 - onboarding) - 1 active treatment
    {
        "patient_external_id": "P005",
        "treatment_id": "T009",
        "assigned_by": "Dr. Johnson",
        "status": "active",
        "notes": "Initial gut health protocol for anemia",
        "sessions_completed": 2,
        "sessions_total": 30,
    },
    # =========================================================================
    # Sarah Chen (P001) - Medication Prescriptions (category=Medications)
    # These replace the old MedicationSubscription model
    # =========================================================================
    {
        "patient_external_id": "P001",
        "treatment_id": "T011",  # Metformin
        "assigned_by": "Dr. Sarah Johnson",
        "status": "active",
        "notes": "Take with breakfast and dinner. Monitor blood sugar levels.",
        "dosage": "500mg",
        "instructions": "Take with breakfast and dinner. Monitor blood sugar levels.",
        "adherence_rate": 96.0,
        "sessions_completed": 180,  # ~6 months daily
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T012",  # Lisinopril
        "assigned_by": "Dr. Michael Chen",
        "status": "active",
        "notes": "Take first thing in the morning on an empty stomach.",
        "dosage": "10mg",
        "instructions": "Take first thing in the morning on an empty stomach.",
        "adherence_rate": 92.0,
        "sessions_completed": 365,  # ~1 year daily
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T013",  # Vitamin D3
        "assigned_by": "Dr. Emily Davis",
        "status": "active",
        "notes": "Take with a meal containing fat for better absorption.",
        "dosage": "5000 IU",
        "instructions": "Take with a meal containing fat for better absorption.",
        "adherence_rate": 88.0,
        "sessions_completed": 90,  # 3 months
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T014",  # Omega-3 Fish Oil
        "assigned_by": "Dr. Emily Davis",
        "status": "active",
        "notes": "Take with meals to reduce fishy aftertaste.",
        "dosage": "1200mg",
        "instructions": "Take with meals to reduce fishy aftertaste.",
        "adherence_rate": 85.0,
        "sessions_completed": 120,  # 4 months
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T015",  # Magnesium Glycinate (Rx)
        "assigned_by": "Dr. Emily Davis",
        "status": "active",
        "notes": "Take before bed to promote relaxation and sleep.",
        "dosage": "400mg",
        "instructions": "Take before bed to promote relaxation and sleep.",
        "adherence_rate": 90.0,
        "sessions_completed": 60,  # 2 months
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T016",  # CoQ10
        "assigned_by": "Dr. Michael Chen",
        "status": "active",
        "notes": "Take with a fatty meal for optimal absorption.",
        "dosage": "100mg",
        "instructions": "Take with a fatty meal for optimal absorption.",
        "adherence_rate": 82.0,
        "sessions_completed": 45,  # 1.5 months
        "sessions_total": None,
    },
    {
        "patient_external_id": "P001",
        "treatment_id": "T017",  # Atorvastatin
        "assigned_by": "Dr. Sarah Johnson",
        "status": "paused",
        "notes": "Take at the same time each night. Avoid grapefruit.",
        "dosage": "20mg",
        "instructions": "Take at the same time each night. Avoid grapefruit.",
        "adherence_rate": 78.0,
        "sessions_completed": 30,  # 1 month
        "sessions_total": None,
    },
]

__all__ = [
    "PATIENT_TREATMENT_ASSIGNMENTS_SEED",
    "PORTAL_TREATMENTS_SEED",
    "TREATMENT_CATALOG_SEED",
    "TREATMENT_CHART_SEED",
    "TREATMENT_PROTOCOL_METRICS_SEED",
]
