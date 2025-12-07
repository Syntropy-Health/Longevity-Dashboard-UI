"""Voice transcription functions using OpenAI Whisper.

This module contains pure functions for voice transcription that can be
used by state classes without coupling to Reflex state management.
"""

import os
from typing import Optional, Tuple
from urllib.request import urlopen

from longevity_clinic.app.config import get_logger

logger = get_logger("longevity_clinic.voice")

# Lazy-initialize OpenAI client
_openai_client = None


def get_openai_client():
    """Get or create the OpenAI client lazily.

    Returns:
        AsyncOpenAI client or None if API key not set
    """
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set. Voice transcription unavailable.")
            return None
        from openai import AsyncOpenAI

        _openai_client = AsyncOpenAI(api_key=api_key)
    return _openai_client


def parse_audio_codec(data_uri: str) -> Tuple[str, str, str]:
    """Parse audio codec information from data URI.

    Args:
        data_uri: Base64 data URI with audio data

    Returns:
        Tuple of (mime_type, audio_type, full_codec_string)
    """
    # Import from reflex_audio_capture if available
    try:
        from reflex_audio_capture import get_codec

        codec_str = get_codec(data_uri)
        mime_type, _, codec = codec_str.partition(";")
        audio_type = mime_type.partition("/")[2]
        if audio_type == "mpeg":
            audio_type = "mp3"
        return mime_type, audio_type, codec_str
    except ImportError:
        # Fallback parsing
        if data_uri.startswith("data:"):
            header = data_uri.split(",")[0]
            mime_type = header.replace("data:", "").split(";")[0]
            audio_type = mime_type.split("/")[1] if "/" in mime_type else "mp3"
            if audio_type == "mpeg":
                audio_type = "mp3"
            return mime_type, audio_type, header
        return "audio/mp3", "mp3", ""


def strip_data_uri_codec(data_uri: str) -> str:
    """Strip codec part from data URI for URL opening.

    Args:
        data_uri: Base64 data URI

    Returns:
        Clean data URI suitable for urlopen
    """
    try:
        from reflex_audio_capture import strip_codec_part

        return strip_codec_part(data_uri)
    except ImportError:
        # Fallback: remove codec info between mime and base64
        if ";codecs=" in data_uri:
            parts = data_uri.split(";codecs=")
            if len(parts) == 2:
                before = parts[0]
                after = parts[1].split(";", 1)
                if len(after) > 1:
                    return before + ";" + after[1]
        return data_uri


async def transcribe_audio(
    audio_data_uri: str,
    model: str = "whisper-1",
) -> Tuple[str, Optional[str]]:
    """Transcribe audio data using OpenAI Whisper.

    Args:
        audio_data_uri: Base64 data URI containing audio
        model: Whisper model to use (default: whisper-1)

    Returns:
        Tuple of (transcript_text, error_message)
        If successful, error_message is None
        If failed, transcript_text is empty and error_message contains the error
    """
    logger.info("Starting audio transcription")

    client = get_openai_client()
    if client is None:
        error = "OpenAI API key not configured. Voice transcription unavailable."
        logger.error(error)
        return "", error

    try:
        # Parse audio format
        mime_type, audio_type, _ = parse_audio_codec(audio_data_uri)
        clean_uri = strip_data_uri_codec(audio_data_uri)

        # Read audio data from data URI
        with urlopen(clean_uri) as audio_data:
            audio_bytes = audio_data.read()

        logger.debug("Transcribing %d bytes of %s audio", len(audio_bytes), audio_type)

        # Transcribe using OpenAI Whisper
        transcription = await client.audio.transcriptions.create(
            model=model,
            file=(f"audio.{audio_type}", audio_bytes, mime_type),
        )

        transcript = transcription.text
        logger.info("Transcription complete: %d chars", len(transcript))
        return transcript, None

    except Exception as e:
        error = f"Transcription failed: {e}"
        logger.error(error)
        return "", error


async def transcribe_audio_file(
    file_path: str,
    model: str = "whisper-1",
) -> Tuple[str, Optional[str]]:
    """Transcribe an audio file using OpenAI Whisper.

    Args:
        file_path: Path to audio file
        model: Whisper model to use

    Returns:
        Tuple of (transcript_text, error_message)
    """
    logger.info("Transcribing file: %s", file_path)

    client = get_openai_client()
    if client is None:
        return "", "OpenAI API key not configured"

    try:
        with open(file_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model=model,
                file=audio_file,
            )
        return transcription.text, None
    except Exception as e:
        return "", f"Transcription failed: {e}"


def format_recording_duration(seconds: float) -> str:
    """Format recording duration as MM:SS string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "01:30")
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"
