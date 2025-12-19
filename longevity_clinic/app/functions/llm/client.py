"""LLM client initialization and structured output helpers."""

import os
from typing import Any, Optional, Type, TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel

from longevity_clinic.app.config import get_logger

logger = get_logger("longevity_clinic.llm")

T = TypeVar("T", bound=BaseModel)

# Default model settings
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.2


def _check_api_key() -> bool:
    """Check if OpenAI API key is available."""
    return bool(os.getenv("OPENAI_API_KEY"))


def get_chat_model(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Optional["BaseChatModel"]:
    """Get a ChatOpenAI instance with specified settings.

    Args:
        model: OpenAI model name (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.2)

    Returns:
        Configured ChatOpenAI instance, or None if API key not set
    """
    if not _check_api_key():
        logger.warning("OPENAI_API_KEY not set, LLM features unavailable")
        return None

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=model, temperature=temperature)


def get_structured_output_model(
    output_schema: Type[T],
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Optional[BaseChatModel]:
    """Get a chat model configured for structured output.

    Args:
        output_schema: Pydantic model class for structured output
        model: OpenAI model name
        temperature: Sampling temperature

    Returns:
        Chat model with structured output binding, or None if API key not set
    """
    llm = get_chat_model(model=model, temperature=temperature)
    if llm is None:
        return None
    return llm.with_structured_output(output_schema)


async def parse_with_structured_output(
    content: str,
    output_schema: Type[T],
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_content_length: int = 4000,
) -> Optional[T]:
    """Parse content using LLM with structured output.

    Args:
        content: Text content to parse
        output_schema: Pydantic model for structured extraction
        system_prompt: System prompt for the LLM
        model: OpenAI model name
        temperature: Sampling temperature
        max_content_length: Max characters to send to LLM

    Returns:
        Parsed output or None if parsing fails or API key not set
    """
    if not content or len(content.strip()) < 10:
        return None

    structured_llm = get_structured_output_model(
        output_schema=output_schema,
        model=model,
        temperature=temperature,
    )
    if structured_llm is None:
        return None

    try:
        messages: list[BaseMessage] = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=content[:max_content_length]),
        ]
        result: T = await structured_llm.ainvoke(messages)
        return result
    except Exception as e:
        logger.warning("Structured output parsing failed: %s", e)
        return None
