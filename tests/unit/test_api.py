import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Fixture para proporcionar un cliente de prueba."""
    from src.backend.main import app
    return TestClient(app)


def test_health_check(client):
    """Test del endpoint de health check."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
