"""SkillGraph FastAPI application entry point."""
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import close_driver
from app.routes import health, candidates, jobs, skills, companies, graph

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Graph-based Job & Skill Discovery Platform backed by CognoDB.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware — reads allowed origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api")
app.include_router(candidates.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(skills.router, prefix="/api")
app.include_router(companies.router, prefix="/api")
app.include_router(graph.router, prefix="/api")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all handler that prevents stack traces leaking to the client."""
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


@app.on_event("shutdown")
def shutdown_event():
    """Close the database driver gracefully on application shutdown."""
    close_driver()
    logger.info("Application shutdown complete.")


@app.get("/")
def root():
    return {"message": "SkillGraph API — graph-powered job matching", "docs": "/api/docs"}
