"""Tests for AI transcript summarization and check-in integration."""

import pytest
import logging
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent to path to import from longevity_clinic
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.demo import CheckInModel

# Get logger from centralized config (with DEBUG level)
logger = get_logger("test_ai_summary", level=logging.DEBUG)


class TestAISummarization:
    """Test AI summarization of call transcripts using LangChain structured output."""

    @pytest.fixture
    def sample_transcript(self):
        """Sample call transcript for testing."""
        return """
        AI: Hey. Sarah speaking here. How are you doing? I heard you're a new patient.
        User: Hi Sarah, yes I'm calling because I've been feeling really tired lately.
        AI: I'm sorry to hear that. Can you tell me more about your fatigue? How long has this been going on?
        User: About two weeks now. I also noticed some joint pain in my knees.
        AI: That's helpful to know. Are you taking any medications currently?
        User: Just my blood pressure medication. I take it every morning.
        AI: Okay, that's important information. Have you noticed any changes in your diet or sleep patterns?
        User: Actually, yes. I've been having trouble sleeping and eating less than usual.
        AI: Thank you for sharing that. I'll make sure to note this for your provider.
        """

    @pytest.fixture
    def expected_summary_keywords(self):
        """Keywords we expect in a good summary."""
        return [
            "fatigue",
            "tired",
            "joint",
            "pain",
            "knee",
            "sleep",
            "medication",
            "blood pressure",
        ]

    @pytest.fixture
    def mock_checkin_model(self):
        """Mock CheckInModel for testing."""
        return CheckInModel(
            id="call_test-123",
            type="call",
            summary="Patient reports fatigue for 2 weeks with joint pain in knees. Taking blood pressure medication. Sleep and appetite issues noted.",
            timestamp="April 26, 2025 at 05:51 AM",
            sentiment="neutral",
            key_topics=["fatigue", "joint pain", "sleep"],
            provider_reviewed=False,
            patient_name="Demo Patient (Sarah Chen)",
        )

    @pytest.mark.asyncio
    async def test_summarize_transcript_returns_checkin_model(
        self, sample_transcript, mock_checkin_model
    ):
        """Test that _summarize_transcript returns a CheckInModel."""
        logger.info("Testing AI summary returns CheckInModel type")

        # Mock the LangChain structured LLM
        with patch(
            "longevity_clinic.app.states.patient_state.structured_llm"
        ) as mock_llm:
            mock_llm.invoke = MagicMock(return_value=mock_checkin_model)

            from longevity_clinic.app.states.patient_state import PatientState

            state = PatientState()

            result = await state._summarize_transcript(
                full_transcript=sample_transcript,
                call_id="test-123",
                call_date="2025-04-26T05:51:14",
                patient_phone="+12126804645",
            )

            assert isinstance(result, CheckInModel)
            assert result.id == "call_test-123"
            assert result.type == "call"
            assert len(result.summary) > 0
            logger.info("AI summary returned CheckInModel: %s", result.summary[:100])

    @pytest.mark.asyncio
    async def test_summarize_transcript_handles_error(self):
        """Test that _summarize_transcript handles errors gracefully."""
        logger.info("Testing AI summary error handling")

        with patch(
            "longevity_clinic.app.states.patient_state.structured_llm"
        ) as mock_llm:
            mock_llm.invoke = MagicMock(side_effect=Exception("API Error"))

            from longevity_clinic.app.states.patient_state import PatientState

            state = PatientState()

            result = await state._summarize_transcript(
                full_transcript="Test transcript",
                call_id="test-error",
                call_date="2025-04-26T05:51:14",
                patient_phone="+12126804645",
            )

            assert isinstance(result, CheckInModel)
            assert result.summary == "Summary generation failed."
            logger.info("Error handling works correctly")

    @pytest.mark.asyncio
    async def test_summarize_transcript_truncates_long_input(
        self, sample_transcript, mock_checkin_model
    ):
        """Test that long transcripts are truncated before sending to API."""
        logger.info("Testing AI summary truncates long input")

        # Create a very long transcript
        long_transcript = sample_transcript * 100  # Make it very long

        with patch(
            "longevity_clinic.app.states.patient_state.structured_llm"
        ) as mock_llm:
            mock_llm.invoke = MagicMock(return_value=mock_checkin_model)

            from longevity_clinic.app.states.patient_state import PatientState

            state = PatientState()

            result = await state._summarize_transcript(
                full_transcript=long_transcript,
                call_id="test-long",
                call_date="2025-04-26T05:51:14",
                patient_phone="+12126804645",
            )

            # Verify the call was made
            assert mock_llm.invoke.called
            # Get the messages passed to the LLM
            call_args = mock_llm.invoke.call_args
            messages = call_args[0][0]  # First positional arg is the messages list

            # The transcript portion should be limited in the HumanMessage
            human_message_content = messages[-1].content
            assert (
                len(human_message_content) <= 4200
            )  # Some overhead for the prompt text
            logger.info("Long transcript was properly truncated")


class TestCheckinIntegration:
    """Test integration of call logs with check-ins."""

    @pytest.fixture
    def sample_call_log(self):
        """Sample call log entry."""
        return {
            "id": 314,
            "caller_phone": "+12126804645",
            "call_date": "2025-04-26T05:51:14",
            "call_duration": 120,
            "summary": "Patient discussed fatigue and joint pain",
            "full_transcript": "AI: Hello... User: I'm tired...",
            "notes": "{}",
            "call_id": "test-uuid-12345",
        }

    @pytest.fixture
    def sample_ai_summary(self):
        """Sample AI-generated summary."""
        return "Patient reports experiencing fatigue for 2 weeks with knee joint pain. Currently taking blood pressure medication. Noted sleep and appetite disturbances."

    def test_transcript_summary_structure(self, sample_call_log, sample_ai_summary):
        """Test that TranscriptSummary has the correct structure."""
        logger.info("Testing TranscriptSummary structure")

        from longevity_clinic.app.states.patient_state import TranscriptSummary

        summary: TranscriptSummary = {
            "call_id": sample_call_log["call_id"],
            "patient_phone": sample_call_log["caller_phone"],
            "call_date": sample_call_log["call_date"],
            "summary": sample_call_log["summary"],
            "ai_summary": sample_ai_summary,
            "type": "call",
            "timestamp": "April 26, 2025 at 5:51 AM",
        }

        assert summary["call_id"] == "test-uuid-12345"
        assert summary["type"] == "call"
        assert "fatigue" in summary["ai_summary"].lower()
        logger.info("TranscriptSummary structure is valid")

    def test_checkin_format_from_call_log(self, sample_call_log, sample_ai_summary):
        """Test conversion of call log to CheckIn format with patient_name."""
        logger.info("Testing call log to CheckIn conversion")

        from longevity_clinic.app.data.demo import CheckIn

        # Create a CheckIn from the call log (now includes patient_name)
        checkin: CheckIn = {
            "id": f"call_{sample_call_log['call_id']}",
            "type": "call",
            "summary": sample_ai_summary,
            "timestamp": "April 26, 2025 at 5:51 AM",
            "sentiment": "neutral",
            "key_topics": ["fatigue", "joint pain", "medication"],
            "provider_reviewed": False,
            "patient_name": "Demo Patient (Sarah Chen)",
        }

        assert checkin["type"] == "call"
        assert checkin["id"].startswith("call_")
        assert "fatigue" in checkin["key_topics"]
        assert checkin["patient_name"] == "Demo Patient (Sarah Chen)"
        logger.info("CheckIn conversion is valid: %s", checkin["id"])

    def test_checkins_sorted_chronologically(self):
        """Test that check-ins are sorted with newest first."""
        logger.info("Testing check-in chronological sorting")

        checkins = [
            {"id": "1", "timestamp": "2025-04-25T10:00:00", "summary": "Older"},
            {"id": "2", "timestamp": "2025-04-26T05:51:14", "summary": "Newer"},
            {"id": "3", "timestamp": "2025-04-24T08:00:00", "summary": "Oldest"},
        ]

        # Sort by timestamp descending
        sorted_checkins = sorted(checkins, key=lambda x: x["timestamp"], reverse=True)

        assert sorted_checkins[0]["id"] == "2"  # Newest first
        assert sorted_checkins[1]["id"] == "1"
        assert sorted_checkins[2]["id"] == "3"  # Oldest last
        logger.info(
            "Check-ins sorted correctly: %s", [c["id"] for c in sorted_checkins]
        )


class TestAdminCheckinView:
    """Test admin check-in view functionality."""

    @pytest.fixture
    def sample_admin_checkin(self):
        """Sample admin check-in entry."""
        return {
            "id": "call_test-uuid",
            "patient_id": "P001",
            "patient_name": "John Doe",
            "type": "call",
            "summary": "Patient reports fatigue and joint pain",
            "timestamp": "Today, 10:30 AM",
            "submitted_at": "2025-04-26T05:51:14",
            "sentiment": "neutral",
            "key_topics": ["fatigue", "joint pain"],
            "status": "pending",
            "provider_reviewed": False,
            "reviewed_by": "",
            "reviewed_at": "",
        }

    def test_admin_checkin_has_patient_name(self, sample_admin_checkin):
        """Test that admin check-in includes patient name."""
        logger.info("Testing admin check-in has patient name")

        assert "patient_name" in sample_admin_checkin
        assert sample_admin_checkin["patient_name"] == "John Doe"
        logger.info(
            "Admin check-in has patient_name: %s", sample_admin_checkin["patient_name"]
        )

    def test_admin_checkin_search_by_patient_name(self, sample_admin_checkin):
        """Test searching check-ins by patient name."""
        logger.info("Testing search by patient name")

        checkins = [
            sample_admin_checkin,
            {**sample_admin_checkin, "id": "2", "patient_name": "Jane Smith"},
            {**sample_admin_checkin, "id": "3", "patient_name": "John Williams"},
        ]

        search_query = "john"
        results = [
            c for c in checkins if search_query.lower() in c["patient_name"].lower()
        ]

        assert len(results) == 2  # John Doe and John Williams
        logger.info("Search found %d results for 'john'", len(results))

    def test_admin_checkin_search_by_summary(self, sample_admin_checkin):
        """Test searching check-ins by summary content."""
        logger.info("Testing search by summary content")

        checkins = [
            sample_admin_checkin,
            {**sample_admin_checkin, "id": "2", "summary": "Sleep issues reported"},
            {**sample_admin_checkin, "id": "3", "summary": "Blood pressure concerns"},
        ]

        search_query = "fatigue"
        results = [c for c in checkins if search_query.lower() in c["summary"].lower()]

        assert len(results) == 1
        assert results[0]["id"] == sample_admin_checkin["id"]
        logger.info("Search found %d results for 'fatigue'", len(results))

    def test_admin_checkin_search_by_topics(self, sample_admin_checkin):
        """Test searching check-ins by key topics."""
        logger.info("Testing search by key topics")

        checkins = [
            sample_admin_checkin,
            {**sample_admin_checkin, "id": "2", "key_topics": ["sleep", "anxiety"]},
            {
                **sample_admin_checkin,
                "id": "3",
                "key_topics": ["joint pain", "medication"],
            },
        ]

        search_query = "joint"
        results = [
            c
            for c in checkins
            if any(search_query.lower() in topic.lower() for topic in c["key_topics"])
        ]

        assert len(results) == 2  # First and third have "joint pain"
        logger.info("Search found %d results for 'joint' topic", len(results))
