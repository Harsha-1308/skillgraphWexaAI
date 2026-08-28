"""Business logic for skill-related operations."""
from app.repositories.skill_repository import SkillRepository
from app.schemas.skill import SkillBase, SkillDemand, SkillWithRelated, RelatedSkill

_repo = SkillRepository()


def list_skills() -> list[SkillBase]:
    rows = _repo.get_all()
    return [SkillBase(**r) for r in rows]


def get_skill_with_related(skill_id: str) -> SkillWithRelated:
    base = _repo.get_by_id(skill_id)
    related_rows = _repo.get_related(skill_id)
    related = [RelatedSkill(**r) for r in related_rows]
    return SkillWithRelated(**base, related=related)


def get_skill_demand() -> list[SkillDemand]:
    rows = _repo.get_demand()
    return [SkillDemand(**r) for r in rows]
