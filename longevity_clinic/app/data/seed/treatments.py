"""Treatment seed data for the Longevity Clinic.

Contains:
- Treatment catalog (full definitions for Treatment model)
- Treatment protocol metrics (for admin dashboard charts)
- Portal treatments (patient-facing view)
"""

from __future__ import annotations

from typing import List


# =============================================================================
# Treatment Catalog Seed Data (for Treatment model)
# =============================================================================

TREATMENT_CATALOG_SEED: List[dict] = [
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
]


# =============================================================================
# Treatment Protocol Metrics Seed (for admin dashboard charts)
# =============================================================================

TREATMENT_PROTOCOL_METRICS_SEED: List[dict] = [
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
# Treatment Chart Data (simple count format for charts)
# =============================================================================

TREATMENT_CHART_SEED: List[dict] = [
    {"name": "IV Therapy", "count": 45},
    {"name": "Cryo", "count": 30},
    {"name": "Supplements", "count": 85},
    {"name": "Hormone", "count": 25},
    {"name": "Physio", "count": 15},
]


# =============================================================================
# Portal Treatments Seed (patient-facing view)
# =============================================================================

PORTAL_TREATMENTS_SEED: List[dict] = [
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


__all__ = [
    "TREATMENT_CATALOG_SEED",
    "TREATMENT_PROTOCOL_METRICS_SEED",
    "TREATMENT_CHART_SEED",
    "PORTAL_TREATMENTS_SEED",
]
