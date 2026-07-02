"""Download media files from Twilio URLs."""

import uuid
from pathlib import Path

import requests

from app import config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def download_media(media_url: str, content_type: str, storage_dir: Path) -> tuple[str, str]:
    """Download a media file from Twilio and save to storage.

    Args:
        media_url: The Twilio media URL.
        content_type: MIME type of the media (e.g. image/jpeg).
        storage_dir: Directory to save the file in.

    Returns:
        Tuple of (filename, file_path) where file_path is the absolute path.
    """
    ext = _extension_from_content_type(content_type)
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = storage_dir / filename

    try:
        response = requests.get(
            media_url,
            auth=(config.ACCOUNT_SID, config.AUTH_TOKEN),
            timeout=30,
        )
        response.raise_for_status()

        file_path.write_bytes(response.content)
        logger.info("Downloaded media: %s (%d bytes)", filename, len(response.content))
        return filename, str(file_path)

    except requests.RequestException as exc:
        logger.error("Failed to download media from %s: %s", media_url, exc)
        raise


def _extension_from_content_type(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "application/pdf": ".pdf",
        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "video/mp4": ".mp4",
        "audio/ogg": ".ogg",
        "audio/mpeg": ".mp3",
    }
    return mapping.get(content_type, ".bin")
