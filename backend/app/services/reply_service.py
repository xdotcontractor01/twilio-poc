from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app import config
from app.models.incoming_message import IncomingMessage
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _display_name(incoming_message: IncomingMessage) -> str:
    return incoming_message.profile_name or "there"


def build_project_aware_reply_text(
    incoming_message: IncomingMessage,
    project_code: str,
) -> str | None:
    if incoming_message.message_type == "text":
        return (
            "📝 Note saved.\n\n"
            "Active Project:\n"
            f"{project_code}"
        )

    if incoming_message.message_type == "image":
        return (
            "📷 Image saved.\n\n"
            "Active Project:\n"
            f"{project_code}"
        )

    if incoming_message.message_type == "document":
        return (
            "📄 Document saved.\n\n"
            f"Filename:\n{incoming_message.body or ''}\n\n"
            "Active Project:\n"
            f"{project_code}"
        )

    return None


def build_reply_text(incoming_message: IncomingMessage) -> str | None:
    name = _display_name(incoming_message)

    if incoming_message.message_type == "text":
        return (
            f"👋 Hi {name}!\n\n"
            "Your text message was received successfully."
        )

    if incoming_message.message_type == "image":
        return (
            f"📷 Hi {name}!\n\n"
            "Your image was received successfully.\n\n"
            f"Media Count: {incoming_message.media_count}"
        )

    if incoming_message.message_type == "document":
        return (
            f"📄 Hi {name}!\n\n"
            "Your document was received successfully.\n\n"
            f"Filename:\n{incoming_message.body or ''}"
        )

    return None


def send_reply(incoming_message: IncomingMessage, reply_text: str) -> bool:
    try:
        client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
        message = client.messages.create(
            from_=config.TWILIO_WHATSAPP_NUMBER,
            to=incoming_message.sender,
            body=reply_text,
        )
        logger.info(
            "Reply sent successfully: sid=%s status=%s to=%s",
            message.sid,
            message.status,
            incoming_message.sender,
        )
        return True
    except TwilioRestException as exc:
        logger.error(
            "Failed to send reply to %s: [%s] %s",
            incoming_message.sender,
            exc.code,
            exc.msg,
        )
        return False
