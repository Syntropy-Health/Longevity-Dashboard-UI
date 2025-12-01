import reflex as rx
from typing import TypedDict, Optional
import random
from datetime import datetime, timedelta


class Patient(TypedDict):
    id: str
    full_name: str
    email: str
    phone: str
    age: int
    gender: str
    last_visit: str
    status: str
    biomarker_score: int
    medical_history: str
    next_appointment: str
    assigned_treatments: list[dict]


class ChartData(TypedDict):
    name: str
    value: int
    value2: int


class PatientState(rx.State):
    patients: list[Patient] = [
        {
            "id": "P001",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "(555) 123-4567",
            "age": 45,
            "gender": "Male",
            "last_visit": "2023-10-15",
            "status": "Active",
            "biomarker_score": 85,
            "medical_history": "Hypertension, Vitamin D deficiency",
            "next_appointment": "2023-11-20",
            "assigned_treatments": [],
        },
        {
            "id": "P002",
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "(555) 987-6543",
            "age": 38,
            "gender": "Female",
            "last_visit": "2023-10-28",
            "status": "Active",
            "biomarker_score": 92,
            "medical_history": "None",
            "next_appointment": "2023-11-15",
            "assigned_treatments": [],
        },
        {
            "id": "P003",
            "full_name": "Robert Johnson",
            "email": "robert.j@example.com",
            "phone": "(555) 456-7890",
            "age": 52,
            "gender": "Male",
            "last_visit": "2023-09-10",
            "status": "Inactive",
            "biomarker_score": 68,
            "medical_history": "Type 2 Diabetes Pre-cursor",
            "next_appointment": "Pending",
            "assigned_treatments": [],
        },
        {
            "id": "P004",
            "full_name": "Emily Davis",
            "email": "emily.d@example.com",
            "phone": "(555) 222-3333",
            "age": 29,
            "gender": "Female",
            "last_visit": "2023-11-01",
            "status": "Onboarding",
            "biomarker_score": 0,
            "medical_history": "Anemia",
            "next_appointment": "2023-11-12",
            "assigned_treatments": [],
        },
        {
            "id": "P005",
            "full_name": "Michael Wilson",
            "email": "michael.w@example.com",
            "phone": "(555) 444-5555",
            "age": 61,
            "gender": "Male",
            "last_visit": "2023-10-05",
            "status": "Active",
            "biomarker_score": 74,
            "medical_history": "High Cholesterol",
            "next_appointment": "2023-11-25",
            "assigned_treatments": [],
        },
    ]
    search_query: str = ""
    status_filter: str = "All"
    sort_key: str = "name"
    is_add_patient_open: bool = False
    is_view_patient_open: bool = False
    selected_patient: Optional[Patient] = None
    new_patient_name: str = ""
    new_patient_email: str = ""
    new_patient_phone: str = ""
    new_patient_age: str = ""
    new_patient_gender: str = ""
    new_patient_history: str = ""
    trend_data: list[dict] = [
        {"name": "Jan", "active": 120, "new": 15},
        {"name": "Feb", "active": 132, "new": 18},
        {"name": "Mar", "active": 145, "new": 20},
        {"name": "Apr", "active": 160, "new": 25},
        {"name": "May", "active": 178, "new": 22},
        {"name": "Jun", "active": 195, "new": 30},
    ]
    treatment_data: list[dict] = [
        {"name": "IV Therapy", "count": 45},
        {"name": "Cryo", "count": 30},
        {"name": "Supplements", "count": 85},
        {"name": "Hormone", "count": 25},
        {"name": "Physio", "count": 15},
    ]
    biomarker_data: list[dict] = [
        {"name": "Wk 1", "score": 65},
        {"name": "Wk 4", "score": 72},
        {"name": "Wk 8", "score": 78},
        {"name": "Wk 12", "score": 82},
        {"name": "Wk 16", "score": 88},
    ]

    @rx.var
    def filtered_patients(self) -> list[Patient]:
        patients = self.patients
        if self.status_filter != "All":
            patients = [
                p for p in patients if p["status"].lower() == self.status_filter.lower()
            ]
        if self.search_query:
            query = self.search_query.lower()
            patients = [
                p
                for p in patients
                if query in p["full_name"].lower() or query in p["email"].lower()
            ]
        if self.sort_key == "name":
            patients = sorted(patients, key=lambda x: x["full_name"])
        elif self.sort_key == "recent":
            patients = sorted(patients, key=lambda x: x["last_visit"], reverse=True)
        elif self.sort_key == "score":
            patients = sorted(
                patients, key=lambda x: x["biomarker_score"], reverse=True
            )
        return patients

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def set_sort_key(self, key: str):
        self.sort_key = key

    @rx.event
    def open_add_patient(self):
        self.is_add_patient_open = True

    @rx.event
    def close_add_patient(self):
        self.is_add_patient_open = False
        self.new_patient_name = ""
        self.new_patient_email = ""
        self.new_patient_phone = ""
        self.new_patient_age = ""
        self.new_patient_gender = ""
        self.new_patient_history = ""

    @rx.event
    def handle_add_patient_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.close_add_patient()

    @rx.event
    def open_view_patient(self, patient: Patient):
        self.selected_patient = patient
        self.is_view_patient_open = True

    @rx.event
    def close_view_patient(self):
        self.is_view_patient_open = False
        self.selected_patient = None

    @rx.event
    def handle_view_patient_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_view_patient_open = False
            self.selected_patient = None

    @rx.event
    def add_patient(self):
        new_id = f"P{random.randint(100, 999)}"
        new_patient: Patient = {
            "id": new_id,
            "full_name": self.new_patient_name,
            "email": self.new_patient_email,
            "phone": self.new_patient_phone,
            "age": int(self.new_patient_age) if self.new_patient_age.isdigit() else 0,
            "gender": self.new_patient_gender,
            "last_visit": datetime.now().strftime("%Y-%m-%d"),
            "status": "Onboarding",
            "biomarker_score": 0,
            "medical_history": self.new_patient_history,
            "next_appointment": (datetime.now() + timedelta(days=7)).strftime(
                "%Y-%m-%d"
            ),
            "assigned_treatments": [],
        }
        self.patients.append(new_patient)
        self.close_add_patient()

    @rx.event
    def set_new_patient_name(self, value: str):
        self.new_patient_name = value

    @rx.event
    def set_new_patient_email(self, value: str):
        self.new_patient_email = value

    @rx.event
    def set_new_patient_phone(self, value: str):
        self.new_patient_phone = value

    @rx.event
    def set_new_patient_age(self, value: str):
        self.new_patient_age = value

    @rx.event
    def set_new_patient_gender(self, value: str):
        self.new_patient_gender = value

    @rx.event
    def set_new_patient_history(self, value: str):
        self.new_patient_history = value

    @rx.event
    def assign_treatment_to_patient(self, patient_id: str, treatment: dict):
        for p in self.patients:
            if p["id"] == patient_id:
                if not any(
                    (
                        t["id"] == treatment["id"]
                        for t in p.get("assigned_treatments", [])
                    )
                ):
                    p.setdefault("assigned_treatments", []).append(treatment)
                break

    @rx.event
    def remove_treatment_from_patient(self, patient_id: str, treatment_id: str):
        for p in self.patients:
            if p["id"] == patient_id:
                p["assigned_treatments"] = [
                    t
                    for t in p.get("assigned_treatments", [])
                    if t["id"] != treatment_id
                ]
                break