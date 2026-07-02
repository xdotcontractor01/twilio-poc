"""REST API endpoints for accessing project data."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_models import Document, Image, Note, Project, TeamMember
from database import get_db

router = APIRouter(prefix="/api")


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "manager": p.manager,
            "contractor": p.contractor,
            "status": p.status,
            "completion_percentage": p.completion_percentage,
        }
        for p in projects
    ]


@router.get("/projects/{code}")
def get_project(code: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.code == code.upper()).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": project.id,
        "code": project.code,
        "name": project.name,
        "manager": project.manager,
        "contractor": project.contractor,
        "status": project.status,
        "completion_percentage": project.completion_percentage,
    }


@router.get("/projects/{code}/notes")
def get_project_notes(code: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.code == code.upper()).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    notes = (
        db.query(Note)
        .filter(Note.project_id == project.id)
        .order_by(Note.created_at.desc())
        .all()
    )
    return [
        {
            "id": n.id,
            "sender": n.sender,
            "message": n.message,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in notes
    ]


@router.get("/projects/{code}/images")
def get_project_images(code: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.code == code.upper()).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    images = (
        db.query(Image)
        .filter(Image.project_id == project.id)
        .order_by(Image.created_at.desc())
        .all()
    )
    return [
        {
            "id": img.id,
            "filename": img.filename,
            "file_path": img.file_path,
            "sender": img.sender,
            "created_at": img.created_at.isoformat() if img.created_at else None,
        }
        for img in images
    ]


@router.get("/projects/{code}/documents")
def get_project_documents(code: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.code == code.upper()).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    docs = (
        db.query(Document)
        .filter(Document.project_id == project.id)
        .order_by(Document.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_path": d.file_path,
            "sender": d.sender,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


@router.get("/projects/{code}/team")
def get_project_team(code: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.code == code.upper()).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = db.query(TeamMember).filter(TeamMember.project_id == project.id).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "role": m.role,
        }
        for m in members
    ]
