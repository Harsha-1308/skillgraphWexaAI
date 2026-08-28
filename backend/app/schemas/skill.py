"""Pydantic schemas for Skill API responses."""
from pydantic import BaseModel
from typing import Optional


class SkillBase(BaseModel):
    id: str
    name: str
    category: str
    level: str


class RelatedSkill(SkillBase):
    strength: float
    hops: int


class SkillDemand(SkillBase):
    job_count: int
    company_count: int


class SkillWithRelated(SkillBase):
    related: list[RelatedSkill] = []
