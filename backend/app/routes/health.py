"""Health check endpoint."""
from fastapi import APIRouter
from app.database import check_connectivity

router = APIRouter()


@router.get("/health")
def health_check():
    """Return application and database health status."""
    db_ok = check_connectivity()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
        "application": "SkillGraph API",
        "version": "1.0.0",
    }
