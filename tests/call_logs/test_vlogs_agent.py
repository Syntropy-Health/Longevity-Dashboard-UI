"""Tests for VlogsAgent - call log processing with structured output.

Tests both simple parsing and LLM-based parsing modes.
Logs all outputs to test.log for validation.
"""

import asyncio
import logging
import os
from pathlib import Path
from datetime import datetime

import pytest

# Configure test logger to file
log_file = Path(__file__).parent.parent / "test.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="a"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("test_vlogs_agent")


# Sample test data
SAMPLE_TRANSCRIPT = """
AI: Hello! How are you feeling today?
User: I've been feeling tired lately, maybe for about two weeks now.
AI: I'm sorry to hear that. Can you tell me more about your fatigue?
User: Yes, I also have some joint pain in my knees. It's been bothering me when I walk.
AI: That's helpful to know. Are you taking any medications currently?
User: Just my blood pressure medication, lisinopril 10mg. I take it every morning.
AI: And how is your diet? Have you been eating well?
User: I had oatmeal for breakfast and a salad for lunch. Trying to eat healthy.
AI: That sounds good. Any other concerns?
User: No, that's about it. I just want to feel more energetic.
"""

SAMPLE_CALL_LOG = {
    "call_id": "test_123",
    "caller_phone": "+12126804645",
    "call_date": "2024-12-09T10:30:00Z",
    "call_duration": 180,
    "summary": "Patient reports fatigue and joint pain. Taking blood pressure medication.",
    "full_transcript": SAMPLE_TRANSCRIPT,
    "notes": "",
}


class TestVlogsAgentSimple:
    """Test VlogsAgent with simple (non-LLM) parsing."""

    @pytest.fixture
    def agent(self):
        """Create agent with simple parsing config."""
        from longevity_clinic.app.states.functions.vlogs_agent import (
            VlogsAgent,
            VlogsConfig,
        )

        return VlogsAgent(config=VlogsConfig(parse_with_llm=False))

    def test_config_defaults(self, agent):
        """Test default configuration values."""
        assert agent.config.parse_with_llm is False
        assert agent.config.llm_model == "gpt-4o-mini"
        assert agent.config.temperature == 0.3
        assert agent.config.limit == 50
        logger.info("✓ Config defaults validated")

    @pytest.mark.asyncio
    async def test_process_single_simple(self, agent):
        """Test processing a single call log with simple parsing."""
        from longevity_clinic.app.data.process_schema import CallLogsOutput

        output, summary = await agent.process_single(SAMPLE_CALL_LOG)

        # Validate output is correct type
        assert isinstance(output, CallLogsOutput)
        logger.info(f"Output type: {type(output).__name__}")

        # Validate checkin structure
        checkin = output.checkin
        assert checkin.id == "call_test_123"
        assert checkin.type == "call"
        assert len(checkin.summary) > 0
        assert checkin.sentiment == "neutral"
        assert "voice" in checkin.key_topics
        assert checkin.patient_name == "Demo Patient (Sarah Chen)"

        logger.info(f"CheckIn ID: {checkin.id}")
        logger.info(f"CheckIn Summary: {checkin.summary[:100]}...")
        logger.info(f"CheckIn Topics: {checkin.key_topics}")
        logger.info(f"CheckIn Patient: {checkin.patient_name}")

        # Validate summary dict
        assert summary["call_id"] == "test_123"
        assert summary["type"] == "call"
        logger.info(f"Summary dict: {summary}")

        logger.info("✓ Simple parsing test passed")

    @pytest.mark.asyncio
    async def test_output_to_dict(self, agent):
        """Test converting output to dict for state storage."""
        output, _ = await agent.process_single(SAMPLE_CALL_LOG)

        # Test to_checkin_dict
        checkin_dict = output.to_checkin_dict()
        assert isinstance(checkin_dict, dict)
        assert "id" in checkin_dict
        assert "summary" in checkin_dict
        assert "key_topics" in checkin_dict

        logger.info(f"Checkin dict keys: {list(checkin_dict.keys())}")
        logger.info("✓ Output to_dict conversion passed")

    @pytest.mark.asyncio
    async def test_medications_and_food_defaults(self, agent):
        """Test that simple parsing returns empty medications/food."""
        output, _ = await agent.process_single(SAMPLE_CALL_LOG)

        # Simple parsing doesn't extract medications/food
        assert output.medications == []
        assert output.food_entries == []
        assert output.has_medications is False
        assert output.has_nutrition is False

        logger.info("✓ Empty medications/food for simple parsing validated")


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set - skipping LLM tests",
)
class TestVlogsAgentLLM:
    """Test VlogsAgent with LLM parsing (requires API key)."""

    @pytest.fixture
    def agent(self):
        """Create agent with LLM parsing config."""
        from longevity_clinic.app.states.functions.vlogs_agent import (
            VlogsAgent,
            VlogsConfig,
        )

        return VlogsAgent(config=VlogsConfig(parse_with_llm=True))

    @pytest.mark.asyncio
    async def test_llm_structured_output(self, agent):
        """Test LLM produces structured CallLogsOutput."""
        from longevity_clinic.app.data.process_schema import CallLogsOutput

        logger.info("=" * 60)
        logger.info("Starting LLM structured output test")
        logger.info("=" * 60)

        output, summary = await agent.process_single(SAMPLE_CALL_LOG)

        # Validate output type
        assert isinstance(output, CallLogsOutput)
        logger.info(f"✓ Output is CallLogsOutput: {type(output).__name__}")

        # Log full output for validation
        logger.info("-" * 40)
        logger.info("CHECKIN DATA:")
        logger.info(f"  ID: {output.checkin.id}")
        logger.info(f"  Type: {output.checkin.type}")
        logger.info(f"  Summary: {output.checkin.summary}")
        logger.info(f"  Timestamp: {output.checkin.timestamp}")
        logger.info(f"  Sentiment: {output.checkin.sentiment}")
        logger.info(f"  Key Topics: {output.checkin.key_topics}")
        logger.info(f"  Provider Reviewed: {output.checkin.provider_reviewed}")
        logger.info(f"  Patient Name: {output.checkin.patient_name}")

        logger.info("-" * 40)
        logger.info("MEDICATIONS:")
        logger.info(f"  Has Medications: {output.has_medications}")
        logger.info(f"  Count: {len(output.medications)}")
        for med in output.medications:
            logger.info(f"    - {med.name}: {med.dosage} ({med.frequency})")

        logger.info("-" * 40)
        logger.info("FOOD ENTRIES:")
        logger.info(f"  Has Nutrition: {output.has_nutrition}")
        logger.info(f"  Count: {len(output.food_entries)}")
        for food in output.food_entries:
            logger.info(f"    - {food.name}: {food.calories} cal ({food.meal_type})")

        logger.info("-" * 40)
        logger.info("SUMMARY DICT:")
        logger.info(f"  {summary}")

        # Validate checkin has required fields
        assert output.checkin.id == "call_test_123"
        assert output.checkin.type == "call"
        assert len(output.checkin.summary) > 10
        assert output.checkin.sentiment in ["positive", "negative", "neutral"]
        assert isinstance(output.checkin.key_topics, list)

        logger.info("=" * 60)
        logger.info("✓ LLM structured output test PASSED")
        logger.info("=" * 60)

    @pytest.mark.asyncio
    async def test_llm_extracts_medications(self, agent):
        """Test LLM can extract medication information."""
        from longevity_clinic.app.data.state_schemas import Medication

        output, _ = await agent.process_single(SAMPLE_CALL_LOG)

        logger.info("Testing medication extraction...")

        if output.has_medications and output.medications:
            for med in output.medications:
                assert isinstance(med, Medication)
                assert med.name
                logger.info(f"Extracted medication: {med.model_dump()}")

        logger.info(f"has_medications: {output.has_medications}")
        logger.info(f"medications count: {len(output.medications)}")

    @pytest.mark.asyncio
    async def test_llm_extracts_food(self, agent):
        """Test LLM can extract food/nutrition information."""
        from longevity_clinic.app.data.state_schemas import FoodEntry

        output, _ = await agent.process_single(SAMPLE_CALL_LOG)

        logger.info("Testing food extraction...")

        if output.has_nutrition and output.food_entries:
            for food in output.food_entries:
                assert isinstance(food, FoodEntry)
                assert food.name
                logger.info(f"Extracted food: {food.model_dump()}")

        logger.info(f"has_nutrition: {output.has_nutrition}")
        logger.info(f"food_entries count: {len(output.food_entries)}")


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info(f"VlogsAgent Test Run - {datetime.now().isoformat()}")
    logger.info("=" * 60)

    pytest.main([__file__, "-v", "-s"])
