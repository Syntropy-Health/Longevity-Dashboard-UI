"""Voice transcription state using OpenAI Whisper."""

import os

# Add the custom component path
import sys
from pathlib import Path
from urllib.request import urlopen

import reflex as rx

custom_component_path = str(
    Path(__file__).parent.parent.parent.parent
    / "reflex-audio-capture"
    / "custom_components"
)
if custom_component_path not in sys.path:
    sys.path.insert(0, custom_component_path)

from reflex_audio_capture import AudioRecorderPolyfill, get_codec, strip_codec_part

# Lazy-initialize OpenAI client to avoid import-time errors when API key is missing
_openai_client = None


def get_openai_client():
    """Get or create the OpenAI client lazily."""
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Voice transcription will not work.")
            return None
        from openai import AsyncOpenAI

        _openai_client = AsyncOpenAI(api_key=api_key)
    return _openai_client


# Unique reference for the audio recorder
AUDIO_REF = "checkin_audio"


class VoiceTranscriptionState(rx.State):
    """State for voice transcription using OpenAI Whisper."""

    # Recording state
    has_error: bool = False
    processing: bool = False
    transcript: str = ""
    error_message: str = ""

    # Audio settings
    timeslice: int = 0  # 0 = send all at once when stopped
    device_id: str = ""
    use_mp3: bool = True

    @rx.event(background=True)
    async def on_data_available(self, chunk: str):
        """Handle incoming audio data and transcribe with Whisper."""
        # Get the codec/mime type from the data URI
        mime_type, _, _codec = get_codec(chunk).partition(";")
        audio_type = mime_type.partition("/")[2]
        if audio_type == "mpeg":
            audio_type = "mp3"

        # Read the audio data from the data URI
        with urlopen(strip_codec_part(chunk)) as audio_data:
            try:
                async with self:
                    self.processing = True
                    self.has_error = False
                    self.error_message = ""

                # Get OpenAI client (lazy initialization)
                client = get_openai_client()
                if client is None:
                    raise Exception(
                        "OpenAI API key not configured. Voice transcription is unavailable."
                    )

                # Transcribe using OpenAI Whisper
                transcription = await client.audio.transcriptions.create(
                    model="whisper-1",
                    file=("temp." + audio_type, audio_data.read(), mime_type),
                )
            except Exception as e:
                async with self:
                    self.has_error = True
                    self.error_message = str(e)
                    self.processing = False
                # Stop recording on error
                yield audio_capture.stop()
                raise
            finally:
                async with self:
                    self.processing = False

            # Update transcript
            async with self:
                # Append to existing transcript (in case of chunked recording)
                if self.transcript:
                    self.transcript = self.transcript + " " + transcription.text
                else:
                    self.transcript = transcription.text

    @rx.event
    def clear_transcript(self):
        """Clear the transcript."""
        self.transcript = ""
        self.has_error = False
        self.error_message = ""

    @rx.event
    def on_error(self, err):
        """Handle recording errors."""
        print(f"Recording error: {err}")
        self.has_error = True
        self.error_message = str(err)

    @rx.event
    def start_recording(self):
        """Start audio recording."""
        self.has_error = False
        self.error_message = ""
        return audio_capture.start()

    @rx.event(background=True)
    async def stop_recording(self):
        """Stop audio recording (background event for non-blocking UI).

        Sets processing=True immediately for instant UI feedback.
        The actual transcription happens in on_data_available (background).
        """
        async with self:
            self.processing = True  # Show processing state immediately
        yield audio_capture.stop()


# Create the audio capture component instance
audio_capture = AudioRecorderPolyfill.create(
    id=AUDIO_REF,
    on_data_available=VoiceTranscriptionState.on_data_available,
    on_error=VoiceTranscriptionState.on_error,
    timeslice=VoiceTranscriptionState.timeslice,
    device_id=VoiceTranscriptionState.device_id,
    use_mp3=VoiceTranscriptionState.use_mp3,
)


def voice_recorder_component() -> rx.Component:
    """Voice recorder component with the audio capture."""
    return audio_capture
