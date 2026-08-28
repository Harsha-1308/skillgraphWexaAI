"""Cypher queries for Job nodes."""
import logging

from neo4j.exceptions import ServiceUnavailable

from app.database import get_session
from app.exceptions import DatabaseUnavailableError, NotFoundError

logger = logging.getLogger(__name__)


class JobRepository:
    """All database operations related to Job nodes."""

    def get_all(self) -> list[dict]:
        """Return all jobs with their company name."""
        query = """
            MATCH (j:Job)-[:AT_COMPANY]->(co:Company)
            RETURN j.id AS id, j.title AS title, j.description AS description,
                   j.experience_required AS experience_required, j.location AS location,
                   j.employment_type AS employment_type,
                   j.salary_min AS salary_min, j.salary_max AS salary_max,
                   co.id AS company_id, co.name AS company_name
            ORDER BY j.title
        """
        try:
            with get_session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_by_id(self, job_id: str) -> dict:
        """Return a single job with all details."""
        query = """
            MATCH (j:Job {id: $job_id})-[:AT_COMPANY]->(co:Company)
            OPTIONAL MATCH (j)-[:FOR_ROLE]->(r:Role)
            OPTIONAL MATCH (j)-[req:REQUIRES_SKILL]->(s:Skill)
            WITH j, co, r,
                 collect({id: s.id, name: s.name, category: s.category,
                          minimum_level: req.minimum_level,
                          importance: req.importance}) AS required_skills
            RETURN j.id AS id, j.title AS title, j.description AS description,
                   j.experience_required AS experience_required, j.location AS location,
                   j.employment_type AS employment_type,
                   j.salary_min AS salary_min, j.salary_max AS salary_max,
                   co.id AS company_id, co.name AS company_name,
                   r.name AS role_name, required_skills
        """
        try:
            with get_session() as session:
                result = session.run(query, job_id=job_id)
                record = result.single()
                if not record:
                    raise NotFoundError("Job", job_id)
                return dict(record)
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc
