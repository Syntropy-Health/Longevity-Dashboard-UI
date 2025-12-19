"""Tests for demo data loading and processing."""

import pytest
from datetime import datetime
from longevity_clinic.app.functions.admins.checkins import (
    fetch_all_checkins,
    filter_checkins,
    count_checkins_by_status,
    extract_health_topics,
    get_patient_name_from_phone,
    HealthKeyword,
)
from longevity_clinic.app.data.seed import ADMIN_CHECKINS_SEED, PHONE_TO_PATIENT_SEED


class TestDemoDataStructure:
    """Test the structure and integrity of demo data."""

    def test_demo_checkins_exist(self):
        """Verify demo checkins are loaded."""
        assert len(ADMIN_CHECKINS_SEED) > 0
        assert isinstance(ADMIN_CHECKINS_SEED, list)

    def test_demo_checkin_fields(self):
        """Verify demo checkins have required fields."""
        checkin = ADMIN_CHECKINS_SEED[0]
        required_fields = [
            "id",
            "patient_id",
            "patient_name",
            "timestamp",
            "submitted_at",
            "status",
            "summary",
            "key_topics",
            "sentiment",
        ]
        for field in required_fields:
            assert field in checkin

    def test_phone_mapping_integrity(self):
        """Verify phone mapping data."""
        assert len(PHONE_TO_PATIENT_SEED) > 0
        for phone, name in PHONE_TO_PATIENT_SEED.items():
            assert isinstance(phone, str)
            assert isinstance(name, str)


class TestFetchAllCheckins:
    """Test fetching checkins function."""

    @pytest.mark.asyncio
    async def test_fetch_demo_data(self):
        """Test fetching demo data returns correct list."""
        checkins = await fetch_all_checkins(is_demo=True)
        assert len(checkins) == len(ADMIN_CHECKINS_SEED)
        assert checkins == ADMIN_CHECKINS_SEED

    @pytest.mark.asyncio
    async def test_fetch_with_status_filter(self):
        """Test fetching with status filter."""
        # Count expected pending
        expected = len([c for c in ADMIN_CHECKINS_SEED if c["status"] == "pending"])

        checkins = await fetch_all_checkins(status_filter="pending", is_demo=True)
        assert len(checkins) == expected
        for checkin in checkins:
            assert checkin["status"] == "pending"

    @pytest.mark.asyncio
    async def test_fetch_with_limit(self):
        """Test fetching with limit."""
        limit = 2
        checkins = await fetch_all_checkins(limit=limit, is_demo=True)
        assert len(checkins) <= limit


class TestFilterCheckins:
    """Test filtering logic."""

    def test_filter_by_status(self):
        """Test filtering by status."""
        checkins = ADMIN_CHECKINS_SEED
        pending = filter_checkins(checkins, status="pending")
        assert all(c["status"] == "pending" for c in pending)

        reviewed = filter_checkins(checkins, status="reviewed")
        assert all(c["status"] == "reviewed" for c in reviewed)

    def test_filter_by_search_name(self):
        """Test filtering by search query (name)."""
        checkins = ADMIN_CHECKINS_SEED
        # Find a name from demo data
        target_name = checkins[0]["patient_name"].split()[0]

        results = filter_checkins(checkins, search_query=target_name)
        assert len(results) > 0
        assert all(target_name.lower() in c["patient_name"].lower() for c in results)

    def test_filter_by_search_topic(self):
        """Test filtering by search query (topic)."""
        checkins = ADMIN_CHECKINS_SEED
        # Find a topic from demo data
        target_topic = checkins[0]["key_topics"][0]

        results = filter_checkins(checkins, search_query=target_topic)
        assert len(results) > 0
        # Note: search looks in name, summary, and topics

    def test_filter_combined(self):
        """Test combined status and search filtering."""
        checkins = ADMIN_CHECKINS_SEED
        results = filter_checkins(
            checkins,
            status="pending",
            search_query="Sarah",  # Assuming Sarah is in demo data
        )
        if results:
            assert all(c["status"] == "pending" for c in results)
            assert all("sarah" in c["patient_name"].lower() for c in results)


class TestCountCheckinsByStatus:
    """Test counting logic."""

    def test_count_statuses(self):
        """Test counting checkins by status."""
        checkins = ADMIN_CHECKINS_SEED
        counts = count_checkins_by_status(checkins)

        assert "total" in counts
        assert counts["total"] == len(checkins)

        # Verify sum matches total
        status_sum = sum(v for k, v in counts.items() if k != "total")
        assert status_sum == counts["total"]

        # Verify specific counts
        pending_count = len([c for c in checkins if c["status"] == "pending"])
        assert counts.get("pending", 0) == pending_count


class TestHelperFunctions:
    """Test helper functions."""

    def test_get_patient_name(self):
        """Test phone to name resolution.

        Note: get_patient_name_from_phone now does DB lookup first,
        falling back to formatted phone if not found. In demo mode
        without a DB, it returns the fallback format.
        """
        # Test known number - should return either DB name or seed data name
        known_phone = list(PHONE_TO_PATIENT_SEED.keys())[0]
        result = get_patient_name_from_phone(known_phone)

        # The function should return a name (either from DB or fallback)
        assert result is not None
        assert len(result) > 0
        # Should contain some recognizable part of the expected name
        assert "Sarah" in result or "Patient" in result

        # Test unknown number - should include "Patient" in fallback
        assert "Patient" in get_patient_name_from_phone("9999999999")

    def test_extract_health_topics(self):
        """Test topic extraction."""
        text = "I have been feeling very tired and have a headache."
        topics = extract_health_topics(text)

        assert "tired" in topics or "fatigue" in topics
        assert "headache" in topics

        # Test empty text
        assert extract_health_topics("") == ["voice call"]

        # Test no keywords
        assert extract_health_topics("I went to the store.") == ["voice call"]
