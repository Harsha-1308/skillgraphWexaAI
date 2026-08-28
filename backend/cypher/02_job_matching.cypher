// ─────────────────────────────────────────────────────────────────────────────
// QUERY 3: Direct job matching with match percentage
// Finds jobs where the candidate has at least one required skill.
// Calculates match_percentage = matched_skills / total_required * 100
// ─────────────────────────────────────────────────────────────────────────────
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
RETURN j.id AS job_id, j.title AS title,
       co.id AS company_id, co.name AS company_name,
       matched_skill_names AS matched_skills,
       size(required_skill_ids) AS total_required,
       size(matched_ids) AS match_count,
       round(100.0 * size(matched_ids) / size(required_skill_ids)) AS match_percentage
ORDER BY match_percentage DESC, j.title
LIMIT 20;
