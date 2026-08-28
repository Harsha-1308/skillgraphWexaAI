"""Graph exploration endpoints."""
from fastapi import APIRouter, HTTPException
from app.exceptions import DatabaseUnavailableError
import app.services.graph_service as svc

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/candidates/{candidate_id}")
def get_candidate_graph(candidate_id: str):
    """Return graph visualization data for a candidate's skill neighbourhood."""
    try:
        return svc.get_candidate_graph(candidate_id)
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")


@router.get("/skill-bridge/{candidate_id}/{job_id}")
def get_skill_bridge(candidate_id: str, job_id: str):
    """Graph-native query: find skill bridge paths between candidate and job."""
    try:
        return svc.get_skill_bridge(candidate_id, job_id)
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")
