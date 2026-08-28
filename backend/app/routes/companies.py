"""Company API endpoints."""
from fastapi import APIRouter, HTTPException
from app.exceptions import DatabaseUnavailableError, NotFoundError
import app.services.company_service as svc

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("")
def list_companies():
    try:
        return svc.list_companies()
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")


@router.get("/{company_id}")
def get_company(company_id: str):
    try:
        return svc.get_company(company_id)
    except NotFoundError as exc:
        raise HTTPException(404, str(exc))
    except DatabaseUnavailableError:
        raise HTTPException(503, "Graph database is currently unavailable.")
