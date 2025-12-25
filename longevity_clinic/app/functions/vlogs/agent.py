"""VlogsAgent - Call log processing with CDC pattern."""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from langchain_core.language_models import BaseChatModel

from longevity_clinic.app.config import VlogsConfig, get_logger
from longevity_clinic.app.data.schemas.db import CallLog
from longevity_clinic.app.data.schemas.llm import CheckInSummary, MetricLogsOutput
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

    # ==========================================================================
    # Primary Parsing API
    # ==========================================================================

    @staticmethod
    async def parse_checkin_with_health_data(
        content: str,
        checkin_type: str = "text",
        patient_name: str = "",
        checkin_id: str | None = None,
        timestamp: str | None = None,
    ) -> MetricLogsOutput:
        """Parse content into MetricLogsOutput with health extraction."""
        checkin_id = checkin_id or f"chk_{uuid.uuid4().hex[:8]}"
        timestamp = timestamp or datetime.now().strftime("Today, %I:%M %p")

        if not content or len(content.strip()) < 10:
            return VlogsAgent._create_empty_output(
                checkin_id,
                checkin_type,
                content[:500] if content else "",
                timestamp,
                patient_name,
            )

        result = await parse_with_structured_output(
            content=content,
            output_schema=MetricLogsOutput,
            system_prompt=PARSE_CHECKIN,
            max_content_length=4000,
        )

        if result:
            tag_checkin_with_metadata(
                result, checkin_id, checkin_type, timestamp, patient_name, content[:500]
            )
            logger.info(
                "Parsed: %d meds, %d foods, %d symptoms",
                len(result.medications_entries),
                len(result.food_entries),
                len(result.symptom_entries),
            )
            return result

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

    # ==========================================================================
    # CDC Pipeline
    # ==========================================================================

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
        """CDC Steps 3-4: Process unprocessed logs with parallel LLM calls."""
        if not self.config.extract_with_llm:
            return 0

        unprocessed = await asyncio.to_thread(get_unprocessed_call_logs_sync)
        if not unprocessed:
            return 0

        logger.info(
            "Processing %d unprocessed call logs (max_parallel=%d)",
            len(unprocessed),
            self.config.max_parallel,
        )

        # Parallel processing with semaphore limit
        sem = asyncio.Semaphore(self.config.max_parallel)
        results = await asyncio.gather(
            *[self._process_single_log(log, sem) for log in unprocessed],
            return_exceptions=True,
        )
        return sum(1 for r in results if r is True)

    async def _process_single_log(
        self, call_log: CallLog, sem: asyncio.Semaphore
    ) -> bool:
        """Process single call log with semaphore-limited concurrency."""
        async with sem:
            try:
                transcript = await asyncio.to_thread(
                    get_transcript_for_call_log, call_log.id
                )
                if not transcript:
                    await asyncio.to_thread(mark_call_log_processed_sync, call_log.id)
                    return False

                output = await self._parse_call_log(
                    transcript,
                    call_log.call_id,
                    call_log.started_at.isoformat(),
                    call_log.phone_number,
                )
                return await asyncio.to_thread(
                    update_call_log_metrics, call_log.id, output, self.config.llm_model
                )
            except Exception as e:
                logger.error("Failed to process call %s: %s", call_log.call_id, e)
                return False

    async def _parse_call_log(
        self, transcript: str, call_id: str, call_date: str, patient_phone: str
    ) -> MetricLogsOutput:
        """Parse call transcript using centralized parsing."""
        patient_name, formatted_date = (
            get_patient_name(patient_phone),
            format_timestamp(call_date),
        )
        checkin_id = f"call_{call_id}"

        if not transcript or len(transcript.strip()) < 10:
            return self._create_empty_output(
                checkin_id, "call", "", formatted_date, patient_name
            )

        try:
            return await self.parse_checkin_with_health_data(
                content=transcript,
                checkin_type="call",
                patient_name=patient_name,
                checkin_id=checkin_id,
                timestamp=formatted_date,
            )
        except Exception as e:
            logger.error("Parse failed for call %s: %s", call_id, e)
            return self._create_empty_output(
                checkin_id, "call", "", formatted_date, patient_name
            )
