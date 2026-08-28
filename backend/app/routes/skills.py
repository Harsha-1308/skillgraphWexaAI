"""Skill API endpoints."""
from fastapi import APIRouter, HTTPException
from app.exceptions import DatabaseUnavailableError, NotFoundError
import app.services.skill_service as svc

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("")
def list_skills():
    try:
        return svc.list_skills()
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")


@router.get("/demand")
def get_skill_demand():
    try:
        return svc.get_skill_demand()
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")


@router.get("/{skill_id}/related")
def get_related_skills(skill_id: str):
    try:
        return svc.get_skill_with_related(skill_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")
