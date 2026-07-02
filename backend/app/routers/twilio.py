from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.services.command_service import try_handle_command
from app.services.parser import parse_twilio_message
from app.services.persistence_service import save_document, save_image, save_note
from app.services.reply_service import (
    build_project_aware_reply_text,
    build_reply_text,
    send_reply,
)
from app.services.session_manager import get_active_project
from app.utils.logger import get_logger
from database import get_db

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Twilio POC Running"}


@router.post("/twilio/webhook")
async def twilio_webhook(request: Request, db: Session = Depends(get_db)) -> dict[str, str]:
    form = await request.form()
    form_data = {key: str(value) for key, value in form.items()}

    message = parse_twilio_message(form_data)
    logger.info("Normalized incoming message: %s", message.model_dump(mode="json"))

    if message.channel == "whatsapp":
        command_reply = try_handle_command(message, db)
        if command_reply:
            send_reply(message, command_reply)
        else:
            active_project = get_active_project(message.sender)
            if active_project:
                _persist_message(db, active_project, message)
                reply_text = build_project_aware_reply_text(message, active_project)
            else:
                reply_text = build_reply_text(message)
            if reply_text:
                send_reply(message, reply_text)

    return {"status": "received"}


def _persist_message(db: Session, project_code: str, message):
    """Persist the message to the database based on its type."""
    if message.message_type == "text":
        save_note(db, project_code, message)
    elif message.message_type == "image":
        save_image(db, project_code, message)
    elif message.message_type == "document":
        save_document(db, project_code, message)
