import reflex as rx
from app.schemas.condition import Condition
from app.enums import ConditionStatus, ConditionSeverity


class ConditionState(rx.State):
    conditions: list[Condition] = [
        Condition(
            id="c1",
            name="Hypertension",
            description="High blood pressure that can lead to serious health problems.",
            status=ConditionStatus.ACTIVE,
            severity=ConditionSeverity.MILD,
            date_diagnosed="2023-04-12",
            last_updated="2023-04-12",
            icon="activity",
        ),
        Condition(
            id="c2",
            name="Asthma",
            description="A condition that affects the airways in the lungs, causing breathing difficulties.",
            status=ConditionStatus.ACTIVE,
            severity=ConditionSeverity.MODERATE,
            date_diagnosed="2023-03-18",
            last_updated="2023-03-18",
            icon="wind",
        ),
        Condition(
            id="c3",
            name="Migraine",
            description="A neurological condition characterized by intense, debilitating headaches.",
            status=ConditionStatus.ACTIVE,
            severity=ConditionSeverity.SEVERE,
            date_diagnosed="2023-05-05",
            last_updated="2023-05-05",
            icon="zap",
        ),
        Condition(
            id="c4",
            name="Hypothyroidism",
            description="A condition in which the thyroid gland doesn't produce enough thyroid hormone.",
            status=ConditionStatus.MANAGED,
            severity=ConditionSeverity.MILD,
            date_diagnosed="2023-01-30",
            last_updated="2023-01-30",
            icon="thermometer",
        ),
    ]
    filter_status: str = "All"

    @rx.var
    def filtered_conditions(self) -> list[Condition]:
        if self.filter_status == "All":
            return self.conditions
        return [c for c in self.conditions if c.status == self.filter_status]

    @rx.event
    def set_filter(self, status: str):
        self.filter_status = status

    @rx.event
    def add_condition(self):
        return rx.toast("Add Condition feature coming soon.")