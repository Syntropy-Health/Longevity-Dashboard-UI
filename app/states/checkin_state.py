import reflex as rx
from app.schemas.checkin import CheckIn
from app.enums import CheckInType
import datetime
import uuid


class CheckInState(rx.State):
    checkins: list[CheckIn] = [
        CheckIn(
            id="chk1",
            type=CheckInType.VOICE,
            content="Feeling much better today after the new protocol. Sleep was solid.",
            timestamp="Today, 9:00 AM",
            sentiment_score=0.8,
        ),
        CheckIn(
            id="chk2",
            type=CheckInType.TEXT,
            content="Noticed some mild nausea after taking supplements.",
            timestamp="Yesterday, 8:30 PM",
            sentiment_score=-0.2,
        ),
    ]
    is_voice_recording: bool = False
    new_note_content: str = ""

    @rx.event
    def toggle_voice_recording(self):
        self.is_voice_recording = not self.is_voice_recording
        if self.is_voice_recording:
            return rx.toast("Listening... (Simulated)")
        else:
            self.checkins.insert(
                0,
                CheckIn(
                    id=str(uuid.uuid4())[:8],
                    type=CheckInType.VOICE,
                    content="(Voice Transcript) I'm feeling energetic today.",
                    timestamp="Just now",
                    sentiment_score=0.9,
                ),
            )
            return rx.toast("Voice log saved.")

    @rx.event
    def set_new_note_content(self, content: str):
        self.new_note_content = content

    @rx.event
    def save_text_note(self):
        if not self.new_note_content.strip():
            return rx.toast("Note cannot be empty.")
        self.checkins.insert(
            0,
            CheckIn(
                id=str(uuid.uuid4())[:8],
                type=CheckInType.TEXT,
                content=self.new_note_content,
                timestamp="Just now",
                sentiment_score=0.5,
            ),
        )
        self.new_note_content = ""
        return rx.toast("Text log saved.")