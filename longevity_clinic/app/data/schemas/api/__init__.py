"""
API schema definitions (Pydantic models) for external API interactions.

Contains request/response models for:
- Call logs API
- Transcript processing

Usage:
    from longevity_clinic.app.data.schemas.api import CallLogsAPIConfig, CallLogsQueryParams
"""

from .schemas import (
    CallLogsAPIConfig,
    CallLogsQueryParams,
    TranscriptSummarizationRequest,
)

__all__ = [
    "CallLogsAPIConfig",
    "CallLogsQueryParams",
    "TranscriptSummarizationRequest",
]
