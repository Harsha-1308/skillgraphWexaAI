"""Business logic for graph exploration."""
from app.repositories.graph_repository import GraphRepository
from app.schemas.graph import GraphData, GraphNode, GraphEdge

_repo = GraphRepository()


def get_candidate_graph(candidate_id: str) -> GraphData:
    """Build graph visualization data for a candidate's skill neighbourhood."""
    raw = _repo.get_candidate_graph(candidate_id)
    if not raw.get("candidate"):
        return GraphData(nodes=[], edges=[])

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    seen_nodes: set[str] = set()

    def add_node(node_id: str, label: str, name: str, props: dict = {}):
        if node_id not in seen_nodes:
            nodes.append(GraphNode(id=node_id, label=label, name=name, properties=props))
            seen_nodes.add(node_id)

    c = raw["candidate"]
    cid = c.get("id", "candidate")
    add_node(cid, "Candidate", c.get("name", "Candidate"))

    for s in raw.get("direct_skills", []):
        if not s:
            continue
        sid = s.get("id", "")
        add_node(sid, "Skill", s.get("name", ""), {"category": s.get("category", "")})
        edges.append(GraphEdge(source=cid, target=sid, type="HAS_SKILL"))

    for s in raw.get("related_skills", []):
        if not s:
            continue
        sid = s.get("id", "")
        add_node(sid, "RelatedSkill", s.get("name", ""), {"category": s.get("category", "")})

    for j in raw.get("jobs", []):
        if not j:
            continue
        jid = j.get("id", "")
        add_node(jid, "Job", j.get("title", ""))

    for co in raw.get("companies", []):
        if not co:
            continue
        coid = co.get("id", "")
        add_node(coid, "Company", co.get("name", ""), {"industry": co.get("industry", "")})

    return GraphData(nodes=nodes, edges=edges)


def get_skill_bridge(candidate_id: str, job_id: str) -> list[dict]:
    """Find skill bridge paths between candidate and job."""
    return _repo.get_skill_bridge(candidate_id, job_id)
