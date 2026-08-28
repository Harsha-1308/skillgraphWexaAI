"""Cypher queries for Candidate nodes and their relationships."""
import logging
from typing import Optional

from neo4j.exceptions import ServiceUnavailable

from app.database import get_session
from app.exceptions import DatabaseUnavailableError, NotFoundError

logger = logging.getLogger(__name__)


class CandidateRepository:
    """All database operations related to Candidate nodes."""

    def get_all(self) -> list[dict]:
        """Return a list of all candidates with basic info."""
        query = """
            MATCH (c:Candidate)
            RETURN c.id AS id, c.name AS name, c.email AS email,
                   c.experience_years AS experience_years,
                   c.location AS location, c.bio AS bio
            ORDER BY c.name
        """
        try:
            with get_session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_by_id(self, candidate_id: str) -> dict:
        """Return a single candidate by ID."""
        query = """
            MATCH (c:Candidate {id: $candidate_id})
            RETURN c.id AS id, c.name AS name, c.email AS email,
                   c.experience_years AS experience_years,
                   c.location AS location, c.bio AS bio
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                record = result.single()
                if not record:
                    raise NotFoundError("Candidate", candidate_id)
                return dict(record)
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_skills(self, candidate_id: str) -> list[dict]:
        """Return all skills for a candidate with proficiency levels."""
        query = """
            MATCH (c:Candidate {id: $candidate_id})-[r:HAS_SKILL]->(s:Skill)
            RETURN s.id AS id, s.name AS name, s.category AS category,
                   s.level AS level, r.level AS candidate_level, r.years AS years
            ORDER BY s.category, s.name
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_matching_jobs(self, candidate_id: str) -> list[dict]:
        """Find jobs where the candidate has at least one required skill.
        
        Returns job match data including match percentage calculated from
        the number of required skills the candidate possesses.
        """
        query = """
            MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(cs:Skill)
            MATCH (j:Job)-[:REQUIRES_SKILL]->(rs:Skill)
            MATCH (j)-[:AT_COMPANY]->(co:Company)
            WITH j, co, c,
                 collect(DISTINCT rs.id) AS required_skill_ids,
                 collect(DISTINCT cs.id) AS candidate_skill_ids
            WITH j, co,
                 required_skill_ids,
                 candidate_skill_ids,
                 [s IN required_skill_ids WHERE s IN candidate_skill_ids] AS matched_ids
            WHERE size(matched_ids) > 0
            MATCH (ms:Skill) WHERE ms.id IN matched_ids
            WITH j, co, required_skill_ids, matched_ids,
                 collect(DISTINCT ms.name) AS matched_skill_names
            RETURN j.id AS job_id, j.title AS title, j.description AS description,
                   j.experience_required AS experience_required, j.location AS location,
                   j.employment_type AS employment_type,
                   j.salary_min AS salary_min, j.salary_max AS salary_max,
                   co.id AS company_id, co.name AS company_name,
                   matched_skill_names AS matched_skills,
                   size(required_skill_ids) AS total_required,
                   size(matched_ids) AS match_count,
                   round(100.0 * size(matched_ids) / size(required_skill_ids)) AS match_percentage
            ORDER BY match_percentage DESC, j.title
            LIMIT 20
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_extended_jobs_via_related_skills(self, candidate_id: str) -> list[dict]:
        """Multi-hop traversal: Candidate → HAS_SKILL → Skill → RELATED_TO → Skill → REQUIRES_SKILL ← Job
        
        This 3-hop graph traversal finds jobs reachable through related skills even when
        the candidate doesn't directly possess every required skill. This is the query
        that demonstrates the power of graph databases over relational databases.
        """
        query = """
            // Step 1: Get candidate's direct skills
            MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(directSkill:Skill)
            
            // Step 2: Traverse RELATED_TO edges up to 2 hops to find adjacent skills
            MATCH (directSkill)-[:RELATED_TO*1..2]->(relatedSkill:Skill)
            WHERE NOT (c)-[:HAS_SKILL]->(relatedSkill)
            
            // Step 3: Find jobs that require these related skills
            MATCH (j:Job)-[:REQUIRES_SKILL]->(relatedSkill)
            MATCH (j)-[:AT_COMPANY]->(co:Company)
            
            // Step 4: Exclude jobs already matched directly
            WITH c, j, co, collect(DISTINCT relatedSkill.name) AS bridgeSkills
            WHERE NOT ANY(ds IN [(c)-[:HAS_SKILL]->(s) | s.id]
                          WHERE (j)-[:REQUIRES_SKILL]->(:Skill {id: ds}))
            
            RETURN j.id AS job_id, j.title AS title, j.description AS description,
                   j.experience_required AS experience_required, j.location AS location,
                   j.employment_type AS employment_type,
                   j.salary_min AS salary_min, j.salary_max AS salary_max,
                   co.id AS company_id, co.name AS company_name,
                   bridgeSkills AS matched_skills,
                   0 AS total_required, 0 AS match_count, 0.0 AS match_percentage
            ORDER BY size(bridgeSkills) DESC
            LIMIT 10
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_skill_gap(self, candidate_id: str, job_id: str) -> dict:
        """Analyse the skill gap between a candidate and a specific job."""
        query = """
            MATCH (j:Job {id: $job_id})-[r:REQUIRES_SKILL]->(s:Skill)
            MATCH (j)-[:AT_COMPANY]->(co:Company)
            OPTIONAL MATCH (c:Candidate {id: $candidate_id})-[ch:HAS_SKILL]->(s)
            WITH j, co, s, r, ch,
                 ch IS NOT NULL AS has_skill
            RETURN j.id AS job_id, j.title AS job_title, co.name AS company_name,
                   s.id AS skill_id, s.name AS skill_name, s.category AS category,
                   r.minimum_level AS minimum_level, r.importance AS importance,
                   has_skill, ch.level AS candidate_level
            ORDER BY r.importance DESC, s.name
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id, job_id=job_id)
                records = [dict(r) for r in result]
                if not records:
                    raise NotFoundError("Job", job_id)
                return {
                    "job_id": records[0]["job_id"],
                    "job_title": records[0]["job_title"],
                    "company_name": records[0]["company_name"],
                    "skills": records,
                }
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_roles(self, candidate_id: str) -> list[dict]:
        """Career path: Candidate → HAS_SKILL → Skill ← REQUIRES_SKILL ← Job → FOR_ROLE → Role."""
        query = """
            MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(s:Skill)
            MATCH (j:Job)-[:REQUIRES_SKILL]->(s)
            MATCH (j)-[:FOR_ROLE]->(r:Role)
            WITH r, collect(DISTINCT s.name) AS connecting_skills,
                 count(DISTINCT j) AS job_count
            RETURN r.id AS role_id, r.name AS role_name,
                   job_count, connecting_skills
            ORDER BY job_count DESC
            LIMIT 10
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc
