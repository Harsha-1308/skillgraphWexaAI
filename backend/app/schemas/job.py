"""Pydantic schemas for Job API responses."""
from pydantic import BaseModel
from typing import Optional


class RequiredSkill(BaseModel):
    id: str
    name: str
    category: str
    minimum_level: str
    importance: str


class JobBase(BaseModel):
    id: str
    title: str
    description: str
    experience_required: int
    location: str
    employment_type: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_id: str
    company_name: str


class JobDetail(JobBase):
    required_skills: list[RequiredSkill] = []
    role_name: Optional[str] = None


class JobMatch(BaseModel):
    job: JobBase
    matched_skills: list[str]
    total_required: int
    match_count: int
    match_percentage: float
    via_related: bool = False  # True if matched via related skill traversal


class SkillGapItem(BaseModel):
    skill_id: str
    skill_name: str
    category: str
    minimum_level: str
    importance: str
    candidate_level: Optional[str] = None  # None = candidate doesn't have this skill
    has_skill: bool


class SkillGapAnalysis(BaseModel):
    job_id: str
    job_title: str
    company_name: str
    match_percentage: float
    required_skills: list[SkillGapItem]
    missing_skills: list[SkillGapItem]
    matched_skills: list[SkillGapItem]
