// ─────────────────────────────────────────────────────────────────────────────
// QUERY 10: Graph-native skill bridge query
//
// Finds the skill bridge between a candidate's existing skills and a job's
// required skills by traversing RELATED_TO edges.
//
// WHY THIS IS GRAPH-NATIVE:
// This query expresses a traversal that connects two sets of nodes
// (candidate skills and job skills) through intermediate relationship hops.
// In a relational database, this would require:
//   - A recursive CTE for the skill graph adjacency
//   - Multiple self-joins with depth limiting
//   - Application-level BFS/DFS logic
// Cypher expresses this naturally as a path query with bounded depth.
// ─────────────────────────────────────────────────────────────────────────────
MATCH (c:Candidate {id: $candidate_id})-[:HAS_SKILL]->(cs:Skill)
MATCH (j:Job {id: $job_id})-[:REQUIRES_SKILL]->(js:Skill)
WITH c, j, collect(DISTINCT cs) AS candidateSkills, collect(DISTINCT js) AS jobSkills
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
LIMIT 20;
