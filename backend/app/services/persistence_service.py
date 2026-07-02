"""Persist incoming WhatsApp messages to the database."""

from sqlalchemy.orm import Session

from app.db_models import Document, Image, Note, Project
from app.models.incoming_message import IncomingMessage
from app.services.downloader import download_media
from app.utils.logger import get_logger
from database import STORAGE_DOCUMENTS, STORAGE_IMAGES

logger = get_logger(__name__)


def save_note(db: Session, project_code: str, message: IncomingMessage) -> Note | None:
    """Save a text message as a Note."""
    project = db.query(Project).filter(Project.code == project_code).first()
    if not project:
        return None

    note = Note(
        project_id=project.id,
        sender=message.sender,
        message=message.body or "",
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    logger.info("Saved note id=%d for project %s", note.id, project_code)
    return note


def save_image(db: Session, project_code: str, message: IncomingMessage) -> Image | None:
    """Download and save an image."""
    project = db.query(Project).filter(Project.code == project_code).first()
    if not project:
        return None

    if not message.media:
        return None

    media_item = message.media[0]
    try:
        filename, file_path = download_media(
            media_item.url, media_item.content_type, STORAGE_IMAGES
        )
    except Exception:
        return None

    image = Image(
        project_id=project.id,
        filename=filename,
        file_path=file_path,
        sender=message.sender,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    logger.info("Saved image id=%d for project %s", image.id, project_code)
    return image


def save_document(db: Session, project_code: str, message: IncomingMessage) -> Document | None:
    """Download and save a document."""
    project = db.query(Project).filter(Project.code == project_code).first()
    if not project:
        return None

    if not message.media:
        return None

    media_item = message.media[0]
    try:
        filename, file_path = download_media(
            media_item.url, media_item.content_type, STORAGE_DOCUMENTS
        )
    except Exception:
        return None

    doc = Document(
        project_id=project.id,
        filename=message.body or filename,
        file_path=file_path,
        sender=message.sender,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    logger.info("Saved document id=%d for project %s", doc.id, project_code)
    return doc
