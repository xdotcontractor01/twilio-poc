"""SQLAlchemy database configuration and session management."""

import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db_models import Base, Document, Image, Note, Project, TeamMember

DATABASE_URL = "sqlite:///fieldhub.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

STORAGE_BASE = Path(__file__).resolve().parent / "storage"
STORAGE_IMAGES = STORAGE_BASE / "images"
STORAGE_DOCUMENTS = STORAGE_BASE / "documents"

DUMMY_DATA_DIR = Path(__file__).resolve().parent.parent / "dummy_data"


def init_db() -> None:
    """Create tables and seed data if the database is empty."""
    Base.metadata.create_all(bind=engine)

    STORAGE_IMAGES.mkdir(parents=True, exist_ok=True)
    STORAGE_DOCUMENTS.mkdir(parents=True, exist_ok=True)

    with SessionLocal() as db:
        if db.query(Project).count() == 0:
            _seed_data(db)


def _seed_data(db: Session) -> None:
    projects_data = _load_json("projects.json")
    team_data = _load_json("team.json")

    for p in projects_data:
        project = Project(
            code=p["project_code"],
            name=p["project_name"],
            manager=p["project_manager"],
            contractor=p["contractor"],
            status=p["status"],
            completion_percentage=p["completion_percentage"],
        )
        db.add(project)

    db.flush()

    project_id_map = {p.code: p.id for p in db.query(Project).all()}

    for team_entry in team_data:
        project_id = project_id_map.get(team_entry["project_code"])
        if project_id is None:
            continue
        for member in team_entry["members"]:
            db.add(TeamMember(
                project_id=project_id,
                name=member["name"],
                role=member["role"],
            ))

    db.commit()


def _load_json(filename: str) -> list[dict]:
    with open(DUMMY_DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def get_db():
    """FastAPI dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
