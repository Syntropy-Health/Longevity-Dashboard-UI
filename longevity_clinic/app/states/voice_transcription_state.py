"""Voice transcription state using OpenAI Whisper."""

from urllib.request import urlopen
from pathlib import Path

import reflex as rx
from openai import AsyncOpenAI

# Add the custom component path
import sys
custom_component_path = str(Path(__file__).parent.parent.parent.parent / "reflex-audio-capture" / "custom_components")
if custom_component_path not in sys.path:
    sys.path.insert(0, custom_component_path)

from reflex_audio_capture import AudioRecorderPolyfill, get_codec, strip_codec_part


# Initialize OpenAI client
client = AsyncOpenAI()

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
        mime_type, _, codec = get_codec(chunk).partition(";")
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
    def set_transcript(self, value: str):
        """Set the transcript value."""
        self.transcript = value
    
    @rx.event
    def clear_transcript(self):
        """Clear the transcript."""
        self.transcript = ""
        self.has_error = False
        self.error_message = ""
    
    @rx.event
    def set_timeslice(self, value: list[int | float]):
        """Set the timeslice for audio chunks."""
        self.timeslice = int(value[0])
    
    @rx.event
    def set_device_id(self, value: str):
        """Set the audio input device."""
        self.device_id = value
        yield audio_capture.stop()
    
    @rx.event
    def on_error(self, err):
        """Handle recording errors."""
        print(f"Recording error: {err}")  # noqa: T201
        self.has_error = True
        self.error_message = str(err)
    
    @rx.event
    def start_recording(self):
        """Start audio recording."""
        self.has_error = False
        self.error_message = ""
        return audio_capture.start()
    
    @rx.event
    def stop_recording(self):
        """Stop audio recording."""
        return audio_capture.stop()


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
