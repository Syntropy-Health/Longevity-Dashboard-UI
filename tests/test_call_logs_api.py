"""Tests for call logs API connection and data verification."""

import pytest
import httpx
import logging
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from longevity_clinic.app.config import get_logger

log_file = Path(__file__).parent.parent / "test.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="w"),
        logging.StreamHandler(),
    ],
)

logger = get_logger("test_call_logs_api", level=logging.DEBUG)


# =============================================================================
# Test fetch_call_logs function from utils
# =============================================================================


class TestFetchCallLogsFunction:
    """Test the fetch_call_logs utility function."""

    @pytest.mark.asyncio
    async def test_fetch_call_logs_with_phone(self, call_api_token, demo_phone_number):
        """Test fetch_call_logs with a phone number filter."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import fetch_call_logs

        logger.info("Testing fetch_call_logs(phone=%s)", demo_phone_number)
        call_logs = await fetch_call_logs(phone_number=demo_phone_number, limit=10)

        assert isinstance(call_logs, list)
        logger.info("Fetched %d call logs", len(call_logs))

        if call_logs:
            log = call_logs[0]
            assert "call_id" in log
            assert "call_date" in log
            logger.info("First log call_id: %s", log.get("call_id"))

    @pytest.mark.asyncio
    async def test_fetch_call_logs_all(self, call_api_token):
        """Test fetch_call_logs without phone filter (admin use case)."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import fetch_call_logs

        logger.info("Testing fetch_call_logs() without phone filter")
        call_logs = await fetch_call_logs(limit=5)

        assert isinstance(call_logs, list)
        logger.info("Fetched %d call logs (no filter)", len(call_logs))

    @pytest.mark.asyncio
    async def test_fetch_call_logs_pagination(self, call_api_token, demo_phone_number):
        """Test fetch_call_logs with pagination."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import fetch_call_logs

        page1 = await fetch_call_logs(phone_number=demo_phone_number, limit=2, page=1)
        page2 = await fetch_call_logs(phone_number=demo_phone_number, limit=2, page=2)

        logger.info("Page 1: %d logs, Page 2: %d logs", len(page1), len(page2))

        # If there are enough records, pages should be different
        if len(page1) == 2 and len(page2) > 0:
            assert page1[0].get("call_id") != page2[0].get("call_id")


# =============================================================================
# Test process_call_logs function
# =============================================================================


class TestProcessCallLogsFunction:
    """Test the process_call_logs function."""

    @pytest.mark.asyncio
    async def test_process_call_logs_without_llm(
        self, call_api_token, demo_phone_number
    ):
        """Test process_call_logs with use_llm_summary=False."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import (
            fetch_call_logs,
            process_call_logs,
        )

        # Fetch raw logs first
        call_logs = await fetch_call_logs(phone_number=demo_phone_number, limit=3)
        if not call_logs:
            pytest.skip("No call logs available")

        logger.info("Processing %d call logs without LLM", len(call_logs))

        # Process without LLM
        new_count, checkins, summaries = await process_call_logs(
            call_logs, processed_ids=set(), use_llm_summary=False
        )

        assert new_count == len(call_logs)
        assert len(checkins) == new_count
        assert len(summaries) == new_count

        logger.info(
            "Processed %d logs -> %d checkins, %d summaries",
            new_count,
            len(checkins),
            len(summaries),
        )

        # Validate checkin structure
        if checkins:
            checkin = checkins[0]
            assert "id" in checkin
            assert "type" in checkin
            assert "summary" in checkin
            assert checkin["type"] == "call"
            logger.info(
                "Sample checkin: id=%s, summary=%s...",
                checkin["id"],
                checkin["summary"][:50],
            )

    @pytest.mark.asyncio
    async def test_process_call_logs_skips_processed(
        self, call_api_token, demo_phone_number
    ):
        """Test that process_call_logs skips already processed IDs."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import (
            fetch_call_logs,
            process_call_logs,
        )

        call_logs = await fetch_call_logs(phone_number=demo_phone_number, limit=3)
        if not call_logs:
            pytest.skip("No call logs available")

        # First pass - process all
        count1, _, summaries1 = await process_call_logs(call_logs, set(), False)

        # Second pass - all should be skipped
        count2, _, summaries2 = await process_call_logs(
            call_logs, set(summaries1.keys()), False
        )

        assert count1 > 0
        assert count2 == 0
        logger.info("First pass: %d, Second pass: %d (all skipped)", count1, count2)


# =============================================================================
# Test fetch_and_process_call_logs combined function
# =============================================================================


class TestFetchAndProcessCallLogs:
    """Test the combined fetch_and_process_call_logs function."""

    @pytest.mark.asyncio
    async def test_fetch_and_process_combined(self, call_api_token, demo_phone_number):
        """Test the combined fetch_and_process_call_logs function."""
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        from longevity_clinic.app.states.functions import (
            fetch_call_logs,
            fetch_and_process_call_logs,
        )

        logger.info("=" * 60)
        logger.info("TEST: fetch_and_process_call_logs(phone=%s)", demo_phone_number)
        logger.info("=" * 60)

        # Step 1: Fetch raw call logs to log intermediate API response
        logger.info("\n--- STEP 1: Raw API Response ---")
        raw_call_logs = await fetch_call_logs(phone_number=demo_phone_number, limit=5)
        logger.info("Raw call logs count: %d", len(raw_call_logs))
        for i, log in enumerate(raw_call_logs):
            logger.info("\n[RAW CALL LOG %d]:", i + 1)
            logger.info("  call_id: %s", log.get("call_id"))
            logger.info("  caller_phone: %s", log.get("caller_phone"))
            logger.info("  call_date: %s", log.get("call_date"))
            logger.info("  call_duration: %s seconds", log.get("call_duration"))
            logger.info(
                "  summary: %s",
                log.get("summary", "")[:200] if log.get("summary") else "N/A",
            )
            transcript = log.get("full_transcript", "")
            logger.info(
                "  transcript_length: %d chars", len(transcript) if transcript else 0
            )
            if transcript:
                logger.info("  transcript_preview: %s...", transcript[:300])

        # Step 2: Process call logs using combined function
        logger.info("\n--- STEP 2: Processing Call Logs ---")
        new_count, checkins, summaries = await fetch_and_process_call_logs(
            phone_number=demo_phone_number,
            processed_ids=set(),
            use_llm_summary=False,
            limit=5,
        )

        assert isinstance(checkins, list)
        assert isinstance(summaries, dict)

        logger.info(
            "Processing result: %d new, %d checkins, %d summaries",
            new_count,
            len(checkins),
            len(summaries),
        )

        # Step 3: Log processed CheckIns (Pydantic dict format)
        logger.info("\n--- STEP 3: Processed CheckIns (Pydantic Dict) ---")
        for i, checkin in enumerate(checkins):
            logger.info("\n[CHECKIN %d]:", i + 1)
            logger.info("  id: %s", checkin.get("id"))
            logger.info("  type: %s", checkin.get("type"))
            logger.info("  timestamp: %s", checkin.get("timestamp"))
            logger.info("  summary: %s", checkin.get("summary"))
            logger.info("  topics: %s", checkin.get("topics"))
            logger.info(
                "  Full CheckIn dict: %s", json.dumps(checkin, indent=4, default=str)
            )

        # Step 4: Log transcript summaries dictionary
        logger.info("\n--- STEP 4: Transcript Summaries Dict ---")
        for call_id, summary in summaries.items():
            logger.info("\n[SUMMARY for %s]:", call_id)
            logger.info("  %s", summary[:500] if len(summary) > 500 else summary)

        logger.info("\n" + "=" * 60)
        logger.info("TEST COMPLETE: All assertions passed")
        logger.info("=" * 60)

        if checkins:
            assert checkins[0]["type"] == "call"


# =============================================================================
# Original API Tests
# =============================================================================


class TestCallLogsAPIConnection:
    """Test call logs API connectivity."""

    def test_api_token_is_set(self, call_api_token):
        """Verify that the API token is properly configured."""
        logger.info("Testing API token configuration")
        assert call_api_token is not None
        assert len(call_api_token) > 0, "CALL_API_TOKEN environment variable is not set"
        logger.info("API token is configured (length: %d)", len(call_api_token))

    @pytest.mark.asyncio
    async def test_api_connection(self, call_logs_api_base, call_api_token):
        """Test that we can connect to the call logs API."""
        logger.info("Testing API connection to: %s", call_logs_api_base)
        if not call_api_token:
            logger.warning("CALL_API_TOKEN not set, skipping test")
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                call_logs_api_base,
                params={"limit": 1},
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            logger.info("API Response Status: %d", response.status_code)
            assert response.status_code == 200, (
                f"API returned status {response.status_code}"
            )
            logger.info("API connection successful")

    @pytest.mark.asyncio
    async def test_api_returns_valid_json(self, call_logs_api_base, call_api_token):
        """Test that the API returns valid JSON."""
        logger.info("Testing API JSON response format")
        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                call_logs_api_base,
                params={"limit": 1},
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            data = response.json()
            logger.info("Response JSON keys: %s", list(data.keys()))
            assert "data" in data, "Response should contain 'data' key"
            assert isinstance(data["data"], list), "'data' should be a list"
            logger.info("API returns valid JSON with 'data' array")


class TestCallLogsDataFetching:
    """Test call logs data fetching for DEMO_PHONE_NUMBER."""

    @pytest.mark.asyncio
    async def test_fetch_demo_phone_logs(
        self, call_logs_api_base, call_api_token, demo_phone_number
    ):
        """Test fetching call logs for the demo phone number."""
        logger.info("=" * 60)
        logger.info("Fetching call logs for DEMO_PHONE_NUMBER: %s", demo_phone_number)

        if not call_api_token:
            logger.warning("CALL_API_TOKEN not set, skipping test")
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            params = {
                "limit": 50,
                "offset": 0,
                "page": 1,
                "sort": "-call_date",
                "fields": "*.*",
                "filter[caller_phone][_eq]": demo_phone_number,
            }
            logger.info("Request params: %s", json.dumps(params, indent=2))

            response = await client.get(
                call_logs_api_base,
                params=params,
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            logger.info("Response status: %d", response.status_code)
            assert response.status_code == 200
            data = response.json()

            # Log metadata if present
            if "meta" in data:
                logger.info("Response metadata: %s", json.dumps(data["meta"], indent=2))

            records = data.get("data", [])
            logger.info("Found %d call logs for %s", len(records), demo_phone_number)

            # Log first record structure
            if records:
                record = records[0]
                logger.info("First record keys: %s", list(record.keys()))
                logger.info(
                    "First record sample: id=%s, call_date=%s, call_duration=%s",
                    record.get("id"),
                    record.get("call_date"),
                    record.get("call_duration"),
                )
                assert "call_id" in record or "id" in record
                assert "caller_phone" in record or "phone" in record
            else:
                logger.warning("No records found for demo phone number")

    @pytest.mark.asyncio
    async def test_fetch_logs_with_transcript(
        self, call_logs_api_base, call_api_token, demo_phone_number
    ):
        """Test fetching call logs that have transcripts."""
        logger.info("=" * 60)
        logger.info("Fetching call logs WITH TRANSCRIPTS for: %s", demo_phone_number)

        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            params = {
                "limit": 50,
                "offset": 0,
                "page": 1,
                "sort": "-call_date",
                "fields": "*.*",
                "filter[caller_phone][_eq]": demo_phone_number,
                "filter[full_transcript][_nnull]": "true",
            }
            logger.info("Request params: %s", json.dumps(params, indent=2))

            response = await client.get(
                call_logs_api_base,
                params=params,
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            assert response.status_code == 200
            data = response.json()
            records = data.get("data", [])

            logger.info("Found %d call logs with transcripts", len(records))

            # Log sample transcripts
            for i, record in enumerate(records[:3]):
                transcript = record.get("full_transcript", "")
                summary = record.get("summary", "")
                logger.info("Record %d:", i + 1)
                logger.info("  - call_id: %s", record.get("call_id"))
                logger.info("  - call_date: %s", record.get("call_date"))
                logger.info(
                    "  - call_duration: %s seconds", record.get("call_duration")
                )
                logger.info(
                    "  - transcript_length: %d chars",
                    len(transcript) if transcript else 0,
                )
                logger.info(
                    "  - summary: %s",
                    summary[:100] + "..." if len(summary) > 100 else summary,
                )

            # Verify transcripts exist
            for record in records[:5]:
                transcript = record.get("full_transcript")
                assert transcript is not None, (
                    "Filtered records should have transcripts"
                )
                assert len(transcript) > 0, "Transcript should not be empty"


class TestCallLogsDataIntegrity:
    """Test call logs data integrity and format."""

    @pytest.mark.asyncio
    async def test_call_log_date_format(
        self, call_logs_api_base, call_api_token, demo_phone_number
    ):
        """Test that call dates are in valid ISO format."""
        logger.info("Testing call date format validation")

        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                call_logs_api_base,
                params={
                    "limit": 10,
                    "filter[caller_phone][_eq]": demo_phone_number,
                },
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            data = response.json()
            records = data.get("data", [])

            valid_dates = 0
            for record in records:
                call_date = record.get("call_date")
                if call_date:
                    try:
                        parsed = datetime.fromisoformat(
                            call_date.replace("Z", "+00:00")
                        )
                        logger.debug("Valid date: %s -> %s", call_date, parsed)
                        valid_dates += 1
                    except ValueError as e:
                        logger.error("Invalid date format: %s - %s", call_date, e)
                        pytest.fail(f"Invalid date format: {call_date} - {e}")

            logger.info("Validated %d/%d date formats", valid_dates, len(records))

    @pytest.mark.asyncio
    async def test_call_log_required_fields(
        self, call_logs_api_base, call_api_token, demo_phone_number
    ):
        """Test that call logs contain required fields."""
        logger.info("Testing required fields in call log records")

        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                call_logs_api_base,
                params={
                    "limit": 10,
                    "filter[caller_phone][_eq]": demo_phone_number,
                },
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            data = response.json()
            records = data.get("data", [])

            # Expected fields based on the API schema
            expected_fields = {
                "id",
                "caller_phone",
                "call_date",
                "call_duration",
                "summary",
                "call_id",
            }

            logger.info("Checking for required fields: %s", expected_fields)

            for i, record in enumerate(records):
                present_fields = set(record.keys())
                missing = expected_fields - present_fields
                if missing:
                    logger.warning("Record %d missing fields: %s", i, missing)

                # These are absolutely required
                assert "caller_phone" in record, "Missing required field: caller_phone"
                assert "call_date" in record, "Missing required field: call_date"

            logger.info("All %d records have required fields", len(records))


class TestCallLogsSchema:
    """Test that the API response matches the expected schema."""

    @pytest.mark.asyncio
    async def test_response_schema(
        self, call_logs_api_base, call_api_token, demo_phone_number
    ):
        """Validate the full response schema."""
        logger.info("=" * 60)
        logger.info("VALIDATING CALL LOGS API SCHEMA")
        logger.info("=" * 60)

        if not call_api_token:
            pytest.skip("CALL_API_TOKEN not set")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                call_logs_api_base,
                params={
                    "limit": 5,
                    "sort": "-call_date",
                    "fields": "*.*",
                    "filter[caller_phone][_eq]": demo_phone_number,
                    "filter[full_transcript][_nnull]": "true",
                    "meta": "total_count,filter_count",
                },
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {call_api_token}",
                },
                timeout=30.0,
            )

            assert response.status_code == 200
            data = response.json()

            # Log full schema structure
            logger.info("RESPONSE STRUCTURE:")
            logger.info("  - Top-level keys: %s", list(data.keys()))

            if "meta" in data:
                logger.info("  - Meta: %s", json.dumps(data["meta"], indent=4))

            records = data.get("data", [])
            logger.info("  - Data count: %d records", len(records))

            if records:
                record = records[0]
                logger.info("\nCALL LOG RECORD SCHEMA:")
                for key, value in record.items():
                    value_type = type(value).__name__
                    if isinstance(value, str):
                        sample = value[:50] + "..." if len(value) > 50 else value
                        logger.info("  - %s: %s = %r", key, value_type, sample)
                    else:
                        logger.info("  - %s: %s = %r", key, value_type, value)

                # Validate expected schema
                expected_schema = {
                    "id": int,
                    "caller_phone": str,
                    "call_date": str,
                    "call_duration": int,
                    "summary": str,
                    "full_transcript": str,
                    "notes": str,
                    "call_id": str,
                }

                logger.info("\nSCHEMA VALIDATION:")
                for field, expected_type in expected_schema.items():
                    if field in record:
                        actual_value = record[field]
                        # Handle None values
                        if actual_value is None:
                            logger.info("  ✓ %s: None (nullable)", field)
                        elif isinstance(actual_value, expected_type):
                            logger.info(
                                "  ✓ %s: %s (valid)", field, expected_type.__name__
                            )
                        else:
                            logger.warning(
                                "  ✗ %s: expected %s, got %s",
                                field,
                                expected_type.__name__,
                                type(actual_value).__name__,
                            )
                    else:
                        logger.warning("  ✗ %s: MISSING", field)

            logger.info("\nSchema validation complete")
