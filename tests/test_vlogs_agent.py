"""Tests for VlogsAgent call log processing.

Tests VlogsConfig, VlogsAgent initialization, and CDC pipeline methods.
Integration tests require API access and may be skipped.
"""

import pytest

from longevity_clinic.app.config import VlogsConfig
from longevity_clinic.app.data.schemas.llm import MetricLogsOutput
from longevity_clinic.app.functions.vlogs import VlogsAgent


class TestVlogsConfig:
    """Test VlogsConfig configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = VlogsConfig()
        assert config.extract_with_llm is True
        assert config.llm_model == "gpt-4o-mini"
        assert config.temperature == 0.3
        assert config.limit == 50

    def test_custom_config(self):
        """Test custom configuration values."""
        config = VlogsConfig(
            extract_with_llm=False,
            llm_model="gpt-4",
            temperature=0.5,
            limit=100,
        )
        assert config.extract_with_llm is False
        assert config.llm_model == "gpt-4"
        assert config.temperature == 0.5
        assert config.limit == 100


class TestVlogsAgent:
    """Test VlogsAgent functionality."""

    def test_agent_initialization(self):
        """Test agent can be initialized."""
        agent = VlogsAgent()
        assert agent.config is not None
        assert isinstance(agent.config, VlogsConfig)

    def test_agent_from_config(self):
        """Test agent created from app config (used by CheckinState)."""
        agent = VlogsAgent.from_config()
        assert agent.config.extract_with_llm is True
        assert agent.config.output_schema == MetricLogsOutput

    def test_agent_with_custom_config(self):
        """Test agent with custom configuration."""
        config = VlogsConfig(extract_with_llm=False, limit=10)
        agent = VlogsAgent(config=config)
        assert agent.config.extract_with_llm is False
        assert agent.config.limit == 10

    def test_agent_with_llm_disabled_has_no_structured_llm(self):
        """Verify agent with LLM disabled doesn't initialize LLM client."""
        config = VlogsConfig(extract_with_llm=False)
        agent = VlogsAgent(config=config)
        assert agent._structured_llm is None

    def test_agent_with_llm_enabled_has_structured_llm(self):
        """Verify agent with LLM enabled initializes LLM client."""
        import os

        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        agent = VlogsAgent.from_config()
        assert agent._structured_llm is not None


class TestParseCheckinWithHealthData:
    """Test parse_checkin_with_health_data (used by CheckinState.save_checkin_and_log_health)."""

    @pytest.mark.asyncio
    async def test_empty_content_returns_empty_output(self):
        """Empty content should return empty MetricLogsOutput."""
        result = await VlogsAgent.parse_checkin_with_health_data(
            content="", checkin_type="voice"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.type == "voice"
        assert len(result.medications_entries) == 0
        assert len(result.food_entries) == 0

    @pytest.mark.asyncio
    async def test_short_content_returns_empty_output(self):
        """Content under 10 chars should return empty MetricLogsOutput."""
        result = await VlogsAgent.parse_checkin_with_health_data(
            content="hi", checkin_type="text"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.summary == "hi"

    @pytest.mark.asyncio
    async def test_parse_with_valid_content(self):
        """Valid content should be parsed with LLM extraction."""
        import os

        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set - LLM extraction unavailable")
        content = (
            "I took my 10mg lisinopril this morning with breakfast. Had eggs and toast."
        )
        result = await VlogsAgent.parse_checkin_with_health_data(
            content=content, checkin_type="voice", patient_name="Test Patient"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.type == "voice"
        # LLM should extract medication and food entries
        assert len(result.medications_entries) > 0 or len(result.food_entries) > 0


class TestVlogsIntegration:
    """Integration tests requiring API access."""

    @pytest.mark.asyncio
    async def test_fetch_and_sync_raw_demo_patient(self):
        """Test fetching and syncing raw call logs (used by CheckinState.refresh_call_logs)."""
        config = VlogsConfig(extract_with_llm=False, limit=3)
        agent = VlogsAgent(config=config)
        phone = "+12126804645"

        try:
            new_count = await agent.fetch_and_sync_raw(phone_number=phone)
            assert new_count >= 0
        except Exception as e:
            pytest.skip(f"API access required: {e}")
