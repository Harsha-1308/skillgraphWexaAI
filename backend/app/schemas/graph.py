"""Pydantic schemas for graph exploration API responses."""
from pydantic import BaseModel
from typing import Optional


class GraphNode(BaseModel):
    id: str
    label: str
    name: str
    properties: dict = {}


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str
    properties: dict = {}


class GraphData(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class RoleDiscovery(BaseModel):
    role_id: str
    role_name: str
    job_count: int
    connecting_skills: list[str]
