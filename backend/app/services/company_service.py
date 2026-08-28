"""Business logic for company-related operations."""
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyBase, CompanyDetail, JobInCompany

_repo = CompanyRepository()


def list_companies() -> list[CompanyBase]:
    rows = _repo.get_all()
    return [
        CompanyBase(
            id=r["id"], name=r["name"], industry=r["industry"],
            description=r["description"], location=r["location"]
        )
        for r in rows
    ]


def get_company(company_id: str) -> CompanyDetail:
    row = _repo.get_by_id(company_id)
    raw_jobs = row.get("jobs", []) or []
    jobs = []
    seen_jobs = set()
    all_skill_names = []
    for j in raw_jobs:
        if not j or j.get("id") in seen_jobs:
            continue
        seen_jobs.add(j.get("id"))
        jobj = JobInCompany(
            id=j["id"], title=j["title"],
            employment_type=j.get("employment_type", ""),
            experience_required=j.get("experience_required", 0),
            required_skills=j.get("required_skills", []) or [],
        )
        jobs.append(jobj)
        all_skill_names.extend(jobj.required_skills)

    # Top skills across all jobs
    from collections import Counter
    top_skills = [s for s, _ in Counter(all_skill_names).most_common(8)]

    return CompanyDetail(
        id=row["id"], name=row["name"], industry=row["industry"],
        description=row["description"], location=row["location"],
        jobs=jobs, total_jobs=len(jobs), top_skills=top_skills,
    )
