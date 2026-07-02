from datetime import datetime, timezone

from app.models.incoming_message import IncomingMessage, MediaItem

WHATSAPP_PREFIX = "whatsapp:"


def _detect_channel(sender: str) -> str:
    if sender.startswith(WHATSAPP_PREFIX):
        return "whatsapp"
    return "sms"


def _parse_media_count(form_data: dict[str, str]) -> int:
    try:
        return int(form_data.get("NumMedia", "0") or "0")
    except (TypeError, ValueError):
        return 0


def _parse_media(form_data: dict[str, str], media_count: int) -> list[MediaItem]:
    media: list[MediaItem] = []
    for i in range(media_count):
        url = form_data.get(f"MediaUrl{i}", "")
        content_type = form_data.get(f"MediaContentType{i}", "")
        if url:
            media.append(MediaItem(url=url, content_type=content_type))
    return media


def parse_twilio_message(form_data: dict[str, str]) -> IncomingMessage:
    sender = form_data.get("From", "")
    channel = _detect_channel(sender)
    media_count = _parse_media_count(form_data)

    whatsapp_id = form_data.get("WaId")
    if not whatsapp_id and channel == "whatsapp":
        whatsapp_id = sender.removeprefix(WHATSAPP_PREFIX)

    return IncomingMessage(
        message_id=form_data.get("MessageSid", ""),
        sender=sender,
        recipient=form_data.get("To", ""),
        profile_name=form_data.get("ProfileName"),
        whatsapp_id=whatsapp_id,
        channel=channel,
        message_type=form_data.get("MessageType", "text"),
        body=form_data.get("Body"),
        media_count=media_count,
        media=_parse_media(form_data, media_count),
        raw_payload=dict(form_data),
        received_at=datetime.now(timezone.utc),
    )
