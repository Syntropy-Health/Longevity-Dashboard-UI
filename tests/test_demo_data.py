"""Tests for demo data loading and processing."""

import pytest

from longevity_clinic.app.data.seed import ADMIN_CHECKINS_SEED, PHONE_TO_PATIENT_SEED
from longevity_clinic.app.functions.admins.checkins import (
    count_checkins_by_status,
    extract_health_topics,
    fetch_all_checkins,
    filter_checkins,
    get_patient_name_from_phone,
)


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
    """Test fetching checkins function from database."""

    @pytest.mark.asyncio
    async def test_fetch_checkins(self):
        """Test fetching checkins from database returns a list."""
        checkins = await fetch_all_checkins()
        assert isinstance(checkins, list)
        # Could be empty if DB not seeded, or populated if seeded

    @pytest.mark.asyncio
    async def test_fetch_with_status_filter(self):
        """Test fetching with status filter."""
        checkins = await fetch_all_checkins(status_filter="pending")
        # All returned should have pending status
        for checkin in checkins:
            assert checkin["status"] == "pending"

    @pytest.mark.asyncio
    async def test_fetch_with_limit(self):
        """Test fetching with limit."""
        limit = 2
        checkins = await fetch_all_checkins(limit=limit)
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

        get_patient_name_from_phone does DB lookup first,
        falling back to formatted phone if not found.
        """
        # Test known number from seed data
        known_phone = next(iter(PHONE_TO_PATIENT_SEED.keys()))
        result = get_patient_name_from_phone(known_phone)

        # The function should return a name (either from DB or fallback)
        assert result is not None
        assert len(result) > 0

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
