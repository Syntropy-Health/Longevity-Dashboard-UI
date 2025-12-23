"""VlogsAgent - Call log processing with CDC pattern."""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from langchain_core.language_models import BaseChatModel

from longevity_clinic.app.config import VlogsConfig, get_logger
from longevity_clinic.app.data.process_schema import CheckInSummary, MetricLogsOutput
from longevity_clinic.app.prompts import PARSE_CHECKIN

from ..llm import get_structured_output_model, parse_with_structured_output
from ..utils import fetch_call_logs, format_timestamp
from .db import (
    get_transcript_for_call_log,
    get_unprocessed_call_logs_sync,
    mark_call_log_processed_sync,
    sync_raw_log_to_db,
    update_call_log_metrics,
)
from .utils import get_patient_name, tag_checkin_with_metadata

logger = get_logger("longevity_clinic.vlogs.agent")


@dataclass
class VlogsAgent:
    """CDC call log processing: fetch → sync → LLM process → update metrics."""

    config: VlogsConfig = field(default_factory=VlogsConfig)
    _structured_llm: BaseChatModel | None = field(default=None, init=False, repr=False)

    @classmethod
    def from_config(cls) -> "VlogsAgent":
        """Create with app defaults."""
        return cls(config=VlogsConfig(output_schema=MetricLogsOutput))

    def __post_init__(self):
        if self.config.extract_with_llm:
            self._structured_llm = get_structured_output_model(
                output_schema=self.config.output_schema or MetricLogsOutput,
                model=self.config.llm_model,
                temperature=self.config.temperature,
            )

    # Primary Parsing API

    @staticmethod
    async def parse_checkin_with_health_data(
        content: str,
        checkin_type: str = "text",
        patient_name: str = "",
        checkin_id: str | None = None,
        timestamp: str | None = None,
    ) -> MetricLogsOutput:
        """Parse content into MetricLogsOutput with health extraction (meds, food, symptoms).
        uses function parse_with_structured_output under the hood.
        """
        # Generate ID and timestamp if not provided
        checkin_id = checkin_id or f"chk_{uuid.uuid4().hex[:8]}"
        timestamp = timestamp or datetime.now().strftime("Today, %I:%M %p")

        # Fallback for empty/short content
        if not content or len(content.strip()) < 10:
            logger.warning(
                "parse_checkin_with_health_data: empty or short content: %s", content
            )
            return VlogsAgent._create_empty_output(
                checkin_id,
                checkin_type,
                content[:500] if content else "",
                timestamp,
                patient_name,
            )

        # Try LLM parsing with full MetricLogsOutput schema
        result = await parse_with_structured_output(
            content=content,
            output_schema=MetricLogsOutput,
            system_prompt=PARSE_CHECKIN,
            max_content_length=4000,
        )

        if result:
            # Tag checkin with provided metadata
            tag_checkin_with_metadata(
                output=result,
                checkin_id=checkin_id,
                checkin_type=checkin_type,
                timestamp=timestamp,
                patient_name=patient_name,
                fallback_summary=content[:500],
            )

            logger.info(
                "Parsed checkin with health data: %d meds, %d foods, %d symptoms",
                len(result.medications_entries),
                len(result.food_entries),
                len(result.symptom_entries),
            )
            return result

        # LLM failed - return empty health data
        logger.warning("parse_checkin_with_health_data LLM returned None")
        return VlogsAgent._create_empty_output(
            checkin_id, checkin_type, content[:500], timestamp, patient_name
        )

    @staticmethod
    def _create_empty_output(
        checkin_id: str,
        checkin_type: str,
        summary: str,
        timestamp: str,
        patient_name: str,
    ) -> MetricLogsOutput:
        """Create empty MetricLogsOutput (fallback)."""
        return MetricLogsOutput(
            checkin=CheckInSummary(
                id=checkin_id,
                type=checkin_type,
                summary=summary,
                timestamp=timestamp,
                sentiment="",
                key_topics=[],
                provider_reviewed=False,
                patient_name=patient_name,
            ),
            medications_entries=[],
            food_entries=[],
            symptom_entries=[],
        )

    # CDC Pipeline

    async def fetch_and_sync_raw(self, phone_number: str | None = None) -> int:
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
        """CDC Steps 3-4: Process unprocessed logs with LLM, mark all as processed."""
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
                # Mark as processed even if no transcript (skip LLM but don't reprocess)
                if not transcript:
                    await asyncio.to_thread(mark_call_log_processed_sync, call_log.id)
                    continue

                output = await self._parse_call_log(
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

    # Internal

    async def _parse_call_log(
        self, transcript: str, call_id: str, call_date: str, patient_phone: str
    ) -> MetricLogsOutput:
        """Parse call transcript using centralized parsing."""
        patient_name = get_patient_name(patient_phone)
        formatted_date = format_timestamp(call_date)
        checkin_id = f"call_{call_id}"

        if not transcript or len(transcript.strip()) < 10:
            return self._create_empty_output(
                checkin_id, "call", "", formatted_date, patient_name
            )

        try:
            # Use centralized parsing function
            result = await self.parse_checkin_with_health_data(
                content=transcript,
                checkin_type="call",
                patient_name=patient_name,
                checkin_id=checkin_id,
                timestamp=formatted_date,
            )
            return result
        except Exception as e:
            logger.error("Parse failed for call %s: %s", call_id, e)
            return self._create_empty_output(
                checkin_id, "call", "", formatted_date, patient_name
            )
