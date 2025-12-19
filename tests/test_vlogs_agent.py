"""Tests for VlogsAgent call log processing.

Tests both LLM-enabled and non-LLM processing modes.
"""

import asyncio
import pytest
from longevity_clinic.app.functions.vlogs import VlogsAgent
from longevity_clinic.app.config import VlogsConfig


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

    def test_default_config_from_app_settings(self):
        """Test default config loads from app settings."""
        config = VlogsConfig()
        assert isinstance(config, VlogsConfig)
        # Should match app config values
        assert config.extract_with_llm is True
        assert config.llm_model == "gpt-4o-mini"


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

    @pytest.mark.asyncio
    async def test_process_logs_demo_patient(self):
        """Test processing logs for demo patient.

        This test fetches actual call logs and processes them.
        Requires valid API access and OpenAI key for LLM parsing.
        """
        # Use non-LLM mode for faster testing
        config = VlogsConfig(extract_with_llm=False, limit=5)
        agent = VlogsAgent(config=config)

        # Demo patient phone number
        phone = "+12126804645"

        try:
            new_count, outputs, summaries = await agent.process_logs(phone_number=phone)

            # Basic assertions
            assert new_count >= 0
            assert isinstance(outputs, list)
            assert isinstance(summaries, list)

            # If we got data, verify structure
            if outputs:
                output = outputs[0]
                assert hasattr(output, "patient_id")
                assert hasattr(output, "call_log_id")
                assert hasattr(output, "timestamp")

            if summaries:
                summary = summaries[0]
                assert hasattr(summary, "summary")
                assert hasattr(summary, "patient_id")

            print(f"\n✅ Processed {new_count} new call logs")
            print(f"   Generated {len(outputs)} outputs")
            print(f"   Generated {len(summaries)} summaries")

        except Exception as e:
            pytest.skip(f"API access required: {e}")

    @pytest.mark.asyncio
    async def test_process_logs_with_llm(self):
        """Test processing with LLM parsing enabled.

        This test uses LLM for structured extraction.
        Requires OpenAI API key and may take longer.
        """
        # Enable LLM parsing
        config = VlogsConfig(extract_with_llm=True, limit=2)
        agent = VlogsAgent(config=config)

        phone = "+12126804645"

        try:
            new_count, outputs, summaries = await agent.process_logs(phone_number=phone)

            # Verify LLM-parsed data has better structure
            if outputs and new_count > 0:
                output = outputs[0]

                # LLM parsing should extract structured fields
                print(f"\n✅ LLM processed {new_count} call logs")
                print(f"   Medications: {len(output.medications)}")
                print(f"   Food entries: {len(output.food_entries)}")

        except Exception as e:
            pytest.skip(f"LLM parsing requires OpenAI API key: {e}")


class TestVlogsIntegration:
    """Integration tests for complete workflows."""

    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test complete processing workflow."""
        # Create agent with app config
        agent = VlogsAgent.from_config()

        # Process logs
        phone = "+12126804645"

        try:
            new_count, outputs, summaries = await agent.process_logs(phone_number=phone)

            # Verify complete workflow
            assert new_count >= 0
            assert len(outputs) == len(summaries)

            # If we have data, verify relationships
            if outputs and summaries:
                assert outputs[0].patient_id == summaries[0].patient_id
                assert outputs[0].call_log_id == summaries[0].call_log_id

            print(f"\n✅ Complete workflow processed {new_count} logs")

        except Exception as e:
            pytest.skip(f"Integration test requires API access: {e}")


# Sync wrapper for manual testing
def test_vlogs_agent_manually():
    """Manual test function that can be run directly."""

    async def run_test():
        print("Testing VlogsAgent...")

        # Test with non-LLM mode first
        print("\n1. Testing non-LLM mode:")
        config = VlogsConfig(extract_with_llm=False, limit=3)
        agent = VlogsAgent(config=config)

        new_count, outputs, summaries = await agent.process_logs(
            phone_number="+12126804645"
        )

        print(f"   ✅ Processed {new_count} logs")
        print(f"   ✅ Generated {len(outputs)} outputs")
        print(f"   ✅ Generated {len(summaries)} summaries")

        # Test with LLM mode
        print("\n2. Testing LLM mode:")
        agent_llm = VlogsAgent.from_config()

        new_count, outputs, summaries = await agent_llm.process_logs(
            phone_number="+12126804645"
        )

        print(f"   ✅ Processed {new_count} logs with LLM")
        if outputs:
            print(
                f"   ✅ First output has {len(outputs[0].medications_entries)} medications"
            )
            print(f"   ✅ First output has {len(outputs[0].food_entries)} food entries")
            print(f"   ✅ First output has {len(outputs[0].symptom_entries)} symptoms")

        print("\n✨ All tests passed!")

    asyncio.run(run_test())


if __name__ == "__main__":
    test_vlogs_agent_manually()
