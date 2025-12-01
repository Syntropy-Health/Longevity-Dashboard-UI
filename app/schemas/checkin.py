from pydantic import BaseModel
from app.enums import CheckInType


class CheckIn(BaseModel):
    id: str
    type: CheckInType
    content: str
    timestamp: str
    audio_url: str | None = None
    sentiment_score: float = 0.0