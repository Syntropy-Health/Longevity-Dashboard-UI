"""Call log seed data loading."""

from __future__ import annotations

import json
from datetime import datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.model import (
    CallLog,
    CallSummary,
    CallTranscript,
    User,
)

from .base import SeedResult, print_section


# Sample call logs for demo purposes
def _get_sample_calls(primary_phone: str, primary_name: str) -> list[dict]:
    """Generate sample call log data for the primary demo user."""
    return [
        {
            "call_id": "CALL-SEED-001",
            "phone_number": primary_phone,
            "direction": "inbound",
            "duration_seconds": 180,
            "started_at": datetime(2025, 1, 15, 10, 30, 0),
            "transcript": f"Hi, this is {primary_name}. I wanted to report that I've been taking my Metformin regularly. Also had a healthy breakfast with Greek yogurt and berries.",
            "summary": "Patient reported medication adherence and healthy eating habits.",
            "health_topics": ["medications", "nutrition"],
        },
        {
            "call_id": "CALL-SEED-002",
            "phone_number": primary_phone,
            "direction": "inbound",
            "duration_seconds": 240,
            "started_at": datetime(2025, 1, 14, 14, 15, 0),
            "transcript": f"Hi, it's {primary_name}. I've been feeling a bit tired lately, maybe 5 out of 10 energy. My blood pressure was 128/82 this morning. I did my 30-minute walk yesterday.",
            "summary": "Patient reported moderate fatigue, blood pressure reading within range, and exercise compliance.",
            "health_topics": ["energy", "vitals", "exercise"],
        },
        {
            "call_id": "CALL-SEED-003",
            "phone_number": primary_phone,
            "direction": "inbound",
            "duration_seconds": 120,
            "started_at": datetime(2025, 1, 13, 9, 0, 0),
            "transcript": f"Hi, {primary_name} here. Just checking in - slept well last night, about 7 hours. Had some mild joint stiffness in the morning but it went away after stretching.",
            "summary": "Patient reported good sleep quality and mild morning joint stiffness that resolved with stretching.",
            "health_topics": ["sleep", "symptoms"],
        },
    ]


def load_call_logs(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load sample call logs for demo purposes.

    All sample calls are linked to the primary demo user (Sarah Chen).

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading sample call logs")
    result = SeedResult(name="call_logs")

    # Get primary demo user's phone from config
    from longevity_clinic.app.config import current_config

    primary_phone = current_config.demo_user.phone
    primary_name = current_config.demo_user.full_name

    sample_calls = _get_sample_calls(primary_phone, primary_name)

    for call_data in sample_calls:
        # Check if exists
        existing = session.exec(
            select(CallLog).where(CallLog.call_id == call_data["call_id"])
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {call_data['call_id']}")
            result.skipped += 1
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
            llm_model="seed-data",
        )
        session.add(summary)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} call logs with transcripts and summaries")
    return result
