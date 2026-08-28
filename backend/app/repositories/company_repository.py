"""Cypher queries for Company nodes."""
import logging

from neo4j.exceptions import ServiceUnavailable

from app.database import get_session
from app.exceptions import DatabaseUnavailableError, NotFoundError

logger = logging.getLogger(__name__)


class CompanyRepository:
    """All database operations related to Company nodes."""

    def get_all(self) -> list[dict]:
        """Return all companies."""
        query = """
            MATCH (co:Company)
            OPTIONAL MATCH (j:Job)-[:AT_COMPANY]->(co)
            WITH co, count(DISTINCT j) AS job_count
            RETURN co.id AS id, co.name AS name, co.industry AS industry,
                   co.description AS description, co.location AS location,
                   job_count
            ORDER BY co.name
        """
        try:
            with get_session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_by_id(self, company_id: str) -> dict:
        """Return a company with all its jobs and required skills."""
        query = """
            MATCH (co:Company {id: $company_id})
            OPTIONAL MATCH (j:Job)-[:AT_COMPANY]->(co)
            OPTIONAL MATCH (j)-[req:REQUIRES_SKILL]->(s:Skill)
            WITH co, j, collect(DISTINCT s.name) AS skill_names
            WITH co,
                 collect(DISTINCT CASE WHEN j IS NOT NULL THEN {
                     id: j.id, title: j.title,
                     employment_type: j.employment_type,
                     experience_required: j.experience_required,
                     required_skills: skill_names
                 } END) AS jobs
            RETURN co.id AS id, co.name AS name, co.industry AS industry,
                   co.description AS description, co.location AS location,
                   jobs
        """
        try:
            with get_session() as session:
                result = session.run(query, company_id=company_id)
                record = result.single()
                if not record:
                    raise NotFoundError("Company", company_id)
                return dict(record)
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc
