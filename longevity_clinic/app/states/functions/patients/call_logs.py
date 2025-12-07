"""Call logs processing functions for patients (stateless)."""

import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.state_schemas import (
    CheckInModel,
    CallLogEntry,
    TranscriptSummary,
)

from ..utils import format_timestamp

logger = get_logger("longevity_clinic.call_logs")

# LLM setup
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
_structured_llm = _llm.with_structured_output(CheckInModel)

# Phone to patient name mapping
PHONE_TO_PATIENT_NAME: dict[str, str] = {
    "+12126804645": "Demo Patient (Sarah Chen)",
}


def get_patient_name(phone: str) -> str:
    """Get patient name from phone number."""
    return PHONE_TO_PATIENT_NAME.get(phone, "Unknown Patient")


def _get_best_summary(api_summary: str, full_transcript: str) -> str:
    """Determine the best summary text from API summary or transcript.
    
    Priority:
    1. API summary if present and meaningful (>20 chars, not just AI greeting)
    2. Extract user content from transcript if meaningful
    3. Fallback placeholder for short/incomplete calls
    
    Args:
        api_summary: Summary from API (may be empty)
        full_transcript: Full transcript text
        
    Returns:
        Best summary string to display
    """
    # 1. Use API summary if meaningful
    if api_summary and len(api_summary.strip()) > 20:
        return api_summary.strip()
    
    # 2. Try to extract meaningful content from transcript
    if full_transcript:
        transcript = full_transcript.strip()
        
        # Extract user portions from transcript (look for "User:" lines)
        user_lines = []
        for line in transcript.split('\n'):
            line = line.strip()
            if line.lower().startswith('user:'):
                user_content = line[5:].strip()  # Remove "User:" prefix
                if user_content:
                    user_lines.append(user_content)
        
        # If we have user content, use that
        if user_lines:
            user_summary = ' '.join(user_lines)
            if len(user_summary) > 200:
                return user_summary[:200] + "..."
            return user_summary
        
        # If no user content extracted, check if transcript is meaningful
        # (not just AI greeting)
        if len(transcript) > 100 and not transcript.lower().startswith('ai:'):
            if len(transcript) > 300:
                return transcript[:300] + "..."
            return transcript
        
        # Short transcript - likely incomplete/cutoff call
        if len(transcript) < 100:
            return "Brief call - conversation incomplete"
    
    # 3. Fallback
    return "Voice call check-in"


async def summarize_transcript(
    full_transcript: str,
    call_id: str = "",
    call_date: str = "",
    patient_phone: str = "",
) -> CheckInModel:
    """Use LLM to create structured CheckIn from transcript."""
    try:
        patient_name = get_patient_name(patient_phone)
        formatted_date = format_timestamp(call_date)

        messages = [
            SystemMessage(
                content="You are a medical assistant. Analyze patient call transcripts and extract structured health information."
            ),
            HumanMessage(
                content=f"""Analyze and extract this patient call transcript.\nTranscript:\n{full_transcript[:4000]}"""
            ),
        ]

        result: CheckInModel = await asyncio.to_thread(_structured_llm.invoke, messages)
        result.id = f"call_{call_id}"
        result.type = "call"
        result.timestamp = formatted_date
        result.provider_reviewed = False
        result.patient_name = patient_name

        return result
    except Exception as e:
        logger.error("Error summarizing transcript: %s", e)
        return CheckInModel(
            id=f"call_{call_id}",
            type="call",
            summary="Summary generation failed.",
            timestamp=format_timestamp(call_date),
            sentiment="neutral",
            key_topics=["voice call"],
            provider_reviewed=False,
            patient_name=get_patient_name(patient_phone),
        )


async def process_call_logs(
    call_logs: list[CallLogEntry],
    processed_ids: set[str],
    use_llm_summary: bool = True,
) -> tuple[int, list[dict], dict[str, TranscriptSummary]]:
    """Process call logs and optionally generate AI summaries.

    Returns: (new_logs_count, new_checkins, new_summaries)
    """
    print(
        f"[DEBUG] process_call_logs ENTERED: {len(call_logs)} logs, use_llm={use_llm_summary}",
        flush=True,
    )
    new_logs_count = 0
    new_checkins: list[dict] = []
    new_summaries: dict[str, TranscriptSummary] = {}

    for log in call_logs:
        call_id = log.get("call_id", "")
        if not call_id or call_id in processed_ids:
            continue

        new_logs_count += 1
        full_transcript = log.get("full_transcript", "")
        call_date = log.get("call_date", "")

        # caller_phone can be a dict (nested) or string depending on API response
        raw_phone = log.get("caller_phone", "")
        if isinstance(raw_phone, dict):
            patient_phone = raw_phone.get("phone_number", "")
        else:
            patient_phone = raw_phone

        api_summary = log.get("summary", "") or ""  # Ensure string, not None

        if use_llm_summary:
            checkin_model = await summarize_transcript(
                full_transcript, call_id, call_date, patient_phone
            )
            ai_summary_text = checkin_model.summary
            timestamp_text = checkin_model.timestamp
        else:
            patient_name = get_patient_name(patient_phone)
            timestamp_text = format_timestamp(call_date)
            
            # Determine the best summary to use:
            # 1. Prefer API summary if it exists and is meaningful
            # 2. Fall back to transcript extract if no summary
            # 3. Use placeholder for very short/meaningless calls
            summary_text = _get_best_summary(api_summary, full_transcript)
            ai_summary_text = summary_text

            checkin_model = CheckInModel(
                id=f"call_{call_id}",
                type="call",
                summary=summary_text,
                timestamp=timestamp_text,
                sentiment="neutral",
                key_topics=["voice call"],
                provider_reviewed=False,
                patient_name=patient_name,
            )

        # TypedDict must be created as a dict, not constructor
        new_summaries[call_id] = {
            "call_id": call_id,
            "patient_phone": patient_phone,
            "call_date": call_date,
            "summary": api_summary,
            "ai_summary": ai_summary_text,
            "type": "call",
            "timestamp": timestamp_text,
        }
        new_checkins.append(checkin_model.to_dict())

    return new_logs_count, new_checkins, new_summaries
