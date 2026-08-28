"""Pydantic schemas for Candidate API responses."""
from pydantic import BaseModel
from typing import Optional


class SkillSummary(BaseModel):
    id: str
    name: str
    category: str
    level: str
    candidate_level: Optional[str] = None
    years: Optional[float] = None


class CandidateBase(BaseModel):
    id: str
    name: str
    email: str
    experience_years: int
    location: str
    bio: str


class CandidateDetail(CandidateBase):
    skills: list[SkillSummary] = []
