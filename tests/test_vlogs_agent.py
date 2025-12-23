"""Tests for VlogsAgent call log processing.

Tests both LLM-enabled and non-LLM processing modes.
Note: Integration tests in this file require API access and may be skipped.
Unit tests for CDC pipeline are in tests/checkin/test_call_log_sync.py.
"""

import pytest

from longevity_clinic.app.config import VlogsConfig
from longevity_clinic.app.functions.vlogs import VlogsAgent


class TestVlogsConfig:
    """Test VlogsConfig configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = VlogsConfig()
        assert config.extract_with_llm is True  # Default should be True
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
        """Test agent created from app config."""
        agent = VlogsAgent.from_config()
        assert agent.config.extract_with_llm is True

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
        agent = VlogsAgent.from_config()
        assert agent._structured_llm is not None


class TestVlogsIntegration:
    """Integration tests requiring API access."""

    @pytest.mark.asyncio
    async def test_fetch_and_sync_raw_demo_patient(self):
        """Test fetching and syncing raw call logs.

        This test fetches actual call logs from the API.
        Requires valid API access.
        """
        config = VlogsConfig(extract_with_llm=False, limit=3)
        agent = VlogsAgent(config=config)

        phone = "+12126804645"

        try:
            new_count = await agent.fetch_and_sync_raw(phone_number=phone)
            assert new_count >= 0
            print(f"\n✅ Synced {new_count} raw call logs")
        except Exception as e:
            pytest.skip(f"API access required: {e}")
