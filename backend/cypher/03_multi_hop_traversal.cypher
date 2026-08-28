// ─────────────────────────────────────────────────────────────────────────────
// QUERY 4: Multi-hop job discovery (3-hop graph traversal)
//
// Path: Candidate → HAS_SKILL → Skill → RELATED_TO* → Skill → ← REQUIRES_SKILL ← Job
//
// This finds jobs reachable through related skills even when the candidate
// does not directly possess every required skill.
//
// WHY THIS IS HARD IN SQL:
// A relational DB would need:
//   1. CTE to get candidate skills
//   2. Self-join on skills table for related skills (1 or more hops)
//   3. Join to job_skills table
//   4. Deduplication logic
// With arbitrary depth, this requires recursive CTEs — awkward and expensive.
// In Cypher, [:RELATED_TO*1..2] expresses this naturally.
// ─────────────────────────────────────────────────────────────────────────────
MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(directSkill:Skill)
MATCH (directSkill)-[:RELATED_TO*1..2]->(relatedSkill:Skill)
WHERE NOT (c)-[:HAS_SKILL]->(relatedSkill)
MATCH (j:Job)-[:REQUIRES_SKILL]->(relatedSkill)
MATCH (j)-[:AT_COMPANY]->(co:Company)
WITH j, co, collect(DISTINCT relatedSkill.name) AS bridgeSkills
RETURN j.id AS job_id, j.title AS title,
       co.name AS company_name,
       bridgeSkills AS bridge_skills
ORDER BY size(bridgeSkills) DESC
LIMIT 10;
