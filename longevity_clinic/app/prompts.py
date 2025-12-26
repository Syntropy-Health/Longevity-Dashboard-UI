"""Concise prompts for LLM structured output tasks."""

# Parse check-in transcript to structured health data
PARSE_CHECKIN = """Extract health-related data from this patient check-in transcript.

Rules:
- Only extract what is explicitly mentioned - do not infer or assume
- Leave timestamps as None unless a specific time is clearly stated
- Include all medications, foods, and symptoms mentioned
- Keep the summary concise (2-3 sentences) focusing on key health updates"""
