// ─────────────────────────────────────────────────────────────────────────────
// QUERY 9: Career path / role discovery
// Candidate → HAS_SKILL → Skill ← REQUIRES_SKILL ← Job → FOR_ROLE → Role
// ─────────────────────────────────────────────────────────────────────────────
MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(s:Skill)
MATCH (j:Job)-[:REQUIRES_SKILL]->(s)
MATCH (j)-[:FOR_ROLE]->(r:Role)
WITH r, collect(DISTINCT s.name) AS connecting_skills, count(DISTINCT j) AS job_count
RETURN r.id AS role_id, r.name AS role_name, job_count, connecting_skills
ORDER BY job_count DESC
LIMIT 10;
