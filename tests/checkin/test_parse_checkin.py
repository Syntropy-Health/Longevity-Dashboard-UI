"""Integration tests for VlogsAgent parsing and health data extraction.

Tests parse_checkin_with_health_data with mocked LLM responses to validate
the complete parsing pipeline without actual API calls.
"""

from unittest.mock import AsyncMock, patch

import pytest

from longevity_clinic.app.config import VlogsConfig
from longevity_clinic.app.data.process_schema import (
    CheckInSummary,
    MetricLogsOutput,
)
from longevity_clinic.app.data.state_schemas import (
    FoodEntry as FoodEntrySchema,
    MedicationEntry as MedicationEntrySchema,
    Symptom as SymptomSchema,
)
from longevity_clinic.app.functions.vlogs import VlogsAgent


def create_llm_mock_response(
    checkin_id: str = "chk_test123",
    checkin_type: str = "voice",
    summary: str = "Patient reports feeling well",
    medications: list = None,
    foods: list = None,
    symptoms: list = None,
) -> MetricLogsOutput:
    """Create a mock LLM response for testing."""
    return MetricLogsOutput(
        checkin=CheckInSummary(
            id=checkin_id,
            type=checkin_type,
            summary=summary,
            timestamp="Today, 10:30 AM",
            sentiment="neutral",
            key_topics=["wellness", "medication"],
            provider_reviewed=False,
            patient_name="Test Patient",
        ),
        medications_entries=medications or [],
        food_entries=foods or [],
        symptom_entries=symptoms or [],
    )


class TestParseCheckinWithHealthData:
    """Test VlogsAgent.parse_checkin_with_health_data."""

    @pytest.mark.asyncio
    async def test_parse_extracts_medications(self):
        """Verify medications are extracted from transcript."""
        mock_meds = [
            MedicationEntrySchema(
                id="med_1",
                name="Metformin",
                dosage="500mg",
                frequency="twice daily",
                status="active",
            ),
            MedicationEntrySchema(
                id="med_2",
                name="Vitamin D",
                dosage="2000IU",
                frequency="daily",
            ),
        ]

        mock_response = create_llm_mock_response(
            summary="Patient taking metformin and vitamin D supplements",
            medications=mock_meds,
        )

        with patch(
            "longevity_clinic.app.functions.vlogs.agent.parse_with_structured_output",
            new_callable=AsyncMock,
        ) as mock_parse:
            mock_parse.return_value = mock_response

            result = await VlogsAgent.parse_checkin_with_health_data(
                content="I took my metformin 500mg and vitamin D this morning",
                checkin_type="voice",
            )

        assert len(result.medications_entries) == 2
        assert result.medications_entries[0].name == "Metformin"
        assert result.medications_entries[0].dosage == "500mg"
        assert result.medications_entries[1].name == "Vitamin D"

    @pytest.mark.asyncio
    async def test_parse_extracts_food_entries(self):
        """Verify food entries are extracted from transcript."""
        mock_foods = [
            FoodEntrySchema(
                id="food_1",
                name="Oatmeal with blueberries",
                calories=300,
                protein=10.0,
                carbs=50.0,
                fat=5.0,
                meal_type="breakfast",
            ),
        ]

        mock_response = create_llm_mock_response(
            summary="Patient had oatmeal for breakfast",
            foods=mock_foods,
        )

        with patch(
            "longevity_clinic.app.functions.vlogs.agent.parse_with_structured_output",
            new_callable=AsyncMock,
        ) as mock_parse:
            mock_parse.return_value = mock_response

            result = await VlogsAgent.parse_checkin_with_health_data(
                content="Had oatmeal with blueberries for breakfast, about 300 calories",
                checkin_type="voice",
            )

        assert len(result.food_entries) == 1
        assert result.food_entries[0].name == "Oatmeal with blueberries"
        assert result.food_entries[0].calories == 300
        assert result.food_entries[0].meal_type == "breakfast"

    @pytest.mark.asyncio
    async def test_parse_extracts_symptoms(self):
        """Verify symptoms are extracted from transcript."""
        mock_symptoms = [
            SymptomSchema(
                id="sym_1",
                name="Headache",
                severity="mild",
                frequency="occasional",
                trend="stable",
            ),
            SymptomSchema(
                id="sym_2",
                name="Fatigue",
                severity="moderate",
                frequency="daily",
                trend="improving",
            ),
        ]

        mock_response = create_llm_mock_response(
            summary="Patient reports headaches and fatigue",
            symptoms=mock_symptoms,
        )

        with patch(
            "longevity_clinic.app.functions.vlogs.agent.parse_with_structured_output",
            new_callable=AsyncMock,
        ) as mock_parse:
            mock_parse.return_value = mock_response

            result = await VlogsAgent.parse_checkin_with_health_data(
                content="Been having mild headaches and some fatigue lately",
                checkin_type="voice",
            )

        assert len(result.symptom_entries) == 2
        assert result.symptom_entries[0].name == "Headache"
        assert result.symptom_entries[0].severity == "mild"
        assert result.symptom_entries[1].name == "Fatigue"
        assert result.symptom_entries[1].trend == "improving"

    @pytest.mark.asyncio
    async def test_parse_empty_content_returns_fallback(self):
        """Verify empty/short content returns fallback output without LLM call."""
        result = await VlogsAgent.parse_checkin_with_health_data(
            content="hi",  # Too short
            checkin_type="text",
        )

        # Should return empty output without calling LLM
        assert len(result.medications_entries) == 0
        assert len(result.food_entries) == 0
        assert len(result.symptom_entries) == 0
        assert result.checkin.type == "text"

    @pytest.mark.asyncio
    async def test_parse_llm_failure_returns_fallback(self):
        """Verify LLM failure returns fallback output."""
        with patch(
            "longevity_clinic.app.functions.vlogs.agent.parse_with_structured_output",
            new_callable=AsyncMock,
        ) as mock_parse:
            mock_parse.return_value = None  # LLM failed

            result = await VlogsAgent.parse_checkin_with_health_data(
                content="This is a normal length check-in transcript that should trigger LLM",
                checkin_type="voice",
            )

        # Should return fallback with empty health data
        assert len(result.medications_entries) == 0
        assert len(result.food_entries) == 0
        assert len(result.symptom_entries) == 0
        # Summary should be truncated content
        assert "check-in transcript" in result.checkin.summary


class TestVlogsAgentConfig:
    """Test VlogsAgent configuration and initialization."""

    def test_agent_with_llm_disabled_skips_initialization(self):
        """Verify agent with LLM disabled doesn't initialize LLM client."""
        config = VlogsConfig(extract_with_llm=False)
        agent = VlogsAgent(config=config)
        assert agent.config.extract_with_llm is False
        assert agent._structured_llm is None
