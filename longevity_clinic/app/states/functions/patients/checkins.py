"""Check-in processing functions (stateless)."""

import asyncio
import uuid
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from longevity_clinic.app.data.state_schemas import CheckInModel

# LLM setup
_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
_structured_llm = _llm.with_structured_output(CheckInModel)


async def extract_checkin_from_text(
    content: str,
    checkin_type: str = "text",
) -> CheckInModel:
    """Use LLM to extract structured check-in data from content.

    Ensures all required fields are properly set even if LLM returns partial data.
    """
    try:
        checkin_model = await asyncio.to_thread(
            _structured_llm.invoke,
            [HumanMessage(content=f"Extract check-in data from: {content[:2000]}")],
        )
    except Exception:
        # Fallback if LLM fails
        checkin_model = CheckInModel(
            id="",
            type=checkin_type,
            summary=content[:500] if content else "No content provided",
            timestamp="",
            sentiment="neutral",
            key_topics=[],
            provider_reviewed=False,
            patient_name="",
        )

    # Override/ensure required fields are set correctly
    checkin_model.id = f"chk_{uuid.uuid4().hex[:8]}"
    checkin_model.type = checkin_type
    checkin_model.timestamp = datetime.now().strftime("Today, %I:%M %p")
    checkin_model.provider_reviewed = False

    # Ensure optional fields have safe defaults
    if not checkin_model.sentiment:
        checkin_model.sentiment = "neutral"
    if checkin_model.key_topics is None:
        checkin_model.key_topics = []
    if not checkin_model.summary:
        checkin_model.summary = content[:500] if content else "No summary available"
    if checkin_model.patient_name is None:
        checkin_model.patient_name = ""

    return checkin_model
