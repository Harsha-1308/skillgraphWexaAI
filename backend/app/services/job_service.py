"""Business logic for job-related operations."""
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobBase, JobDetail, RequiredSkill

_repo = JobRepository()


def list_jobs() -> list[JobBase]:
    rows = _repo.get_all()
    return [JobBase(**r) for r in rows]


def get_job(job_id: str) -> JobDetail:
    row = _repo.get_by_id(job_id)
    raw_skills = row.get("required_skills", []) or []
    skills = [
        RequiredSkill(**s) for s in raw_skills
        if s and s.get("id")
    ]
    return JobDetail(
        id=row["id"], title=row["title"], description=row["description"],
        experience_required=row["experience_required"], location=row["location"],
        employment_type=row["employment_type"],
        salary_min=row.get("salary_min"), salary_max=row.get("salary_max"),
        company_id=row["company_id"], company_name=row["company_name"],
        role_name=row.get("role_name"),
        required_skills=skills,
    )
