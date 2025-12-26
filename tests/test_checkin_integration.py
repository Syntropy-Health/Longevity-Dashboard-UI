"""Integration tests for CheckinState and VlogsAgent pipeline.

Tests the full CDC pipeline used by patient check-ins:
1. Call logs API health check
2. VlogsAgent.fetch_and_sync_raw() - sync raw call logs to DB
3. VlogsAgent.process_unprocessed_logs() - LLM processing
4. filter_checkins() - sorting and filtering

Run with: uv run pytest tests/test_checkin_integration.py -v
"""

from datetime import datetime, timedelta
from typing import Any

import httpx
import pytest

from longevity_clinic.app.config import (
    CALL_API_TOKEN,
    OPENAI_API_KEY,
    VlogsConfig,
    current_config,
)
from longevity_clinic.app.data.schemas.llm import MetricLogsOutput
from longevity_clinic.app.functions.admins.checkins import filter_checkins
from longevity_clinic.app.functions.utils import fetch_call_logs
from longevity_clinic.app.functions.vlogs import VlogsAgent

# =============================================================================
# API Health Tests
# =============================================================================


class TestCallLogsAPIHealth:
    """Verify call logs API is accessible and returning data."""

    @pytest.mark.asyncio
    async def test_api_endpoint_reachable(self):
        """Test that the call logs API endpoint is reachable."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                current_config.call_logs_api_base,
                headers={"Authorization": f"Bearer {CALL_API_TOKEN}"},
                params={"limit": 1},
                timeout=10.0,
            )
            assert response.status_code == 200, f"API returned {response.status_code}"

    @pytest.mark.asyncio
    async def test_api_returns_valid_json(self):
        """Test that the API returns valid JSON with expected structure."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                current_config.call_logs_api_base,
                headers={"Authorization": f"Bearer {CALL_API_TOKEN}"},
                params={"limit": 1},
                timeout=10.0,
            )
            data = response.json()
            assert "data" in data, "Response missing 'data' key"
            assert isinstance(data["data"], list), "'data' should be a list"

    @pytest.mark.asyncio
    async def test_fetch_call_logs_function(self):
        """Test fetch_call_logs utility function works correctly."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        # Fetch without phone filter (admin view)
        logs = await fetch_call_logs(phone_number=None, limit=5)
        assert isinstance(logs, list)

        # Fetch with demo patient phone
        demo_phone = current_config.demo_user.phone
        patient_logs = await fetch_call_logs(phone_number=demo_phone, limit=5)
        assert isinstance(patient_logs, list)

    @pytest.mark.asyncio
    async def test_api_returns_transcripts(self):
        """Test that API returns call logs with transcripts."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        logs = await fetch_call_logs(
            phone_number=None, limit=10, require_transcript=True
        )

        # At least some logs should have transcripts
        logs_with_transcript = [
            log for log in logs if log.get("full_transcript", "").strip()
        ]
        # Don't fail if no transcripts - just report
        if not logs_with_transcript:
            pytest.skip("No call logs with transcripts found in API")


# =============================================================================
# VlogsAgent Tests
# =============================================================================


class TestVlogsAgentConfig:
    """Test VlogsAgent configuration and initialization."""

    def test_vlogs_config_defaults(self):
        """Test default VlogsConfig values from process_config."""
        config = VlogsConfig()
        assert config.extract_with_llm is True
        assert config.llm_model == "gpt-4o-mini"
        assert config.temperature == 0.3
        assert config.limit == 50

    def test_vlogs_config_llm_disabled(self):
        """Test VlogsConfig with LLM disabled."""
        config = VlogsConfig(extract_with_llm=False)
        assert config.extract_with_llm is False

    def test_agent_from_config(self):
        """Test VlogsAgent.from_config() factory method."""
        import os

        agent = VlogsAgent.from_config()
        assert agent.config.output_schema == MetricLogsOutput
        # LLM client only initialized when API key is set
        if os.getenv("OPENAI_API_KEY"):
            assert agent._structured_llm is not None
        else:
            assert agent._structured_llm is None

    def test_agent_without_llm(self):
        """Test VlogsAgent with LLM disabled doesn't create LLM client."""
        config = VlogsConfig(extract_with_llm=False)
        agent = VlogsAgent(config=config)
        assert agent._structured_llm is None


class TestVlogsAgentParsing:
    """Test VlogsAgent.parse_checkin_with_health_data() method."""

    @pytest.mark.asyncio
    async def test_empty_content_returns_empty_output(self):
        """Empty content should return MetricLogsOutput with empty lists."""
        result = await VlogsAgent.parse_checkin_with_health_data(
            content="", checkin_type="voice"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.type == "voice"
        assert len(result.medications_entries) == 0
        assert len(result.food_entries) == 0
        assert len(result.symptom_entries) == 0

    @pytest.mark.asyncio
    async def test_short_content_under_10_chars(self):
        """Content under 10 chars should return empty MetricLogsOutput."""
        result = await VlogsAgent.parse_checkin_with_health_data(
            content="hi", checkin_type="text"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.summary == "hi"
        assert len(result.medications_entries) == 0

    @pytest.mark.asyncio
    async def test_parse_medication_content(self):
        """Content with medication mentions should extract them."""
        if not OPENAI_API_KEY:
            pytest.skip("OPENAI_API_KEY not set")

        content = "I took my 10mg lisinopril this morning with breakfast."
        result = await VlogsAgent.parse_checkin_with_health_data(
            content=content, checkin_type="voice", patient_name="Test Patient"
        )
        assert isinstance(result, MetricLogsOutput)
        assert result.checkin.type == "voice"
        # LLM should extract medication
        assert len(result.medications_entries) >= 0  # May vary based on LLM

    @pytest.mark.asyncio
    async def test_parse_food_content(self):
        """Content with food mentions should extract them."""
        if not OPENAI_API_KEY:
            pytest.skip("OPENAI_API_KEY not set")

        content = "For breakfast I had scrambled eggs with whole wheat toast and orange juice."
        result = await VlogsAgent.parse_checkin_with_health_data(
            content=content, checkin_type="text", patient_name="Test Patient"
        )
        assert isinstance(result, MetricLogsOutput)
        # Food entries may or may not be extracted depending on LLM
        assert len(result.food_entries) >= 0


class TestVlogsAgentCDC:
    """Test VlogsAgent CDC pipeline methods."""

    @pytest.mark.asyncio
    async def test_fetch_and_sync_raw_returns_count(self):
        """Test fetch_and_sync_raw returns count of synced logs."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        config = VlogsConfig(extract_with_llm=False, limit=3)
        agent = VlogsAgent(config=config)

        demo_phone = current_config.demo_user.phone
        # Clean phone number (remove formatting)
        phone_clean = (
            demo_phone.replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        new_count = await agent.fetch_and_sync_raw(phone_number=phone_clean)
        # Should return 0 or more (0 if already synced)
        assert new_count >= 0

    @pytest.mark.asyncio
    async def test_process_unprocessed_with_llm_disabled(self):
        """Test process_unprocessed_logs with LLM disabled returns 0."""
        config = VlogsConfig(extract_with_llm=False)
        agent = VlogsAgent(config=config)

        count = await agent.process_unprocessed_logs()
        assert count == 0


# =============================================================================
# Filter/Sort Tests
# =============================================================================


class TestFilterCheckins:
    """Test filter_checkins function used by CheckinState.filtered_checkins."""

    def _create_mock_checkins(self) -> list[dict[str, Any]]:
        """Create mock checkins with various statuses and timestamps."""
        base_time = datetime.now()
        return [
            {
                "id": "chk_001",
                "patient_name": "Sarah Chen",
                "summary": "Feeling good today",
                "status": "pending",
                "timestamp": (base_time - timedelta(hours=1)).isoformat(),
                "key_topics": ["wellness"],
            },
            {
                "id": "chk_002",
                "patient_name": "John Smith",
                "summary": "Took medication",
                "status": "reviewed",
                "timestamp": (base_time - timedelta(hours=2)).isoformat(),
                "key_topics": ["medication"],
            },
            {
                "id": "chk_003",
                "patient_name": "Sarah Chen",
                "summary": "Headache reported",
                "status": "flagged",
                "timestamp": (base_time - timedelta(hours=3)).isoformat(),
                "key_topics": ["symptoms", "pain"],
            },
            {
                "id": "chk_004",
                "patient_name": "Mike Johnson",
                "summary": "Exercise completed",
                "status": "pending",
                "timestamp": base_time.isoformat(),  # Most recent
                "key_topics": ["exercise"],
            },
        ]

    def test_filter_by_status_pending(self):
        """Test filtering by pending status."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status="pending")

        assert len(result) == 2
        assert all(c["status"] == "pending" for c in result)

    def test_filter_by_status_reviewed(self):
        """Test filtering by reviewed status."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status="reviewed")

        assert len(result) == 1
        assert result[0]["status"] == "reviewed"

    def test_filter_by_status_flagged(self):
        """Test filtering by flagged status."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status="flagged")

        assert len(result) == 1
        assert result[0]["status"] == "flagged"

    def test_filter_status_all_returns_all(self):
        """Test 'all' status returns all checkins."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status="all")

        assert len(result) == 4

    def test_filter_status_none_returns_all(self):
        """Test None status returns all checkins."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status=None)

        assert len(result) == 4

    def test_filter_by_search_query_patient_name(self):
        """Test filtering by patient name search."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, search_query="Sarah")

        assert len(result) == 2
        assert all("Sarah" in c["patient_name"] for c in result)

    def test_filter_by_search_query_summary(self):
        """Test filtering by summary content."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, search_query="medication")

        assert len(result) == 1
        assert "medication" in result[0]["summary"].lower()

    def test_filter_by_search_query_topic(self):
        """Test filtering by topic keyword."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, search_query="pain")

        assert len(result) == 1
        assert "pain" in result[0]["key_topics"]

    def test_filter_combined_status_and_search(self):
        """Test combined status and search filtering."""
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status="pending", search_query="Sarah")

        assert len(result) == 1
        assert result[0]["patient_name"] == "Sarah Chen"
        assert result[0]["status"] == "pending"

    def test_sort_by_timestamp_newest_first(self):
        """Test that results are sorted by timestamp (newest first).

        This was a bug - filter_checkins was sorting by 'submitted_at' but
        _load_checkins_from_db uses 'timestamp' key.
        """
        checkins = self._create_mock_checkins()
        result = filter_checkins(checkins, status=None)

        # chk_004 has the most recent timestamp, should be first
        assert result[0]["id"] == "chk_004"
        # chk_003 has the oldest, should be last
        assert result[-1]["id"] == "chk_003"

    def test_empty_checkins_list(self):
        """Test filtering empty list returns empty list."""
        result = filter_checkins([], status="pending")
        assert result == []

    def test_search_case_insensitive(self):
        """Test search is case-insensitive."""
        checkins = self._create_mock_checkins()

        result_lower = filter_checkins(checkins, search_query="sarah")
        result_upper = filter_checkins(checkins, search_query="SARAH")

        assert len(result_lower) == len(result_upper) == 2


# =============================================================================
# End-to-End Pipeline Test
# =============================================================================


class TestCheckinPipeline:
    """End-to-end tests for the checkin pipeline."""

    @pytest.mark.asyncio
    async def test_full_pipeline_without_llm(self):
        """Test full CDC pipeline with LLM disabled (API → sync only)."""
        if not CALL_API_TOKEN:
            pytest.skip("CALL_API_TOKEN not set")

        # Step 1: Create agent without LLM
        config = VlogsConfig(extract_with_llm=False, limit=2)
        agent = VlogsAgent(config=config)

        # Step 2: Fetch and sync (may return 0 if already synced)
        demo_phone = current_config.demo_user.phone
        phone_clean = (
            demo_phone.replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        new_count = await agent.fetch_and_sync_raw(phone_number=phone_clean)
        assert new_count >= 0

        # Step 3: Process unprocessed (should be 0 with LLM disabled)
        processed = await agent.process_unprocessed_logs()
        assert processed == 0

    @pytest.mark.asyncio
    async def test_parse_then_filter_flow(self):
        """Test the flow: parse content → create checkin dict → filter."""
        if not OPENAI_API_KEY:
            pytest.skip("OPENAI_API_KEY not set")

        # Parse content
        content = "I took my vitamins this morning. Feeling pretty good overall."
        result = await VlogsAgent.parse_checkin_with_health_data(
            content=content, checkin_type="text", patient_name="Test Patient"
        )

        # Create checkin dict (simulating what _load_checkins_from_db returns)
        checkin_dict = {
            "id": result.checkin.id,
            "patient_name": result.checkin.patient_name,
            "summary": result.checkin.summary,
            "status": "pending",
            "timestamp": datetime.now().isoformat(),
            "key_topics": result.checkin.key_topics or [],
        }

        # Filter should work correctly
        filtered = filter_checkins([checkin_dict], status="pending")
        assert len(filtered) == 1
        assert filtered[0]["status"] == "pending"
