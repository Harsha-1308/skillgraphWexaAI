"""Candidate API endpoints."""
from fastapi import APIRouter, HTTPException
from app.exceptions import DatabaseUnavailableError, NotFoundError
import app.services.candidate_service as svc

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("")
def list_candidates():
    try:
        return svc.list_candidates()
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):
    try:
        return svc.get_candidate(candidate_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")


@router.get("/{candidate_id}/skills")
def get_candidate_skills(candidate_id: str):
    try:
        return svc.get_candidate_skills(candidate_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")


@router.get("/{candidate_id}/jobs")
def get_matching_jobs(candidate_id: str, include_extended: bool = True):
    """Get matching jobs for a candidate, optionally including multi-hop related skill matches."""
    try:
        direct = svc.get_matching_jobs(candidate_id)
        if include_extended:
            extended = svc.get_extended_jobs(candidate_id)
            # Only include extended jobs not already in direct results
            direct_ids = {m.job.id for m in direct}
            new_extended = [m for m in extended if m.job.id not in direct_ids]
            return {"direct_matches": direct, "extended_matches": new_extended}
        return {"direct_matches": direct, "extended_matches": []}
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")


@router.get("/{candidate_id}/skill-gaps/{job_id}")
def get_skill_gap(candidate_id: str, job_id: str):
    try:
        return svc.get_skill_gap_analysis(candidate_id, job_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")


@router.get("/{candidate_id}/roles")
def get_roles(candidate_id: str):
    try:
        return svc.get_roles(candidate_id)
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable. Please try again later.")
