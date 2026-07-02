from datetime import datetime

from pydantic import BaseModel, Field


class MediaItem(BaseModel):
    url: str
    content_type: str


class IncomingMessage(BaseModel):
    message_id: str
    sender: str
    recipient: str
    profile_name: str | None = None
    whatsapp_id: str | None = None
    channel: str
    message_type: str
    body: str | None = None
    media_count: int = 0
    media: list[MediaItem] = Field(default_factory=list)
    raw_payload: dict[str, str]
    received_at: datetime
