"""Pydantic schemas for Company API responses."""
from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    id: str
    name: str
    industry: str
    description: str
    location: str


class JobInCompany(BaseModel):
    id: str
    title: str
    employment_type: str
    experience_required: int
    required_skills: list[str] = []


class CompanyDetail(CompanyBase):
    jobs: list[JobInCompany] = []
    total_jobs: int = 0
    top_skills: list[str] = []
