// ─────────────────────────────────────────────────────────────────────────────
// QUERY 1: Get a candidate by ID
// ─────────────────────────────────────────────────────────────────────────────
MATCH (c:Candidate {id: $candidate_id})
RETURN c.id AS id, c.name AS name, c.email AS email,
       c.experience_years AS experience_years,
       c.location AS location, c.bio AS bio;

// ─────────────────────────────────────────────────────────────────────────────
// QUERY 2: Get all skills for a candidate
// ─────────────────────────────────────────────────────────────────────────────
MATCH (c:Candidate {id: $candidate_id})-[r:HAS_SKILL]->(s:Skill)
RETURN s.id AS id, s.name AS name, s.category AS category,
       s.level AS level, r.level AS candidate_level, r.years AS years
ORDER BY s.category, s.name;
