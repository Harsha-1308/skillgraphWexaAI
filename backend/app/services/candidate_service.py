"""Business logic for candidate-related operations."""
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateBase, CandidateDetail, SkillSummary
from app.schemas.job import JobMatch, JobBase, SkillGapAnalysis, SkillGapItem
from app.schemas.graph import RoleDiscovery

_repo = CandidateRepository()


def list_candidates() -> list[CandidateBase]:
    rows = _repo.get_all()
    return [CandidateBase(**r) for r in rows]


def get_candidate(candidate_id: str) -> CandidateDetail:
    row = _repo.get_by_id(candidate_id)
    skills = _repo.get_skills(candidate_id)
    skill_objs = [SkillSummary(**s) for s in skills]
    return CandidateDetail(**row, skills=skill_objs)


def get_candidate_skills(candidate_id: str) -> list[SkillSummary]:
    rows = _repo.get_skills(candidate_id)
    return [SkillSummary(**r) for r in rows]


def get_matching_jobs(candidate_id: str) -> list[JobMatch]:
    rows = _repo.get_matching_jobs(candidate_id)
    results = []
    for r in rows:
        job = JobBase(
            id=r["job_id"], title=r["title"], description=r["description"],
            experience_required=r["experience_required"], location=r["location"],
            employment_type=r["employment_type"],
            salary_min=r.get("salary_min"), salary_max=r.get("salary_max"),
            company_id=r["company_id"], company_name=r["company_name"]
        )
        results.append(JobMatch(
            job=job,
            matched_skills=r["matched_skills"],
            total_required=r["total_required"],
            match_count=r["match_count"],
            match_percentage=float(r["match_percentage"]),
            via_related=False,
        ))
    return results


def get_extended_jobs(candidate_id: str) -> list[JobMatch]:
    """Jobs reachable via related-skill multi-hop traversal."""
    rows = _repo.get_extended_jobs_via_related_skills(candidate_id)
    results = []
    for r in rows:
        job = JobBase(
            id=r["job_id"], title=r["title"], description=r["description"],
            experience_required=r["experience_required"], location=r["location"],
            employment_type=r["employment_type"],
            salary_min=r.get("salary_min"), salary_max=r.get("salary_max"),
            company_id=r["company_id"], company_name=r["company_name"]
        )
        results.append(JobMatch(
            job=job,
            matched_skills=r["matched_skills"],
            total_required=0,
            match_count=0,
            match_percentage=0.0,
            via_related=True,
        ))
    return results


def get_skill_gap_analysis(candidate_id: str, job_id: str) -> SkillGapAnalysis:
    data = _repo.get_skill_gap(candidate_id, job_id)
    skills = data["skills"]
    all_skills = []
    for s in skills:
        item = SkillGapItem(
            skill_id=s["skill_id"],
            skill_name=s["skill_name"],
            category=s["category"],
            minimum_level=s["minimum_level"],
            importance=s["importance"],
            candidate_level=s.get("candidate_level"),
            has_skill=bool(s["has_skill"]),
        )
        all_skills.append(item)

    matched = [s for s in all_skills if s.has_skill]
    missing = [s for s in all_skills if not s.has_skill]
    pct = round(100.0 * len(matched) / len(all_skills)) if all_skills else 0.0

    return SkillGapAnalysis(
        job_id=data["job_id"],
        job_title=data["job_title"],
        company_name=data["company_name"],
        match_percentage=pct,
        required_skills=all_skills,
        missing_skills=missing,
        matched_skills=matched,
    )


def get_roles(candidate_id: str) -> list[RoleDiscovery]:
    rows = _repo.get_roles(candidate_id)
    return [
        RoleDiscovery(
            role_id=r["role_id"],
            role_name=r["role_name"],
            job_count=r["job_count"],
            connecting_skills=r["connecting_skills"],
        )
        for r in rows
    ]
