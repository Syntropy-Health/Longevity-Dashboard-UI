#!/usr/bin/env python
"""Load demo data into the SQLite database.

Run this script to populate a fresh database with demo data:
    python scripts/load_demo_data.py

Or to reset and reload:
    python scripts/load_demo_data.py --reset
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize Reflex config to set up database URL
import rxconfig  # noqa: F401

import reflex as rx
from sqlmodel import Session, select

from longevity_clinic.app.data.model import (
    User,
    CallLog,
    CallTranscript,
    CallSummary,
    CheckIn,
    Notification,
)
from longevity_clinic.app.data.demo import (
    DEMO_PATIENTS,
    DEMO_CHECKINS,
    ADMIN_NOTIFICATIONS_DEMO,
    PATIENT_NOTIFICATIONS_DEMO,
    PHONE_TO_PATIENT,
)


def get_engine():
    """Get SQLAlchemy engine from Reflex."""
    return rx.model.get_engine()


def create_tables(engine):
    """Create all database tables."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    print("✓ Created database tables")


def drop_tables(engine):
    """Drop all database tables."""
    from sqlmodel import SQLModel
    SQLModel.metadata.drop_all(engine)
    print("✓ Dropped existing tables")


def load_users(session: Session) -> dict[str, int]:
    """Load demo users and return mapping of external_id to db id."""
    print("\n📥 Loading users...")
    user_id_map = {}
    
    for patient in DEMO_PATIENTS:
        # Check if user exists
        existing = session.exec(
            select(User).where(User.external_id == patient["id"])
        ).first()
        
        if existing:
            user_id_map[patient["id"]] = existing.id
            print(f"  ○ Skipped (exists): {patient['name']}")
            continue
        
        # Get phone from mapping
        phone = None
        for p, name in PHONE_TO_PATIENT.items():
            if patient["name"] in name:
                phone = p
                break
        
        user = User(
            external_id=patient["id"],
            name=patient["name"],
            email=patient["email"],
            phone=phone,
            role="patient",
        )
        session.add(user)
        session.flush()  # Get the ID
        user_id_map[patient["id"]] = user.id
        print(f"  ✓ Created: {patient['name']} (id={user.id})")
    
    # Add admin user
    admin = session.exec(
        select(User).where(User.external_id == "ADMIN001")
    ).first()
    
    if not admin:
        admin = User(
            external_id="ADMIN001",
            name="Dr. Admin",
            email="admin@longevityclinic.com",
            role="admin",
        )
        session.add(admin)
        session.flush()
        print(f"  ✓ Created: Dr. Admin (id={admin.id})")
    
    session.commit()
    print(f"  Total users: {len(user_id_map) + 1}")
    return user_id_map


def load_checkins(session: Session, user_id_map: dict[str, int]) -> None:
    """Load demo check-ins."""
    print("\n📥 Loading check-ins...")
    count = 0
    
    for checkin_data in DEMO_CHECKINS:
        checkin_id = checkin_data.get("id", f"CHK-{count:03d}")
        
        # Check if exists
        existing = session.exec(
            select(CheckIn).where(CheckIn.checkin_id == checkin_id)
        ).first()
        
        if existing:
            print(f"  ○ Skipped (exists): {checkin_id}")
            continue
        
        # Parse timestamp
        timestamp_str = checkin_data.get("timestamp", "")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            timestamp = datetime.now(timezone.utc)
        
        # Get user_id from patient_name
        user_id = None
        patient_name = checkin_data.get("patient_name", "Unknown")
        for ext_id, db_id in user_id_map.items():
            # Simple name matching
            if ext_id in checkin_data.get("patient_id", ""):
                user_id = db_id
                break
        
        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=user_id,
            patient_name=patient_name,
            checkin_type=checkin_data.get("type", "manual"),
            summary=checkin_data.get("summary", ""),
            raw_content=checkin_data.get("content", checkin_data.get("transcript", "")),
            health_topics=json.dumps(checkin_data.get("health_topics", [])),
            mood=checkin_data.get("mood"),
            energy_level=checkin_data.get("energy_level"),
            status=checkin_data.get("status", "pending"),
            provider_reviewed=checkin_data.get("provider_reviewed", False),
            reviewed_by=checkin_data.get("reviewed_by"),
            timestamp=timestamp,
        )
        session.add(checkin)
        count += 1
    
    session.commit()
    print(f"  ✓ Loaded {count} check-ins")


def load_notifications(session: Session, user_id_map: dict[str, int]) -> None:
    """Load demo notifications."""
    print("\n📥 Loading notifications...")
    count = 0
    
    all_notifications = ADMIN_NOTIFICATIONS_DEMO + PATIENT_NOTIFICATIONS_DEMO
    
    for notif_data in all_notifications:
        notif_id = notif_data.get("id", f"NOTIF-{count:03d}")
        
        # Check if exists
        existing = session.exec(
            select(Notification).where(Notification.notification_id == notif_id)
        ).first()
        
        if existing:
            print(f"  ○ Skipped (exists): {notif_id}")
            continue
        
        # Parse timestamp
        timestamp_str = notif_data.get("created_at", "")
        try:
            created_at = datetime.fromisoformat(timestamp_str)
        except (ValueError, AttributeError):
            created_at = datetime.now(timezone.utc)
        
        # Map patient_id to user_id
        user_id = None
        patient_id = notif_data.get("patient_id")
        if patient_id and patient_id != "current" and patient_id in user_id_map:
            user_id = user_id_map[patient_id]
        
        notification = Notification(
            notification_id=notif_id,
            user_id=user_id,
            recipient_role=notif_data.get("recipient_role", "patient"),
            title=notif_data.get("title", ""),
            message=notif_data.get("message", ""),
            notification_type=notif_data.get("type", "info"),
            is_read=notif_data.get("is_read", False),
            patient_id=patient_id,
            created_at=created_at,
        )
        session.add(notification)
        count += 1
    
    session.commit()
    print(f"  ✓ Loaded {count} notifications")


def load_sample_call_logs(session: Session, user_id_map: dict[str, int]) -> None:
    """Load sample call logs for demo purposes."""
    print("\n📥 Loading sample call logs...")
    
    # Sample call logs based on PHONE_TO_PATIENT mapping
    sample_calls = [
        {
            "call_id": "CALL-DEMO-001",
            "phone_number": "+12126804645",
            "direction": "inbound",
            "duration_seconds": 180,
            "started_at": datetime(2025, 1, 15, 10, 30, 0),
            "transcript": "Hi, I wanted to report that I've been taking my Metformin regularly. Also had a healthy breakfast with Greek yogurt and berries.",
            "summary": "Patient reported medication adherence and healthy eating habits.",
            "health_topics": ["medications", "nutrition"],
        },
        {
            "call_id": "CALL-DEMO-002", 
            "phone_number": "+12126804645",
            "direction": "inbound",
            "duration_seconds": 240,
            "started_at": datetime(2025, 1, 14, 14, 15, 0),
            "transcript": "I've been feeling a bit tired lately, maybe 5 out of 10 energy. My blood pressure was 128/82 this morning. I did my 30-minute walk yesterday.",
            "summary": "Patient reported moderate fatigue, blood pressure reading within range, and exercise compliance.",
            "health_topics": ["energy", "vitals", "exercise"],
        },
        {
            "call_id": "CALL-DEMO-003",
            "phone_number": "+12126804645",
            "direction": "inbound",
            "duration_seconds": 120,
            "started_at": datetime(2025, 1, 13, 9, 0, 0),
            "transcript": "Just checking in - slept well last night, about 7 hours. Had some mild joint stiffness in the morning but it went away after stretching.",
            "summary": "Patient reported good sleep quality and mild morning joint stiffness that resolved with stretching.",
            "health_topics": ["sleep", "symptoms"],
        },
    ]
    
    count = 0
    for call_data in sample_calls:
        # Check if exists
        existing = session.exec(
            select(CallLog).where(CallLog.call_id == call_data["call_id"])
        ).first()
        
        if existing:
            print(f"  ○ Skipped (exists): {call_data['call_id']}")
            continue
        
        # Find user_id from phone
        user_id = None
        for ext_id, db_id in user_id_map.items():
            user = session.exec(select(User).where(User.id == db_id)).first()
            if user and user.phone == call_data["phone_number"]:
                user_id = db_id
                break
        
        # Create call log
        call_log = CallLog(
            call_id=call_data["call_id"],
            user_id=user_id,
            phone_number=call_data["phone_number"],
            direction=call_data["direction"],
            duration_seconds=call_data["duration_seconds"],
            started_at=call_data["started_at"],
            status="completed",
        )
        session.add(call_log)
        session.flush()
        
        # Create transcript
        transcript = CallTranscript(
            call_log_id=call_log.id,
            call_id=call_data["call_id"],
            raw_transcript=call_data["transcript"],
            language="en",
        )
        session.add(transcript)
        
        # Create summary
        summary = CallSummary(
            call_log_id=call_log.id,
            call_id=call_data["call_id"],
            summary=call_data["summary"],
            health_topics=json.dumps(call_data["health_topics"]),
            urgency_level="routine",
            has_medications="medications" in call_data["health_topics"],
            has_nutrition="nutrition" in call_data["health_topics"],
            has_symptoms="symptoms" in call_data["health_topics"],
            llm_model="demo-data",
        )
        session.add(summary)
        count += 1
    
    session.commit()
    print(f"  ✓ Loaded {count} call logs with transcripts and summaries")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Load demo data into database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before loading (WARNING: destroys existing data)",
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("Longevity Clinic - Demo Data Loader")
    print("=" * 60)
    
    engine = get_engine()
    
    if args.reset:
        print("\n⚠️  Resetting database (--reset flag)")
        drop_tables(engine)
    
    create_tables(engine)
    
    with Session(engine) as session:
        user_id_map = load_users(session)
        load_checkins(session, user_id_map)
        load_notifications(session, user_id_map)
        load_sample_call_logs(session, user_id_map)
    
    print("\n" + "=" * 60)
    print("✅ Demo data loaded successfully!")
    print("=" * 60)
    print("\nDatabase location: sqlite:///reflex.db")
    print("Run `reflex db migrate` if you haven't already to sync schema.")


if __name__ == "__main__":
    main()
