"""In-memory session manager for mapping senders to active projects."""

_sessions: dict[str, str] = {}


def set_active_project(sender: str, project_code: str) -> None:
    """Store the active project code for a sender.

    Args:
        sender: The sender identifier (e.g. ``whatsapp:+919652474668``).
        project_code: The project code to associate with the sender (e.g. ``P102``).
    """
    _sessions[sender] = project_code


def get_active_project(sender: str) -> str | None:
    """Return the active project code for a sender.

    Args:
        sender: The sender identifier to look up.

    Returns:
        The active project code if one exists, otherwise ``None``.
    """
    return _sessions.get(sender)


def clear_active_project(sender: str) -> None:
    """Remove the active project for a sender.

    Args:
        sender: The sender identifier whose session should be cleared.
    """
    _sessions.pop(sender, None)


def has_active_project(sender: str) -> bool:
    """Check whether a sender has an active project.

    Args:
        sender: The sender identifier to check.

    Returns:
        ``True`` if the sender has an active project, otherwise ``False``.
    """
    return sender in _sessions
