"""VlogsAgent - Modular call logs processing agent.

Handles fetching and processing call logs with configurable LLM parsing.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.prompts import PARSE_CHECKIN
from longevity_clinic.app.data.process_schema import CallLogsOutput, CheckInSummary
from longevity_clinic.app.data.state_schemas import CallLogEntry, TranscriptSummary

from .utils import fetch_call_logs, format_timestamp

logger = get_logger("longevity_clinic.vlogs_agent")

# Phone to patient name mapping
PHONE_TO_PATIENT_NAME: dict[str, str] = {
    "+12126804645": "Demo Patient (Sarah Chen)",
}


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


@dataclass
class VlogsConfig:
    """Configuration for VlogsAgent."""

    parse_with_llm: bool = False
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.3
    limit: int = 50


@dataclass
class VlogsAgent:
    """Agent for processing voice call logs into structured data.

    Usage:
        agent = VlogsAgent(config=VlogsConfig(parse_with_llm=True))
        result = await agent.process_logs(phone_number="+1234567890")
    """

    config: VlogsConfig = field(default_factory=VlogsConfig)
    _llm: Optional[ChatOpenAI] = field(default=None, init=False)
    _structured_llm: Optional[object] = field(default=None, init=False)

    def __post_init__(self):
        if self.config.parse_with_llm:
            self._llm = ChatOpenAI(
                model=self.config.llm_model, temperature=self.config.temperature
            )
            self._structured_llm = self._llm.with_structured_output(CallLogsOutput)

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
