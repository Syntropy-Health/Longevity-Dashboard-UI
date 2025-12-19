"""Tests for database seeding.

Verifies that seed data from demo.py/seed package matches what's loaded in the database.
These tests require a seeded database to pass.
"""

import pytest
from typing import Any

# Database access
from sqlmodel import Session, select

# Models
from longevity_clinic.app.data.model import (
    BiomarkerDefinition,
    BiomarkerReading,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    Notification,
    SymptomEntry,
    Treatment,
    User,
)

# Seed data for comparison
from longevity_clinic.app.data.seed import (
    ADMIN_CHECKINS_SEED,
    ADMIN_NOTIFICATIONS_SEED,
    CHECKIN_SEED_DATA,
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    PATIENT_NOTIFICATIONS_SEED,
    PHONE_TO_PATIENT_SEED,
    PORTAL_BIOMARKERS_SEED,
    SYMPTOMS_SEED,
    TREATMENT_CATALOG_SEED,
    get_all_demo_patients,
)


@pytest.fixture(scope="module")
def db_session():
    """Create a database session for testing.

    Uses Reflex's database engine.
    """
    import reflex as rx

    engine = rx.model.get_engine()
    with Session(engine) as session:
        yield session


class TestUserSeeding:
    """Test user seeding matches seed data."""

    def test_all_demo_patients_exist(self, db_session):
        """Verify all demo patients from seed data exist in database."""
        demo_patients = get_all_demo_patients()

        for patient in demo_patients:
            db_user = db_session.exec(
                select(User).where(User.external_id == patient.external_id)
            ).first()

            assert db_user is not None, f"Patient {patient.name} not found in database"
            assert db_user.name == patient.name
            assert db_user.email == patient.email
            assert db_user.phone == patient.phone
            assert db_user.role == "patient"

    def test_phone_mapping_matches(self, db_session):
        """Verify phone-to-patient mapping matches seed data."""
        for phone, name in PHONE_TO_PATIENT_SEED.items():
            db_user = db_session.exec(select(User).where(User.phone == phone)).first()

            assert db_user is not None, f"User with phone {phone} not found"
            assert db_user.name == name

    def test_admin_user_exists(self, db_session):
        """Verify admin user exists."""
        admin = db_session.exec(
            select(User).where(User.external_id == "ADMIN001")
        ).first()

        assert admin is not None, "Admin user not found"
        assert admin.role == "admin"
        assert admin.name == "Dr. Admin"


class TestCheckinSeeding:
    """Test check-in seeding matches seed data."""

    def test_checkins_count(self, db_session):
        """Verify expected number of check-ins exist."""
        db_count = db_session.exec(select(CheckIn)).all()
        seed_count = len(CHECKIN_SEED_DATA)

        # Database should have at least as many as seed data
        assert (
            len(db_count) >= seed_count
        ), f"Expected at least {seed_count} check-ins, found {len(db_count)}"

    def test_checkin_fields_match(self, db_session):
        """Verify check-in field values match seed data."""
        for seed_checkin in CHECKIN_SEED_DATA:
            checkin_id = seed_checkin.get("id")
            if not checkin_id:
                continue

            db_checkin = db_session.exec(
                select(CheckIn).where(CheckIn.checkin_id == checkin_id)
            ).first()

            if db_checkin:
                assert db_checkin.summary == seed_checkin.get("summary", "")
                assert db_checkin.status == seed_checkin.get("status", "pending")


class TestNotificationSeeding:
    """Test notification seeding matches seed data."""

    def test_notifications_count(self, db_session):
        """Verify expected number of notifications exist."""
        db_count = len(db_session.exec(select(Notification)).all())
        seed_count = len(ADMIN_NOTIFICATIONS_SEED) + len(PATIENT_NOTIFICATIONS_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} notifications, found {db_count}"

    def test_admin_notifications_exist(self, db_session):
        """Verify admin notifications from seed data exist."""
        for seed_notif in ADMIN_NOTIFICATIONS_SEED:
            notif_id = seed_notif.get("id")
            if not notif_id:
                continue

            db_notif = db_session.exec(
                select(Notification).where(Notification.notification_id == notif_id)
            ).first()

            if db_notif:
                assert db_notif.title == seed_notif.get("title", "")
                assert db_notif.recipient_role == seed_notif.get(
                    "recipient_role", "admin"
                )


class TestTreatmentSeeding:
    """Test treatment seeding matches seed data."""

    def test_treatments_count(self, db_session):
        """Verify expected number of treatments exist."""
        db_count = len(db_session.exec(select(Treatment)).all())
        seed_count = len(TREATMENT_CATALOG_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} treatments, found {db_count}"

    def test_treatment_fields_match(self, db_session):
        """Verify treatment field values match seed data."""
        for seed_treatment in TREATMENT_CATALOG_SEED:
            treatment_id = seed_treatment["treatment_id"]

            db_treatment = db_session.exec(
                select(Treatment).where(Treatment.treatment_id == treatment_id)
            ).first()

            if db_treatment:
                assert db_treatment.name == seed_treatment["name"]
                assert db_treatment.category == seed_treatment["category"]


class TestBiomarkerSeeding:
    """Test biomarker seeding matches seed data."""

    def test_biomarker_definitions_count(self, db_session):
        """Verify expected number of biomarker definitions exist."""
        db_count = len(db_session.exec(select(BiomarkerDefinition)).all())
        seed_count = len(PORTAL_BIOMARKERS_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} biomarker definitions, found {db_count}"

    def test_biomarker_definition_fields(self, db_session):
        """Verify biomarker definition fields match seed data."""
        for seed_bio in PORTAL_BIOMARKERS_SEED:
            code = (
                seed_bio["name"]
                .upper()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("(", "")
                .replace(")", "")
            )

            db_bio = db_session.exec(
                select(BiomarkerDefinition).where(BiomarkerDefinition.code == code)
            ).first()

            if db_bio:
                assert db_bio.name == seed_bio["name"]
                assert db_bio.unit == seed_bio["unit"]
                assert db_bio.optimal_min == seed_bio["optimal_min"]
                assert db_bio.optimal_max == seed_bio["optimal_max"]

    def test_biomarker_readings_exist(self, db_session):
        """Verify biomarker readings exist for primary user."""
        readings = db_session.exec(select(BiomarkerReading)).all()

        # Should have some readings from seed data history
        assert len(readings) > 0, "No biomarker readings found in database"


class TestHealthEntriesSeeding:
    """Test health entries seeding matches seed data."""

    def test_medications_count(self, db_session):
        """Verify expected number of medications exist."""
        db_count = len(db_session.exec(select(MedicationEntry)).all())
        seed_count = len(MEDICATIONS_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} medications, found {db_count}"

    def test_food_entries_count(self, db_session):
        """Verify expected number of food entries exist."""
        db_count = len(db_session.exec(select(FoodLogEntry)).all())
        seed_count = len(FOOD_ENTRIES_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} food entries, found {db_count}"

    def test_symptoms_count(self, db_session):
        """Verify expected number of symptoms exist."""
        db_count = len(db_session.exec(select(SymptomEntry)).all())
        seed_count = len(SYMPTOMS_SEED)

        assert (
            db_count >= seed_count
        ), f"Expected at least {seed_count} symptoms, found {db_count}"


class TestSeedDataIntegrity:
    """Test overall seed data integrity."""

    def test_primary_user_has_health_data(self, db_session):
        """Verify primary demo user has associated health data."""
        # Get primary user
        primary_user = db_session.exec(
            select(User).where(User.external_id == "P001")
        ).first()

        if not primary_user:
            pytest.skip("Primary user not found - database may not be seeded")

        # Check medications
        meds = db_session.exec(
            select(MedicationEntry).where(MedicationEntry.user_id == primary_user.id)
        ).all()
        assert len(meds) > 0, "Primary user should have medications"

        # Check food entries
        foods = db_session.exec(
            select(FoodLogEntry).where(FoodLogEntry.user_id == primary_user.id)
        ).all()
        assert len(foods) > 0, "Primary user should have food entries"

        # Check symptoms
        symptoms = db_session.exec(
            select(SymptomEntry).where(SymptomEntry.user_id == primary_user.id)
        ).all()
        assert len(symptoms) > 0, "Primary user should have symptoms"

    def test_primary_user_has_biomarker_readings(self, db_session):
        """Verify primary demo user has biomarker readings."""
        primary_user = db_session.exec(
            select(User).where(User.external_id == "P001")
        ).first()

        if not primary_user:
            pytest.skip("Primary user not found - database may not be seeded")

        readings = db_session.exec(
            select(BiomarkerReading).where(BiomarkerReading.user_id == primary_user.id)
        ).all()
        assert len(readings) > 0, "Primary user should have biomarker readings"


class TestSeedDataConsistency:
    """Test consistency between seed data sources."""

    def test_phone_numbers_are_normalized(self, db_session):
        """Verify phone numbers in database match seed format."""
        users = db_session.exec(select(User).where(User.role == "patient")).all()

        for user in users:
            if user.phone:
                # Check phone is in expected format
                assert user.phone.startswith(
                    "+"
                ), f"Phone {user.phone} for {user.name} should start with +"

    def test_external_ids_are_unique(self, db_session):
        """Verify external IDs are unique."""
        users = db_session.exec(select(User)).all()
        external_ids = [u.external_id for u in users if u.external_id]

        assert len(external_ids) == len(
            set(external_ids)
        ), "External IDs should be unique"
