"""
Test para verificar el endpoint de salud de la API
Sprint 1: Validación básica de la API
"""
import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio src/backend al path  
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src' / 'backend'))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture que proporciona un cliente TestClient para FastAPI."""
    return TestClient(app)


class TestHealthEndpoint:
    """Suite de tests para el endpoint /health"""
    
    def test_health_endpoint_returns_200(self, client):
        """Verificar que el endpoint /health devuelve HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_response_structure(self, client):
        """Verificar que la respuesta tiene la estructura esperada."""
        response = client.get("/health")
        json_response = response.json()
        
        assert "status" in json_response
        assert "service" in json_response
        assert "version" in json_response
    
    def test_health_endpoint_response_values(self, client):
        """Verificar que los valores de la respuesta son correctos."""
        response = client.get("/health")
        json_response = response.json()
        
        assert json_response["status"] == "healthy"
        assert json_response["service"] == "NEWSRADAR API"
        assert json_response["version"] == "1.0.0"
    
    def test_health_endpoint_content_type(self, client):
        """Verificar que el Content-Type es JSON."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_exists(self, client):
        """Verificar que el endpoint raíz existe y responde."""
        response = client.get("/")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response
        assert "version" in json_response


class TestAPIDocumentation:
    """Suite de tests para la documentación de la API"""
    
    def test_swagger_ui_available(self, client):
        """Verificar que Swagger UI está disponible en /docs."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_available(self, client):
        """Verificar que ReDoc está disponible en /redoc."""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema_available(self, client):
        """Verificar que el esquema OpenAPI está disponible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        json_response = response.json()
        assert "info" in json_response
        assert "paths" in json_response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
