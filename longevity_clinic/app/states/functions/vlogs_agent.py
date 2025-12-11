"""VlogsAgent - Modular call logs processing agent.

Handles fetching and processing call logs with configurable LLM parsing.
Implements CDC (Change Data Capture) pattern for syncing to database.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import reflex as rx
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from sqlmodel import select

from longevity_clinic.app.config import get_logger, VlogsConfig
from longevity_clinic.app.prompts import PARSE_CHECKIN
from longevity_clinic.app.data.process_schema import CallLogsOutput, CheckInSummary
from longevity_clinic.app.data.state_schemas import CallLogEntry, TranscriptSummary
from longevity_clinic.app.data.model import (
    CallLog,
    CallTranscript,
    CallSummary,
    CheckIn,
    MedicationEntry,
    FoodLogEntry,
    SymptomEntry,
    User,
)

from .utils import fetch_call_logs, format_timestamp

logger = get_logger("longevity_clinic.vlogs_agent")


# =============================================================================
# Constants
# =============================================================================

PHONE_TO_PATIENT_NAME: dict[str, str] = {
    "+12126804645": "Demo Patient (Sarah Chen)",
}


# =============================================================================
# Helper Functions
# =============================================================================


def _get_patient_name(phone: str) -> str:
    """Get patient name from phone number."""
    return PHONE_TO_PATIENT_NAME.get(phone, "Unknown Patient")


def _get_best_summary(api_summary: str, full_transcript: str) -> str:
    """Extract best summary from API or transcript."""
    if api_summary and len(api_summary.strip()) > 20:
        return api_summary.strip()

    if full_transcript:
        transcript = full_transcript.strip()
        user_lines = []
        for line in transcript.split("\n"):
            line = line.strip()
            if line.lower().startswith("user:"):
                user_content = line[5:].strip()
                if user_content:
                    user_lines.append(user_content)

        if user_lines:
            user_summary = " ".join(user_lines)
            return (
                user_summary[:200] + "..." if len(user_summary) > 200 else user_summary
            )

        if len(transcript) > 100 and not transcript.lower().startswith("ai:"):
            return transcript[:300] + "..." if len(transcript) > 300 else transcript

        if len(transcript) < 100:
            return "Brief call - conversation incomplete"

    return "Voice call check-in"


# =============================================================================
# Main Agent Dataclass
# =============================================================================


@dataclass
class VlogsAgent:
    """Agent for processing voice call logs into structured data.

    This agent handles the complete pipeline of:
    1. Fetching call logs from the API
    2. Processing transcripts (with or without LLM)
    3. Extracting structured health data
    4. Generating summaries and metadata

    Usage:
        # Use default config from app settings
        agent = VlogsAgent.from_config()
        
        # Or with custom config
        from longevity_clinic.app.data.process_schema import CallLogsOutput
        config = VlogsConfig(parse_with_llm=True, limit=100, output_schema=CallLogsOutput)
        agent = VlogsAgent(config=config)
        
        # Process logs
        new_count, outputs, summaries = await agent.process_logs(
            phone_number="+1234567890"
        )

    Attributes:
        config: VlogsConfig instance with agent settings
    """

    config: VlogsConfig = field(default_factory=VlogsConfig)
    _llm: Optional[ChatOpenAI] = field(default=None, init=False, repr=False)
    _structured_llm: Optional[object] = field(default=None, init=False, repr=False)

    @classmethod
    def from_config(cls) -> "VlogsAgent":
        """Create VlogsAgent with configuration from app settings."""
        return cls(config=VlogsConfig(output_schema=CallLogsOutput))

    def __post_init__(self):
        if self.config.parse_with_llm:
            self._llm = ChatOpenAI(
                model=self.config.llm_model, temperature=self.config.temperature
            )
            # Use output_schema from config, fallback to CallLogsOutput
            schema = self.config.output_schema or CallLogsOutput
            self._structured_llm = self._llm.with_structured_output(schema)

    async def fetch(
        self,
        phone_number: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[CallLogEntry]:
        """Fetch call logs from API."""
        return await fetch_call_logs(
            phone_number=phone_number, limit=limit or self.config.limit
        )

    async def _parse_with_llm(
        self,
        transcript: str,
        call_id: str,
        call_date: str,
        patient_phone: str,
    ) -> CallLogsOutput:
        """Parse transcript using LLM for structured extraction."""
        try:
            patient_name = _get_patient_name(patient_phone)
            formatted_date = format_timestamp(call_date)

            messages = [
                SystemMessage(content=PARSE_CHECKIN),
                HumanMessage(content=transcript[:4000]),
            ]

            result: CallLogsOutput = await asyncio.to_thread(
                self._structured_llm.invoke, messages
            )

            # Set IDs and metadata
            result.checkin.id = f"call_{call_id}"
            result.checkin.type = "call"
            result.checkin.timestamp = formatted_date
            result.checkin.patient_name = patient_name

            return result

        except Exception as e:
            logger.error("LLM parse failed: %s", e)
            return self._create_fallback_output(
                call_id, call_date, patient_phone, "Parse failed"
            )

    def _parse_simple(
        self,
        api_summary: str,
        transcript: str,
        call_id: str,
        call_date: str,
        patient_phone: str,
    ) -> CallLogsOutput:
        """Simple parsing without LLM."""
        patient_name = _get_patient_name(patient_phone)
        timestamp = format_timestamp(call_date)
        summary = _get_best_summary(api_summary, transcript)

        return CallLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary=summary,
                timestamp=timestamp,
                sentiment="neutral",
                key_topics=["voice"],
                provider_reviewed=False,
                patient_name=patient_name,
            ),
            medications=[],
            food_entries=[],
            has_medications=False,
            has_nutrition=False,
        )

    def _create_fallback_output(
        self,
        call_id: str,
        call_date: str,
        patient_phone: str,
        summary: str = "Voice call check-in",
    ) -> CallLogsOutput:
        """Create fallback output for error cases."""
        return CallLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary=summary,
                timestamp=format_timestamp(call_date),
                sentiment="neutral",
                key_topics=["voice"],
                provider_reviewed=False,
                patient_name=_get_patient_name(patient_phone),
            ),
            medications=[],
            food_entries=[],
            has_medications=False,
            has_nutrition=False,
        )

    async def process_single(
        self,
        log: CallLogEntry,
    ) -> tuple[CallLogsOutput, TranscriptSummary]:
        """Process a single call log entry."""
        call_id = log.get("call_id", "")
        transcript = log.get("full_transcript", "")
        call_date = log.get("call_date", "")
        api_summary = log.get("summary", "") or ""

        raw_phone = log.get("caller_phone", "")
        patient_phone = (
            raw_phone.get("phone_number", "")
            if isinstance(raw_phone, dict)
            else raw_phone
        )

        if self.config.parse_with_llm and self._structured_llm:
            output = await self._parse_with_llm(
                transcript, call_id, call_date, patient_phone
            )
        else:
            output = self._parse_simple(
                api_summary, transcript, call_id, call_date, patient_phone
            )

        summary: TranscriptSummary = {
            "call_id": call_id,
            "patient_phone": patient_phone,
            "call_date": call_date,
            "summary": api_summary,
            "ai_summary": output.checkin.summary,
            "type": "call",
            "timestamp": output.checkin.timestamp,
        }

        return output, summary

    async def process_logs(
        self,
        phone_number: Optional[str] = None,
        processed_ids: Optional[set[str]] = None,
    ) -> tuple[int, list[CallLogsOutput], dict[str, TranscriptSummary]]:
        """Main entrypoint: fetch and process call logs.

        Args:
            phone_number: Filter by phone (None = all logs)
            processed_ids: Skip these call IDs

        Returns:
            Tuple of (new_count, outputs, summaries)
        """
        processed_ids = processed_ids or set()

        # Fetch logs
        call_logs = await self.fetch(phone_number=phone_number)
        logger.info("Fetched %d call logs", len(call_logs))

        # Process each log
        new_count = 0
        outputs: list[CallLogsOutput] = []
        summaries: dict[str, TranscriptSummary] = {}

        for log in call_logs:
            call_id = log.get("call_id", "")
            if not call_id or call_id in processed_ids:
                continue

            new_count += 1
            output, summary = await self.process_single(log)
            outputs.append(output)
            summaries[call_id] = summary

        logger.info("Processed %d new call logs", new_count)
        return new_count, outputs, summaries

    # =========================================================================
    # Database Sync Methods (CDC Pattern)
    # =========================================================================

    def get_processed_call_ids_sync(self) -> set[str]:
        """Get set of call_ids already in database (sync version)."""
        with rx.session() as session:
            result = session.exec(select(CallLog.call_id))
            return set(result.all())

    def get_user_by_phone_sync(self, phone: str) -> Optional[int]:
        """Get user_id by phone number (sync version)."""
        with rx.session() as session:
            result = session.exec(
                select(User).where(User.phone == phone)
            )
            user = result.first()
            return user.id if user else None

    def sync_single_to_db_sync(
        self,
        log: CallLogEntry,
        output: CallLogsOutput,
        summary: TranscriptSummary,
    ) -> Optional[int]:
        """Sync a single processed call log to database (sync version).
        
        Returns the call_log_id if successful.
        """
        call_id = log.get("call_id", "")
        if not call_id:
            return None

        try:
            with rx.session() as session:
                # Check if already exists
                existing = session.exec(
                    select(CallLog).where(CallLog.call_id == call_id)
                ).first()
                if existing:
                    logger.debug("Call %s already in DB, skipping", call_id)
                    return None

                # Get user_id from phone
                raw_phone = log.get("caller_phone", "")
                phone = (
                    raw_phone.get("phone_number", "")
                    if isinstance(raw_phone, dict)
                    else raw_phone
                )
                user_id = self.get_user_by_phone_sync(phone)

                # Parse call date
                call_date_str = log.get("call_date", "")
                try:
                    started_at = datetime.fromisoformat(
                        call_date_str.replace("Z", "+00:00")
                    )
                except (ValueError, AttributeError):
                    started_at = datetime.now(timezone.utc)

                # 1. Create CallLog
                call_log = CallLog(
                    call_id=call_id,
                    user_id=user_id,
                    phone_number=phone,
                    direction="inbound",
                    duration_seconds=log.get("duration", 0),
                    started_at=started_at,
                    status="completed",
                )
                session.add(call_log)
                session.flush()  # Get the ID
                call_log_id = call_log.id

                # 2. Create CallTranscript
                transcript = CallTranscript(
                    call_log_id=call_log_id,
                    call_id=call_id,
                    raw_transcript=log.get("full_transcript", ""),
                    language="en",
                )
                session.add(transcript)

                # 3. Create CallSummary with LLM output
                medications = getattr(output, 'medications_entries', []) or getattr(output, 'medications', [])
                symptom_entries = getattr(output, 'symptom_entries', [])
                call_summary = CallSummary(
                    call_log_id=call_log_id,
                    call_id=call_id,
                    summary=output.checkin.summary,
                    health_topics=json.dumps(output.checkin.key_topics),
                    sentiment=output.checkin.sentiment,
                    urgency_level="routine",
                    medications_json=json.dumps(
                        [m.model_dump() for m in medications]
                    ) if medications else None,
                    food_entries_json=json.dumps(
                        [f.model_dump() for f in output.food_entries]
                    ) if output.food_entries else None,
                    symptoms_json=json.dumps(
                        [s.model_dump() for s in symptom_entries]
                    ) if symptom_entries else None,
                    has_medications=output.has_medications,
                    has_nutrition=output.has_nutrition,
                    has_symptoms=getattr(output, 'has_symptoms', False),
                    llm_model=self.config.llm_model if self.config.parse_with_llm else None,
                )
                session.add(call_summary)
                session.flush()
                summary_id = call_summary.id

                # 4. Create CheckIn
                checkin = CheckIn(
                    checkin_id=output.checkin.id,
                    user_id=user_id,
                    call_log_id=call_log_id,
                    patient_name=output.checkin.patient_name,
                    checkin_type="call",
                    summary=output.checkin.summary,
                    raw_content=log.get("full_transcript", ""),
                    health_topics=json.dumps(output.checkin.key_topics),
                    status="pending",
                    timestamp=started_at,
                )
                session.add(checkin)

                # 5. Create normalized MedicationEntry records
                med_count = 0
                medications = getattr(output, 'medications_entries', []) or getattr(output, 'medications', [])
                for med in medications:
                    med_entry = MedicationEntry(
                        user_id=user_id,
                        call_log_id=call_log_id,
                        summary_id=summary_id,
                        name=med.name,
                        dosage=med.dosage,
                        frequency=med.frequency,
                        status=med.status,
                        adherence_rate=med.adherence_rate,
                        source="call_log",
                        mentioned_at=started_at,
                    )
                    session.add(med_entry)
                    med_count += 1

                # 6. Create normalized FoodLogEntry records
                food_count = 0
                for food in output.food_entries:
                    food_entry = FoodLogEntry(
                        user_id=user_id,
                        call_log_id=call_log_id,
                        summary_id=summary_id,
                        name=food.name,
                        calories=food.calories,
                        protein=food.protein,
                        carbs=food.carbs,
                        fat=food.fat,
                        meal_type=food.meal_type,
                        consumed_at=food.time,
                        source="call_log",
                        logged_at=started_at,
                    )
                    session.add(food_entry)
                    food_count += 1

                # 7. Create normalized SymptomEntry records
                symptom_count = 0
                symptom_entries = getattr(output, 'symptom_entries', [])
                for sym in symptom_entries:
                    sym_entry = SymptomEntry(
                        user_id=user_id,
                        call_log_id=call_log_id,
                        summary_id=summary_id,
                        name=sym.name,
                        severity=sym.severity,
                        frequency=sym.frequency,
                        trend=sym.trend,
                        source="call_log",
                        reported_at=started_at,
                    )
                    session.add(sym_entry)
                    symptom_count += 1

                session.commit()
                logger.info(
                    "Synced call %s to DB (id=%d): %d meds, %d foods, %d symptoms",
                    call_id, call_log_id, med_count, food_count, symptom_count
                )
                return call_log_id

        except Exception as e:
            logger.error("Failed to sync call %s to DB: %s", call_id, e)
            return None

    async def process_and_sync(
        self,
        phone_number: Optional[str] = None,
    ) -> tuple[int, list[CallLogsOutput]]:
        """Full CDC pipeline: fetch, diff, process, sync.
        
        Returns:
            Tuple of (new_count, outputs)
        """
        # 1. Get already processed IDs from DB (sync call in thread)
        processed_ids = await asyncio.to_thread(self.get_processed_call_ids_sync)
        logger.info("Found %d existing call logs in DB", len(processed_ids))

        # 2. Fetch from API
        call_logs = await self.fetch(phone_number=phone_number)
        logger.info("Fetched %d call logs from API", len(call_logs))

        # 3. Filter to new logs only
        new_logs = [
            log for log in call_logs
            if log.get("call_id") and log.get("call_id") not in processed_ids
        ]
        logger.info("Found %d new call logs to process", len(new_logs))

        if not new_logs:
            return 0, []

        # 4. Process each new log with LLM and sync to DB
        outputs: list[CallLogsOutput] = []
        synced_count = 0

        for log in new_logs:
            output, summary = await self.process_single(log)
            outputs.append(output)
            
            # Sync to database (sync call in thread)
            call_log_id = await asyncio.to_thread(
                self.sync_single_to_db_sync, log, output, summary
            )
            if call_log_id:
                synced_count += 1

        logger.info("Processed and synced %d new call logs", synced_count)
        return synced_count, outputs
