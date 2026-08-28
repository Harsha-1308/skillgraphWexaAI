"""Cypher queries for graph exploration and visualization."""
import logging

from neo4j.exceptions import ServiceUnavailable

from app.database import get_session
from app.exceptions import DatabaseUnavailableError

logger = logging.getLogger(__name__)


class GraphRepository:
    """Queries for graph exploration and visualization."""

    def get_candidate_graph(self, candidate_id: str) -> dict:
        """Return the graph neighbourhood of a candidate for visualization.
        
        Returns nodes and edges for:
        - The candidate
        - Their direct skills
        - Related skills (1 hop)
        - Jobs connected to those skills
        - Companies for those jobs
        """
        query = """
            MATCH (c:Candidate {id: $candidate_id})
            OPTIONAL MATCH (c)-[:HAS_SKILL]->(s:Skill)
            OPTIONAL MATCH (s)-[:RELATED_TO]->(rs:Skill)
            OPTIONAL MATCH (j:Job)-[:REQUIRES_SKILL]->(s)
            OPTIONAL MATCH (j)-[:AT_COMPANY]->(co:Company)
            
            WITH c, 
                 collect(DISTINCT s) AS direct_skills,
                 collect(DISTINCT rs) AS related_skills,
                 collect(DISTINCT j) AS jobs,
                 collect(DISTINCT co) AS companies
            
            RETURN c, direct_skills, related_skills, jobs, companies
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id)
                record = result.single()
                if not record:
                    return {"nodes": [], "edges": []}
                return {
                    "candidate": dict(record["c"]),
                    "direct_skills": [dict(s) for s in record["direct_skills"] if s],
                    "related_skills": [dict(s) for s in record["related_skills"] if s],
                    "jobs": [dict(j) for j in record["jobs"] if j],
                    "companies": [dict(co) for co in record["companies"] if co],
                }
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc

    def get_skill_bridge(self, candidate_id: str, job_id: str) -> list[dict]:
        """Graph-native query: Find the skill bridge between a candidate and a job.
        
        This demonstrates graph-database power: find what skills (and related skills)
        form the shortest conceptual path from a candidate's skillset to a job's requirements.
        A relational DB would require complex recursive CTEs or application-level BFS.
        """
        query = """
            // Get candidate skills and job required skills
            MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(cs:Skill)
            MATCH (j:Job {id: $job_id})-[:REQUIRES_SKILL]->(js:Skill)
            
            // Find which candidate skills are directly required
            WITH c, j, collect(DISTINCT cs) AS candidateSkills,
                 collect(DISTINCT js) AS jobSkills
            
            // Find skills that bridge via RELATED_TO (1-2 hops)
            UNWIND candidateSkills AS cs
            OPTIONAL MATCH path = (cs)-[:RELATED_TO*1..2]->(bridge:Skill)
            WHERE bridge IN jobSkills
            
            WITH cs, bridge, path,
                 CASE WHEN path IS NOT NULL THEN length(path) ELSE 999 END AS distance
            WHERE distance < 999
            
            RETURN cs.name AS from_skill, bridge.name AS to_skill,
                   distance AS hops,
                   [n IN nodes(path) | n.name] AS path_names
            ORDER BY distance, cs.name
            LIMIT 20
        """
        try:
            with get_session() as session:
                result = session.run(query, candidate_id=candidate_id, job_id=job_id)
                return [dict(record) for record in result]
        except ServiceUnavailable as exc:
            raise DatabaseUnavailableError("Database is unavailable.") from exc
