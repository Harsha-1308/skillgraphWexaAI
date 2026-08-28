"""Cypher queries for Skill nodes."""
import logging

from neo4j.exceptions import ServiceUnavailable

from app.database import get_session
from app.exceptions import DatabaseUnavailableError, NotFoundError

logger = logging.getLogger(__name__)


class SkillRepository:
    """All database operations related to Skill nodes."""

    def get_all(self) -> list[dict]:
        """Return all skills ordered by category and name."""
        query = """
            MATCH (s:Skill)
            RETURN s.id AS id, s.name AS name, s.category AS category, s.level AS level
            ORDER BY s.category, s.name
        """
        try:
            with get_session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_by_id(self, skill_id: str) -> dict:
        """Return a single skill."""
        query = """
            MATCH (s:Skill {id: $skill_id})
            RETURN s.id AS id, s.name AS name, s.category AS category, s.level AS level
        """
        try:
            with get_session() as session:
                result = session.run(query, skill_id=skill_id)
                record = result.single()
                if not record:
                    raise NotFoundError("Skill", skill_id)
                return dict(record)
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_related(self, skill_id: str, max_hops: int = 3) -> list[dict]:
        """Find related skills via RELATED_TO traversal up to max_hops hops.
        
        Uses bounded variable-length path to avoid runaway queries.
        Returns skills with the minimum path strength (weakest link) and hop count.
        """
        query = """
            MATCH path = (s:Skill {id: $skill_id})-[:RELATED_TO*1..3]->(related:Skill)
            WHERE related.id <> $skill_id
            WITH related, length(path) AS hops,
                 reduce(minStr = 1.0, r IN relationships(path) | 
                        CASE WHEN r.strength < minStr THEN r.strength ELSE minStr END) AS min_strength
            RETURN DISTINCT related.id AS id, related.name AS name,
                   related.category AS category, related.level AS level,
                   min_strength AS strength, min(hops) AS hops
            ORDER BY hops ASC, min_strength DESC
            LIMIT 20
        """
        try:
            with get_session() as session:
                result = session.run(query, skill_id=skill_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_demand(self) -> list[dict]:
        """Return skills ranked by demand across jobs and companies."""
        query = """
            MATCH (j:Job)-[:REQUIRES_SKILL]->(s:Skill)
            MATCH (j)-[:AT_COMPANY]->(co:Company)
            WITH s, count(DISTINCT j) AS job_count, count(DISTINCT co) AS company_count
            RETURN s.id AS id, s.name AS name, s.category AS category, s.level AS level,
                   job_count, company_count
            ORDER BY job_count DESC, company_count DESC
            LIMIT 30
        """
        try:
            with get_session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc
