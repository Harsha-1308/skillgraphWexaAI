// ─────────────────────────────────────────────────────────────────────────────
// QUERY 5: Skill gap analysis
// Shows which required skills the candidate has vs. is missing for a job.
// ─────────────────────────────────────────────────────────────────────────────
MATCH (j:Job {id: $job_id})-[r:REQUIRES_SKILL]->(s:Skill)
MATCH (j)-[:AT_COMPANY]->(co:Company)
OPTIONAL MATCH (c:Candidate {id: $candidate_id})-[ch:HAS_SKILL]->(s)
WITH j, co, s, r, ch,
     ch IS NOT NULL AS has_skill
RETURN j.id AS job_id, j.title AS job_title, co.name AS company_name,
       s.id AS skill_id, s.name AS skill_name, s.category AS category,
       r.minimum_level AS minimum_level, r.importance AS importance,
       has_skill, ch.level AS candidate_level
ORDER BY r.importance DESC, s.name;
