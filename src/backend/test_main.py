from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Verifica que el endpoint /api/v1/health responde correctamente."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "NEWSRADAR API"
    assert data["version"] == "1.0.0"


def test_root():
    """Verifica que el endpoint raíz responde."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_get_articles():
    """Verifica que el endpoint de artículos responde."""
    response = client.get("/api/v1/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert "count" in data


def test_get_sources():
    """Verifica que el endpoint de fuentes responde."""
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data


def test_get_topics():
    """Verifica que el endpoint de topics responde."""
    response = client.get("/api/v1/topics")
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data


def test_invalid_endpoint():
    """Verifica que un endpoint inexistente devuelve 404."""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
