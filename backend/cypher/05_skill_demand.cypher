// ─────────────────────────────────────────────────────────────────────────────
// QUERY 8: Skill demand across jobs and companies
// ─────────────────────────────────────────────────────────────────────────────
MATCH (j:Job)-[:REQUIRES_SKILL]->(s:Skill)
MATCH (j)-[:AT_COMPANY]->(co:Company)
WITH s, count(DISTINCT j) AS job_count, count(DISTINCT co) AS company_count
RETURN s.id AS id, s.name AS name, s.category AS category,
       job_count, company_count
ORDER BY job_count DESC, company_count DESC
LIMIT 30;
