"""Tests for candidate API endpoints."""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_CANDIDATE = {
    "id": "cand-test", "name": "Test User", "email": "test@example.com",
    "experience_years": 3, "location": "Remote", "bio": "A test candidate."
}


def test_list_candidates_returns_list():
    with patch("app.services.candidate_service._repo") as mock_repo:
        mock_repo.get_all.return_value = [SAMPLE_CANDIDATE]
        response = client.get("/api/candidates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == "cand-test"


def test_get_candidate_by_id():
    with patch("app.services.candidate_service._repo") as mock_repo:
        mock_repo.get_by_id.return_value = SAMPLE_CANDIDATE
        mock_repo.get_skills.return_value = []
        response = client.get("/api/candidates/cand-test")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cand-test"
        assert data["name"] == "Test User"


def test_candidate_not_found():
    from app.exceptions import NotFoundError
    with patch("app.services.candidate_service._repo") as mock_repo:
        mock_repo.get_by_id.side_effect = NotFoundError("Candidate", "nonexistent")
        response = client.get("/api/candidates/nonexistent")
        assert response.status_code == 404


def test_database_unavailable_returns_503():
    from app.exceptions import DatabaseUnavailableError
    with patch("app.services.candidate_service._repo") as mock_repo:
        mock_repo.get_all.side_effect = DatabaseUnavailableError("DB down")
        response = client.get("/api/candidates")
        assert response.status_code == 503
