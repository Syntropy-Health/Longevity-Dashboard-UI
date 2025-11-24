import reflex as rx


class AnalyticsState(rx.State):
    """
    State for Analytics Dashboards (Admin & Patient).
    Contains mock data for charts and modal logic.
    """

    operational_data: list[dict[str, str | int]] = [
        {"month": "Jan", "patients": 120, "requests": 45, "approvals": 40},
        {"month": "Feb", "patients": 132, "requests": 52, "approvals": 48},
        {"month": "Mar", "patients": 145, "requests": 61, "approvals": 55},
        {"month": "Apr", "patients": 155, "requests": 58, "approvals": 50},
        {"month": "May", "patients": 168, "requests": 72, "approvals": 68},
        {"month": "Jun", "patients": 180, "requests": 85, "approvals": 80},
    ]
    protocol_usage_data: list[dict[str, str | int]] = [
        {"name": "NAD+ IV", "count": 145, "effectiveness": 88},
        {"name": "Peptides", "count": 89, "effectiveness": 76},
        {"name": "Hyperbaric", "count": 64, "effectiveness": 92},
        {"name": "Cryo", "count": 45, "effectiveness": 65},
        {"name": "Sauna", "count": 110, "effectiveness": 82},
    ]
    biomarker_history: list[dict[str, str | float]] = [
        {"date": "Sep", "NAD": 22.0, "hsCRP": 1.2, "Cortisol": 18.5, "VitaminD": 35.0},
        {"date": "Oct", "NAD": 24.5, "hsCRP": 1.0, "Cortisol": 17.0, "VitaminD": 38.5},
        {"date": "Nov", "NAD": 28.0, "hsCRP": 0.8, "Cortisol": 16.2, "VitaminD": 44.0},
        {"date": "Dec", "NAD": 31.5, "hsCRP": 0.6, "Cortisol": 15.5, "VitaminD": 52.0},
        {"date": "Jan", "NAD": 35.0, "hsCRP": 0.4, "Cortisol": 14.0, "VitaminD": 58.0},
        {"date": "Feb", "NAD": 38.2, "hsCRP": 0.3, "Cortisol": 12.5, "VitaminD": 65.0},
    ]
    biomarker_improvement_data: list[dict[str, str | int]] = [
        {"category": "NAD+", "improvement": 45},
        {"category": "Inflammation", "improvement": 32},
        {"category": "Metabolic", "improvement": 28},
        {"category": "Hormones", "improvement": 15},
        {"category": "Vitamin D", "improvement": 55},
        {"category": "Lipids", "improvement": 12},
    ]
    biomarker_categories: list[str] = [
        "Complete Blood Count (CBC)",
        "Metabolic Panel",
        "Lipid Panel",
        "Hormones",
        "Vitamins & Minerals",
        "Inflammation",
    ]
    comprehensive_biomarkers: dict[str, list[dict]] = {
        "Complete Blood Count (CBC)": [
            {
                "name": "Red Blood Cells",
                "category": "Complete Blood Count (CBC)",
                "value": 5.2,
                "unit": "M/uL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Oxygen carrying capacity",
            },
            {
                "name": "Hemoglobin",
                "category": "Complete Blood Count (CBC)",
                "value": 15.5,
                "unit": "g/dL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Protein in red blood cells",
            },
            {
                "name": "Hematocrit",
                "category": "Complete Blood Count (CBC)",
                "value": 46.0,
                "unit": "%",
                "status": "Optimal",
                "trend": "up",
                "description": "Volume percentage of RBCs",
            },
            {
                "name": "White Blood Cells",
                "category": "Complete Blood Count (CBC)",
                "value": 6.8,
                "unit": "K/uL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Immune system status",
            },
        ],
        "Metabolic Panel": [
            {
                "name": "Glucose (Fasting)",
                "category": "Metabolic Panel",
                "value": 88.0,
                "unit": "mg/dL",
                "status": "Optimal",
                "trend": "down",
                "description": "Blood sugar levels",
            },
            {
                "name": "HbA1c",
                "category": "Metabolic Panel",
                "value": 5.1,
                "unit": "%",
                "status": "Optimal",
                "trend": "down",
                "description": "Average blood sugar over 3 months",
            },
            {
                "name": "Creatinine",
                "category": "Metabolic Panel",
                "value": 0.95,
                "unit": "mg/dL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Kidney function indicator",
            },
        ],
        "Lipid Panel": [
            {
                "name": "Total Cholesterol",
                "category": "Lipid Panel",
                "value": 185.0,
                "unit": "mg/dL",
                "status": "Warning",
                "trend": "down",
                "description": "Overall cholesterol measure",
            },
            {
                "name": "LDL Cholesterol",
                "category": "Lipid Panel",
                "value": 110.0,
                "unit": "mg/dL",
                "status": "Warning",
                "trend": "down",
                "description": "'Bad' cholesterol",
            },
            {
                "name": "HDL Cholesterol",
                "category": "Lipid Panel",
                "value": 65.0,
                "unit": "mg/dL",
                "status": "Optimal",
                "trend": "up",
                "description": "'Good' cholesterol",
            },
            {
                "name": "Triglycerides",
                "category": "Lipid Panel",
                "value": 85.0,
                "unit": "mg/dL",
                "status": "Optimal",
                "trend": "down",
                "description": "Fat in the blood",
            },
        ],
        "Hormones": [
            {
                "name": "Testosterone (Total)",
                "category": "Hormones",
                "value": 750.0,
                "unit": "ng/dL",
                "status": "Optimal",
                "trend": "up",
                "description": "Primary male sex hormone",
            },
            {
                "name": "Free Testosterone",
                "category": "Hormones",
                "value": 15.5,
                "unit": "ng/dL",
                "status": "Optimal",
                "trend": "up",
                "description": "Bioavailable testosterone",
            },
            {
                "name": "Cortisol (AM)",
                "category": "Hormones",
                "value": 12.5,
                "unit": "ug/dL",
                "status": "Optimal",
                "trend": "down",
                "description": "Stress hormone levels",
            },
            {
                "name": "TSH",
                "category": "Hormones",
                "value": 2.1,
                "unit": "mIU/L",
                "status": "Optimal",
                "trend": "stable",
                "description": "Thyroid stimulating hormone",
            },
        ],
        "Vitamins & Minerals": [
            {
                "name": "Vitamin D",
                "category": "Vitamins & Minerals",
                "value": 65.0,
                "unit": "ng/mL",
                "status": "Optimal",
                "trend": "up",
                "description": "Bone & immune health",
            },
            {
                "name": "Vitamin B12",
                "category": "Vitamins & Minerals",
                "value": 850.0,
                "unit": "pg/mL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Nerve & blood cell health",
            },
            {
                "name": "Magnesium (RBC)",
                "category": "Vitamins & Minerals",
                "value": 6.2,
                "unit": "mg/dL",
                "status": "Optimal",
                "trend": "stable",
                "description": "Cellular magnesium levels",
            },
            {
                "name": "Ferritin",
                "category": "Vitamins & Minerals",
                "value": 150.0,
                "unit": "ng/mL",
                "status": "Optimal",
                "trend": "down",
                "description": "Iron storage protein",
            },
        ],
        "Inflammation": [
            {
                "name": "hs-CRP",
                "category": "Inflammation",
                "value": 0.3,
                "unit": "mg/L",
                "status": "Optimal",
                "trend": "down",
                "description": "Systemic inflammation marker",
            },
            {
                "name": "Homocysteine",
                "category": "Inflammation",
                "value": 7.5,
                "unit": "umol/L",
                "status": "Optimal",
                "trend": "down",
                "description": "Amino acid linked to heart disease",
            },
            {
                "name": "NAD+",
                "category": "Inflammation",
                "value": 38.2,
                "unit": "uM",
                "status": "Optimal",
                "trend": "up",
                "description": "Cellular energy & repair",
            },
        ],
    }
    active_chart_index: int = -1
    detail_modal_open: bool = False
    detail_title: str = ""
    detail_type: str = ""

    @rx.event
    def set_active_index(self, index: int):
        self.active_chart_index = index

    @rx.event
    def clear_active_index(self):
        self.active_chart_index = -1

    @rx.event
    def open_detail_modal(self, title: str, type_: str):
        self.detail_title = title
        self.detail_type = type_
        self.detail_modal_open = True

    @rx.event
    def close_detail_modal(self):
        self.detail_modal_open = False

    @rx.event
    def handle_detail_modal_open_change(self, is_open: bool):
        if not is_open:
            self.close_detail_modal()