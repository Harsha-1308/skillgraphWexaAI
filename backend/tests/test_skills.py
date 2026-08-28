"""Tests for skill API endpoints."""
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_SKILL = {
    "id": "skill-python", "name": "Python",
    "category": "Programming", "level": "advanced"
}


def test_list_skills():
    with patch("app.services.skill_service._repo") as mock_repo:
        mock_repo.get_all.return_value = [SAMPLE_SKILL]
        response = client.get("/api/skills")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "Python"


def test_skill_demand():
    demand_skill = {**SAMPLE_SKILL, "job_count": 10, "company_count": 5}
    with patch("app.services.skill_service._repo") as mock_repo:
        mock_repo.get_demand.return_value = [demand_skill]
        response = client.get("/api/skills/demand")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["job_count"] == 10


def test_related_skills():
    related = {**SAMPLE_SKILL, "id": "skill-fastapi", "name": "FastAPI",
               "strength": 0.9, "hops": 1}
    with patch("app.services.skill_service._repo") as mock_repo:
        mock_repo.get_by_id.return_value = SAMPLE_SKILL
        mock_repo.get_related.return_value = [related]
        response = client.get("/api/skills/skill-python/related")
        assert response.status_code == 200
        data = response.json()
        assert "related" in data
        assert len(data["related"]) == 1
