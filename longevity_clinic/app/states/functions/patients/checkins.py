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
    """Use LLM to extract structured check-in data from content."""
    checkin_model = await asyncio.to_thread(
        _structured_llm.invoke,
        [HumanMessage(content=f"Extract check-in data from: {content[:2000]}")],
    )

    checkin_model.id = f"chk_{uuid.uuid4().hex[:8]}"
    checkin_model.type = checkin_type
    checkin_model.timestamp = datetime.now().strftime("Today, %I:%M %p")
    checkin_model.provider_reviewed = False

    return checkin_model
