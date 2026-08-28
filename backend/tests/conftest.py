"""Test configuration and fixtures."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_db_unavailable():
    """Mock a database-unavailable scenario."""
    with patch("app.database.get_session") as mock:
        from neo4j.exceptions import ServiceUnavailable
        mock.side_effect = ServiceUnavailable("Test: DB unavailable")
        yield mock
