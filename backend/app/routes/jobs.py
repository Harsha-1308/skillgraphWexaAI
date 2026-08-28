"""Job API endpoints."""
from fastapi import APIRouter, HTTPException
from app.exceptions import DatabaseUnavailableError, NotFoundError
import app.services.job_service as svc

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def list_jobs():
    try:
        return svc.list_jobs()
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")


@router.get("/{job_id}")
def get_job(job_id: str):
    try:
        return svc.get_job(job_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")
