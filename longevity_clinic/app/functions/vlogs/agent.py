"""VlogsAgent - Call log processing with CDC pattern."""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Set, Tuple

from langchain_core.language_models import BaseChatModel

from longevity_clinic.app.config import VlogsConfig, get_logger
from longevity_clinic.app.data.process_schema import CallLogsOutput, CheckInSummary
from longevity_clinic.app.data.state_schemas import CallLogEntry, TranscriptSummary
from longevity_clinic.app.prompts import PARSE_CHECKIN

from ..llm import get_structured_output_model, parse_with_structured_output
from ..utils import fetch_call_logs, format_timestamp
from .db import (
    get_transcript_for_call_log,
    get_unprocessed_call_logs_sync,
    sync_raw_log_to_db,
    update_call_log_metrics,
)
from .utils import get_best_summary, get_patient_name, parse_phone

logger = get_logger("longevity_clinic.vlogs.agent")


@dataclass
class VlogsAgent:
    """Agent for CDC call log processing pipeline.

    Primary API (used in CheckinState):
    - parse_user_checkin(): Static method for manual/voice check-ins
    - fetch_and_sync_raw(): CDC steps 1-2 (fetch API → sync to DB)
    - process_unprocessed_logs(): CDC steps 3-4 (LLM process → update metrics)
    """

    config: VlogsConfig = field(default_factory=VlogsConfig)
    _structured_llm: Optional[BaseChatModel] = field(
        default=None, init=False, repr=False
    )

    @classmethod
    def from_config(cls) -> "VlogsAgent":
        """Create agent with app default config."""
        return cls(config=VlogsConfig(output_schema=CallLogsOutput))

    def __post_init__(self):
        if self.config.extract_with_llm:
            self._structured_llm = get_structured_output_model(
                output_schema=self.config.output_schema or CallLogsOutput,
                model=self.config.llm_model,
                temperature=self.config.temperature,
            )

    # =========================================================================
    # Static: Manual/Voice Check-in Parsing
    # =========================================================================

    @staticmethod
    async def parse_user_checkin(
        content: str, checkin_type: str = "text"
    ) -> CheckInSummary:
        """Parse user-entered text into CheckInSummary (not call logs)."""
        checkin_id = f"chk_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().strftime("Today, %I:%M %p")

        # Fallback for empty/short content - no fake data
        if not content or len(content.strip()) < 10:
            return CheckInSummary(
                id=checkin_id,
                type=checkin_type,
                summary=content[:500] if content else "",
                timestamp=timestamp,
                sentiment="",
                key_topics=[],
                provider_reviewed=False,
                patient_name="",
            )

        # Try LLM parsing
        result = await parse_with_structured_output(
            content=content,
            output_schema=CheckInSummary,
            system_prompt=PARSE_CHECKIN,
            max_content_length=2000,
        )

        if result:
            # Override system-generated fields
            result.id = checkin_id
            result.type = checkin_type
            result.timestamp = timestamp
            result.provider_reviewed = False
            # Keep LLM values, don't force defaults
            result.key_topics = result.key_topics or []
            result.summary = result.summary or content[:500]
            return result

        # LLM failed - return with raw content, no fake sentiment
        logger.warning("parse_user_checkin LLM returned None")
        return CheckInSummary(
            id=checkin_id,
            type=checkin_type,
            summary=content[:500],
            timestamp=timestamp,
            sentiment="",
            key_topics=[],
            provider_reviewed=False,
            patient_name="",
        )

    @staticmethod
    async def parse_checkin_with_health_data(
        content: str, checkin_type: str = "text", patient_name: str = ""
    ) -> CallLogsOutput:
        """Parse user-entered text into CallLogsOutput with full health extraction.
        
        This method extracts not just the check-in summary, but also:
        - Medications mentioned
        - Food/nutrition items
        - Symptoms reported
        
        Use this for voice/text check-ins when you want to persist health data to DB.
        
        Args:
            content: The transcript or text content
            checkin_type: "voice" or "text"
            patient_name: Patient's display name
            
        Returns:
            CallLogsOutput with checkin summary and health entries
        """
        checkin_id = f"chk_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().strftime("Today, %I:%M %p")

        # Fallback for empty/short content
        if not content or len(content.strip()) < 10:
            return CallLogsOutput(
                checkin=CheckInSummary(
                    id=checkin_id,
                    type=checkin_type,
                    summary=content[:500] if content else "",
                    timestamp=timestamp,
                    sentiment="neutral",
                    key_topics=[],
                    provider_reviewed=False,
                    patient_name=patient_name,
                ),
                medications_entries=[],
                food_entries=[],
                symptom_entries=[],
                has_medications=False,
                has_nutrition=False,
                has_symptoms=False,
            )

        # Try LLM parsing with full CallLogsOutput schema
        result = await parse_with_structured_output(
            content=content,
            output_schema=CallLogsOutput,
            system_prompt=PARSE_CHECKIN,
            max_content_length=4000,
        )

        if result:
            # Override system-generated fields in checkin
            result.checkin.id = checkin_id
            result.checkin.type = checkin_type
            result.checkin.timestamp = timestamp
            result.checkin.provider_reviewed = False
            result.checkin.patient_name = patient_name or result.checkin.patient_name
            result.checkin.summary = result.checkin.summary or content[:500]
            result.checkin.key_topics = result.checkin.key_topics or []
            
            # Ensure flags are set correctly
            result.has_medications = len(result.medications_entries) > 0
            result.has_nutrition = len(result.food_entries) > 0
            result.has_symptoms = len(result.symptom_entries) > 0
            
            logger.info(
                "Parsed checkin with health data: %d meds, %d foods, %d symptoms",
                len(result.medications_entries),
                len(result.food_entries),
                len(result.symptom_entries),
            )
            return result

        # LLM failed - return empty health data
        logger.warning("parse_checkin_with_health_data LLM returned None")
        return CallLogsOutput(
            checkin=CheckInSummary(
                id=checkin_id,
                type=checkin_type,
                summary=content[:500],
                timestamp=timestamp,
                sentiment="neutral",
                key_topics=[],
                provider_reviewed=False,
                patient_name=patient_name,
            ),
            medications_entries=[],
            food_entries=[],
            symptom_entries=[],
            has_medications=False,
            has_nutrition=False,
            has_symptoms=False,
        )

    # =========================================================================
    # CDC Pipeline: fetch_and_sync_raw → process_unprocessed_logs
    # =========================================================================

    async def fetch_and_sync_raw(self, phone_number: Optional[str] = None) -> int:
        """CDC Steps 1-2: Fetch from API and sync raw logs to DB."""
        call_logs = await fetch_call_logs(
            phone_number=phone_number, limit=self.config.limit
        )
        if not call_logs:
            return 0
        count = 0
        for log in call_logs:
            if await asyncio.to_thread(sync_raw_log_to_db, log):
                count += 1
        return count

    async def process_unprocessed_logs(self) -> int:
        """CDC Steps 3-4: Process unprocessed logs with LLM."""
        if not self.config.extract_with_llm:
            return 0

        unprocessed = await asyncio.to_thread(get_unprocessed_call_logs_sync)
        if not unprocessed:
            return 0

        logger.info("Processing %d unprocessed call logs", len(unprocessed))
        count = 0
        for call_log in unprocessed:
            try:
                transcript = await asyncio.to_thread(
                    get_transcript_for_call_log, call_log.id
                )
                if not transcript:
                    continue

                output = await self._parse_with_llm(
                    transcript,
                    call_log.call_id,
                    call_log.started_at.isoformat(),
                    call_log.phone_number,
                )
                if await asyncio.to_thread(
                    update_call_log_metrics, call_log.id, output, self.config.llm_model
                ):
                    count += 1
            except Exception as e:
                logger.error("Failed to process call %s: %s", call_log.call_id, e)
        return count

    # =========================================================================
    # Internal: LLM Parsing
    # =========================================================================

    async def _parse_with_llm(
        self, transcript: str, call_id: str, call_date: str, patient_phone: str
    ) -> CallLogsOutput:
        """Parse transcript with LLM for structured extraction."""
        from langchain_core.messages import HumanMessage, SystemMessage

        patient_name = get_patient_name(patient_phone)
        formatted_date = format_timestamp(call_date)

        if not transcript or len(transcript.strip()) < 10:
            return self._fallback_output(call_id, formatted_date, patient_name)

        try:
            result: CallLogsOutput = await self._structured_llm.ainvoke(
                [
                    SystemMessage(content=PARSE_CHECKIN),
                    HumanMessage(content=transcript[:4000]),
                ]
            )
            # Defensive check: ensure checkin exists
            if result.checkin is None:
                logger.warning("LLM returned None checkin for call %s", call_id)
                return self._fallback_output(call_id, formatted_date, patient_name)

            result.checkin.id = f"call_{call_id}"
            result.checkin.type = "call"
            result.checkin.timestamp = formatted_date
            result.checkin.patient_name = patient_name
            return result
        except Exception as e:
            logger.error("LLM parse failed for call %s: %s", call_id, e)
            return self._fallback_output(
                call_id, formatted_date, patient_name, summary=""
            )

    def _fallback_output(
        self, call_id: str, timestamp: str, patient_name: str, summary: str = ""
    ) -> CallLogsOutput:
        """Create fallback output when LLM fails or transcript is empty."""
        return CallLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary=summary,
                timestamp=timestamp,
                sentiment="",
                key_topics=[],
                provider_reviewed=False,
                patient_name=patient_name,
            ),
            medications_entries=[],
            food_entries=[],
            has_medications=False,
            has_nutrition=False,
        )

    # =========================================================================
    # Legacy API (for tests/backwards compat) - consider deprecating
    # =========================================================================

    async def fetch(
        self, phone_number: Optional[str] = None, limit: Optional[int] = None
    ) -> List[CallLogEntry]:
        """Fetch call logs from API."""
        return await fetch_call_logs(
            phone_number=phone_number, limit=limit or self.config.limit
        )

    async def process_logs(
        self,
        phone_number: Optional[str] = None,
        processed_ids: Optional[Set[str]] = None,
    ) -> Tuple[int, List[CallLogsOutput], dict[str, TranscriptSummary]]:
        """Fetch and process logs (legacy - without DB sync). Used by tests."""
        processed_ids = processed_ids or set()
        call_logs = await self.fetch(phone_number=phone_number)

        new_count, outputs, summaries = 0, [], {}
        for log in call_logs:
            call_id = log.get("call_id", "")
            if not call_id or call_id in processed_ids:
                continue
            new_count += 1
            patient_phone = parse_phone(log.get("caller_phone", ""))
            output = self.parse_transcript(
                log.get("summary", ""),
                log.get("full_transcript", ""),
                call_id,
                log.get("call_date", ""),
                patient_phone,
            )
            outputs.append(output)
            summaries[call_id] = TranscriptSummary(
                call_id=call_id,
                patient_phone=patient_phone,
                call_date=log.get("call_date", ""),
                summary=log.get("summary", ""),
                ai_summary=output.checkin.summary,
                type="call",
                timestamp=output.checkin.timestamp,
            )
        return new_count, outputs, summaries

    def parse_transcript(
        self,
        api_summary: str,
        transcript: str,
        call_id: str,
        call_date: str,
        patient_phone: str,
    ) -> CallLogsOutput:
        """Parse without LLM (fallback/no-LLM mode)."""
        return CallLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary=get_best_summary(api_summary, transcript),
                timestamp=format_timestamp(call_date),
                sentiment="",
                key_topics=[],
                provider_reviewed=False,
                patient_name=get_patient_name(patient_phone),
            ),
            medications_entries=[],
            food_entries=[],
            has_medications=False,
            has_nutrition=False,
        )
