"""Demo data access service for xDOT prototype data."""

import json
from pathlib import Path

_DUMMY_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "dummy_data"


def _load_json(filename: str) -> list[dict]:
    with open(_DUMMY_DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def _index_by_project_code(records: list[dict]) -> dict[str, dict]:
    return {record["project_code"]: record for record in records}


_PROJECTS: dict[str, dict] = _index_by_project_code(_load_json("projects.json"))
_PROJECT_STATUS: dict[str, dict] = _index_by_project_code(_load_json("project_status.json"))
_PROJECT_TEAMS: dict[str, dict] = _index_by_project_code(_load_json("team.json"))
_PROJECT_ACTIVITIES: dict[str, dict] = _index_by_project_code(_load_json("activities.json"))


def get_project(project_code: str) -> dict | None:
    """Return project details for a given project code.

    Args:
        project_code: The project identifier (e.g. ``P102``).

    Returns:
        A dictionary with project fields, or ``None`` if not found.
    """
    return _PROJECTS.get(project_code)


def get_project_status(project_code: str) -> dict | None:
    """Return upload and activity status for a given project code.

    Args:
        project_code: The project identifier (e.g. ``P102``).

    Returns:
        A dictionary with status fields, or ``None`` if not found.
    """
    return _PROJECT_STATUS.get(project_code)


def get_project_team(project_code: str) -> dict | None:
    """Return team members assigned to a given project code.

    Args:
        project_code: The project identifier (e.g. ``P102``).

    Returns:
        A dictionary containing ``project_code`` and ``members``, or ``None`` if not found.
    """
    return _PROJECT_TEAMS.get(project_code)


def get_project_activities(project_code: str) -> list[dict] | None:
    """Return recent activity records for a given project code.

    Args:
        project_code: The project identifier (e.g. ``P102``).

    Returns:
        A list of activity dictionaries, or ``None`` if the project is not found.
    """
    record = _PROJECT_ACTIVITIES.get(project_code)
    if record is None:
        return None
    return record["activities"]
