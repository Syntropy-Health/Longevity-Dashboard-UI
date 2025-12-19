# Call Logs API Documentation

## Overview

The Call Logs API is a Directus-based REST API that provides access to patient call records, including transcripts, summaries, and metadata. This API is used to fetch and process patient voice check-ins from the longevity clinic's phone system.

## Base URL

```
https://directus-staging-ee94.up.railway.app/items/call_logs
```

## Authentication

The API requires Bearer token authentication via the `Authorization` header.

```http
Authorization: Bearer <CALL_API_TOKEN>
```

The token is configured via the `CALL_API_TOKEN` environment variable.

---

## Endpoints

### GET /items/call_logs

Fetch call log records with optional filtering, sorting, and pagination.

#### Request

**Headers:**
| Header | Value | Required |
|--------|-------|----------|
| `accept` | `application/json` | Yes |
| `Authorization` | `Bearer <token>` | Yes |

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `limit` | integer | Maximum number of records to return | `50` |
| `offset` | integer | Number of records to skip | `0` |
| `page` | integer | Page number for pagination | `1` |
| `sort` | string | Field to sort by (prefix with `-` for descending) | `-call_date` |
| `fields` | string | Fields to include in response | `*.*` |
| `meta` | string | Metadata fields to include | `total_count,filter_count` |
| `filter[field][operator]` | string | Filter conditions | See filters below |

**Filter Operators:**
| Operator | Description | Example |
|----------|-------------|---------|
| `_eq` | Equals | `filter[caller_phone][_eq]=+12126804645` |
| `_neq` | Not equals | `filter[status][_neq]=deleted` |
| `_nnull` | Is not null | `filter[full_transcript][_nnull]=true` |
| `_null` | Is null | `filter[summary][_null]=true` |
| `_contains` | Contains substring | `filter[summary][_contains]=medication` |
| `_gt` | Greater than | `filter[duration][_gt]=60` |
| `_gte` | Greater than or equal | `filter[call_date][_gte]=2025-01-01` |
| `_lt` | Less than | `filter[duration][_lt]=300` |
| `_lte` | Less than or equal | `filter[call_date][_lte]=2025-12-31` |

#### Example Request

```bash
curl -X GET \
  'https://directus-staging-ee94.up.railway.app/items/call_logs?limit=50&offset=0&page=1&sort=-call_date&fields=*.*&filter[caller_phone][_eq]=+12126804645&filter[full_transcript][_nnull]=true&meta=total_count,filter_count' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_API_TOKEN'
```

---

## Response Schema

### Success Response (200 OK)

```json
{
  "meta": {
    "total_count": 458,
    "filter_count": 2
  },
  "data": [
    {
      "id": 314,
      "sort": null,
      "date_created": "2025-04-26T00:21:16.359Z",
      "call_date": "2025-04-26T05:51:14",
      "duration": 0,
      "summary": "Sarah spoke with a caller who shared they were feeling sad because their grandmother is sick...",
      "notes": "{\"message\":{\"timestamp\":1745627474012,\"type\":\"assistant-message\",...}}",
      "call_id": "871dd0b7-0d36-45a9-a29d-218f71aa0a28",
      "full_transcript": "AI: Hey. Sarah speaking here. How are you doing? I heard you're a new patient...",
      "caller_phone": "+12126804645"
    }
  ]
}
```

### Response Fields

#### Meta Object

| Field | Type | Description |
|-------|------|-------------|
| `total_count` | integer | Total number of records in the collection |
| `filter_count` | integer | Number of records matching the current filter |

#### Data Array - Call Log Record

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | integer | No | Unique identifier for the call log |
| `sort` | integer | Yes | Sort order (null if not set) |
| `date_created` | string (ISO 8601) | No | Timestamp when record was created |
| `call_date` | string (ISO 8601) | No | Timestamp when the call occurred |
| `duration` | integer | No | Duration of the call in seconds |
| `summary` | string | Yes | Human-readable summary of the call |
| `notes` | string (JSON) | Yes | Additional metadata as JSON string |
| `call_id` | string (UUID) | No | Unique call identifier |
| `full_transcript` | string | Yes | Complete transcript of the call |
| `caller_phone` | string | No | Phone number of the caller (E.164 format) |

#### Expanded caller_phone (when using `fields=*.*`)

When using expanded fields, `caller_phone` may return as an object:

```json
{
  "caller_phone": {
    "phone_number": "+12126804645",
    "user_created": "18166c40-d589-438a-8251-2c84c76949d1",
    "date_created": "2025-04-26T00:21:16.359Z",
    "user_updated": "18166c40-d589-438a-8251-2c84c76949d1",
    "date_updated": "2025-04-26T00:28:40.541Z",
    "first_call_date": "2025-04-26T05:51:14",
    "last_call_date": "2025-04-26T05:58:39",
    "notes": null,
    "customer_name": null,
    "calls": [314, 315]
  }
}
```

---

## TypeScript/Python Types

### TypeScript

```typescript
interface CallLogEntry {
  id: number;
  sort: number | null;
  date_created: string;
  call_date: string;
  duration: number;
  summary: string | null;
  notes: string | null;
  call_id: string;
  full_transcript: string | null;
  caller_phone: string | CallerPhoneExpanded;
}

interface CallerPhoneExpanded {
  phone_number: string;
  user_created: string;
  date_created: string;
  user_updated: string;
  date_updated: string;
  first_call_date: string;
  last_call_date: string;
  notes: string | null;
  customer_name: string | null;
  calls: number[];
}

interface CallLogsResponse {
  meta?: {
    total_count: number;
    filter_count: number;
  };
  data: CallLogEntry[];
}
```

### Python

```python
from typing import TypedDict, Optional, List, Union

class CallLogEntry(TypedDict):
    """Call log entry from the API."""
    id: int
    sort: Optional[int]
    date_created: str
    call_date: str
    duration: int
    summary: Optional[str]
    notes: Optional[str]
    call_id: str
    full_transcript: Optional[str]
    caller_phone: str

class CallerPhoneExpanded(TypedDict):
    """Expanded caller phone information."""
    phone_number: str
    user_created: str
    date_created: str
    user_updated: str
    date_updated: str
    first_call_date: str
    last_call_date: str
    notes: Optional[str]
    customer_name: Optional[str]
    calls: List[int]

class CallLogsMeta(TypedDict):
    """Response metadata."""
    total_count: int
    filter_count: int

class CallLogsResponse(TypedDict):
    """Full API response."""
    meta: Optional[CallLogsMeta]
    data: List[CallLogEntry]
```

---

## Error Responses

### 401 Unauthorized

```json
{
  "errors": [
    {
      "message": "Invalid token",
      "extensions": {
        "code": "INVALID_TOKEN"
      }
    }
  ]
}
```

### 403 Forbidden

```json
{
  "errors": [
    {
      "message": "You don't have permission to access this.",
      "extensions": {
        "code": "FORBIDDEN"
      }
    }
  ]
}
```

### 400 Bad Request

```json
{
  "errors": [
    {
      "message": "Invalid query parameters",
      "extensions": {
        "code": "INVALID_QUERY"
      }
    }
  ]
}
```

---

## Usage Examples

### Fetch Recent Calls with Transcripts

```python
import httpx

async def fetch_calls_with_transcripts(phone_number: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://directus-staging-ee94.up.railway.app/items/call_logs",
            params={
                "limit": 50,
                "sort": "-call_date",
                "fields": "*.*",
                "filter[caller_phone][_eq]": phone_number,
                "filter[full_transcript][_nnull]": "true",
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
```

### Fetch Calls with Metadata

```python
params = {
    "limit": 10,
    "sort": "-call_date",
    "meta": "total_count,filter_count",
    "filter[duration][_gt]": 60,  # Calls longer than 1 minute
}
```

---

## Rate Limits

The API has the following rate limits:
- **Default:** 100 requests per minute per token
- **Burst:** Up to 10 concurrent requests

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CALL_API_TOKEN` | Bearer token for API authentication | Yes |
| `CALL_LOGS_API_BASE` | Base URL for the API (optional override) | No |

---

## Related Files

- `longevity_clinic/app/states/patient_state.py` - State management for call logs
- `longevity_clinic/app/config.py` - API configuration
- `tests/call_logs/test_call_logs_api.py` - API tests
