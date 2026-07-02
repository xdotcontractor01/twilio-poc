"""WhatsApp command handlers for the xDOT prototype."""

from sqlalchemy.orm import Session

from app.db_models import Project, TeamMember
from app.models.incoming_message import IncomingMessage
from app.services.session_manager import clear_active_project, get_active_project, set_active_project

_NO_ACTIVE_PROJECT_REPLY = (
    "❌ No active project.\n\n"
    "Start one using:\n\n"
    "PROJECT <project_code>"
)


def _get_project_by_code(db: Session, code: str) -> Project | None:
    return db.query(Project).filter(Project.code == code).first()


def _handle_help() -> str:
    return (
        "👋 xDOT WhatsApp Assistant\n\n"
        "Available Commands:\n\n"
        "• PROJECT <project_code>\n"
        "  Select a project.\n\n"
        "• STATUS\n"
        "  View current project status.\n\n"
        "• TEAM\n"
        "  View assigned project team.\n\n"
        "• END\n"
        "  Close the current project session.\n\n"
        "After selecting a project, simply send notes, images or documents "
        "and they will automatically be associated with the active project."
    )


def _handle_end(sender: str) -> str:
    clear_active_project(sender)
    return (
        "✅ Project session closed.\n\n"
        "Thank you.\n\n"
        "To start another project:\n\n"
        "PROJECT <project_code>"
    )


def _handle_status(sender: str, db: Session) -> str:
    project_code = get_active_project(sender)
    if not project_code:
        return _NO_ACTIVE_PROJECT_REPLY

    project = _get_project_by_code(db, project_code)
    if project is None:
        return _NO_ACTIVE_PROJECT_REPLY

    from app.db_models import Document, Image, Note

    photos_count = db.query(Image).filter(Image.project_id == project.id).count()
    docs_count = db.query(Document).filter(Document.project_id == project.id).count()
    notes_count = db.query(Note).filter(Note.project_id == project.id).count()

    return (
        "📊 Project Status\n\n"
        f"Project:\n{project.name}\n\n"
        f"Code:\n{project.code}\n\n"
        f"Status:\n{project.status}\n\n"
        f"Completion:\n{project.completion_percentage}%\n\n"
        f"Photos:\n{photos_count}\n\n"
        f"Documents:\n{docs_count}\n\n"
        f"Notes:\n{notes_count}"
    )


def _handle_team(sender: str, db: Session) -> str:
    project_code = get_active_project(sender)
    if not project_code:
        return _NO_ACTIVE_PROJECT_REPLY

    project = _get_project_by_code(db, project_code)
    if project is None:
        return _NO_ACTIVE_PROJECT_REPLY

    members = db.query(TeamMember).filter(TeamMember.project_id == project.id).all()

    lines = [
        "👷 Project Team\n",
        project.name,
        "",
    ]
    for member in members:
        lines.append(member.name)
        lines.append(member.role)
        lines.append("")

    return "\n".join(lines).rstrip()


def _handle_project_selection(message: IncomingMessage, body: str, db: Session) -> str:
    parts = body.split(None, 1)
    if len(parts) == 1 or not parts[1].strip():
        return (
            "Please provide a project code.\n\n"
            "Example:\n\n"
            "PROJECT P102"
        )

    project_code = parts[1].strip().upper()
    project = _get_project_by_code(db, project_code)

    if project is None:
        return (
            "❌ Project not found.\n\n"
            "Please verify the project code."
        )

    set_active_project(message.sender, project_code)
    return (
        "✅ Project Selected\n\n"
        f"Project:\n{project.name}\n\n"
        f"Project Code:\n{project.code}\n\n"
        f"Project Manager:\n{project.manager}\n\n"
        f"Contractor:\n{project.contractor}\n\n"
        f"Status:\n{project.status}\n\n"
        f"Completion:\n{project.completion_percentage}%\n\n"
        "You may now send notes, photos, or documents for this project."
    )


def try_handle_command(message: IncomingMessage, db: Session) -> str | None:
    """Handle a recognized text command, if applicable.

    Args:
        message: The normalized incoming message.
        db: SQLAlchemy database session.

    Returns:
        The reply text if a command was handled, otherwise ``None``.
    """
    if message.message_type != "text":
        return None

    body = (message.body or "").strip()
    command = body.upper()

    if command == "HELP":
        return _handle_help()
    if command == "END":
        return _handle_end(message.sender)
    if command == "STATUS":
        return _handle_status(message.sender, db)
    if command == "TEAM":
        return _handle_team(message.sender, db)

    parts = body.split(None, 1)
    if parts and parts[0].upper() == "PROJECT":
        return _handle_project_selection(message, body, db)

    return None
