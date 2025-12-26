"""
API schema definitions (Pydantic models) for external API interactions.

This module centralizes all Pydantic models used for API request/response
validation and serialization, including call logs API parameters.
"""

from pydantic import BaseModel, Field

# =============================================================================
# Call Logs API Schemas
# =============================================================================


class CallLogsQueryParams(BaseModel):
    """Query parameters for the call logs API.

    Used to construct API requests for fetching call logs from Directus.
    Supports smart filtering by date to fetch only newer calls.
    """

    limit: int | None = Field(
        default=None, ge=1, description="Maximum records to return (None = no limit)"
    )
    offset: int = Field(default=0, ge=0, description="Number of records to skip")
    page: int = Field(default=1, ge=1, description="Page number for pagination")
    sort: str = Field(
        default="-call_date",
        description="Sort field with optional - prefix for descending",
    )
    fields: str = Field(default="*.*", description="Fields to include in response")

    # Filter parameters
    caller_phone: str | None = Field(
        default=None, description="Filter by caller phone number"
    )
    require_transcript: bool = Field(
        default=True, description="Only return records with transcripts"
    )
    since_date: str | None = Field(
        default=None,
        description="ISO date string - only fetch calls after this date (exclusive)",
    )

    def to_api_params(self) -> dict:
        """Convert to API query parameters dictionary."""
        params = {
            "offset": self.offset,
            "page": self.page,
            "sort": self.sort,
            "fields": self.fields,
        }

        # Only add limit if explicitly set (smart fetch = no limit by default)
        if self.limit is not None:
            params["limit"] = self.limit

        if self.caller_phone:
            params["filter[caller_phone][_eq]"] = self.caller_phone

        if self.require_transcript:
            params["filter[full_transcript][_nnull]"] = "true"

        # Smart filter: only fetch calls newer than since_date
        if self.since_date:
            params["filter[call_date][_gt]"] = self.since_date

        return params


class CallLogsAPIConfig(BaseModel):
    """Configuration for the call logs API client.

    Centralizes API configuration including base URL, authentication, and timeouts.
    """

    base_url: str = Field(description="Base URL for the call logs API")
    api_token: str = Field(description="Bearer token for API authentication")
    timeout: float = Field(
        default=30.0, ge=1.0, description="Request timeout in seconds"
    )

    def get_headers(self) -> dict:
        """Get HTTP headers for API requests."""
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }


# =============================================================================
# Transcript Processing Schemas
# =============================================================================


class TranscriptSummarizationRequest(BaseModel):
    """Request parameters for transcript summarization.

    Encapsulates all inputs needed to generate an AI summary from a call transcript.
    """

    full_transcript: str = Field(
        description="The complete transcript text to summarize"
    )
    call_id: str = Field(default="", description="Unique identifier for the call")
    call_date: str = Field(default="", description="ISO timestamp of the call")
    patient_phone: str = Field(
        default="", description="Patient's phone number for name lookup"
    )
    max_transcript_length: int = Field(
        default=4000,
        ge=100,
        description="Maximum transcript length to process (truncated if longer)",
    )


__all__ = [
    "CallLogsAPIConfig",
    "CallLogsQueryParams",
    "TranscriptSummarizationRequest",
]
