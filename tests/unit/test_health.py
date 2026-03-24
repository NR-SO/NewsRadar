"""
Test para verificar el endpoint de health de la API
Sprint 1: Validación básica del API
Se emplea pytest para realizar pruebas unitarias.
"""


# Test para verificar que el endpoint de health de la API responde correctamente
def test_health_endpoint_returns_200(client):
    # Simulamos una petición HTTP GET a la ruta /health utilizando el cliente de pruebas
    response = client.get("/health")
    assert response.status_code == 200


# Test para verificar que el endpoint de health devuelve la estructura de datos esperada
def test_health_endpoint_response_structure(client):
    # Simulamos la petición
    response = client.get("/health")
    # Convertimos la respuesta en un diccionario para verificar su contenido
    data = response.json()

    assert "status" in data
    assert "service" in data
    assert "version" in data


# Test para verificar que el endpoint de health devuelve los valores correctos
def test_health_endpoint_response_values(client):
    # Simulamos la petición
    response = client.get("/health")
    # Convertimos la respuesta en un diccionario para verificar su contenido
    data = response.json()

    assert data["status"] == "healthy", f"Se esperaba status='healthy' y se obtuvo {data['status']}"
    assert data["service"] == "NEWSRADAR API", f"Se esperaba service='NEWSRADAR API' y se obtuvo {data['service']}"
    assert data["version"] == "1.0.0", f"Se esperaba version='1.0.0' y se obtuvo {data['version']}"


# Test para verificar que el endpoint de health devuelve un JSON válido
def test_health_endpoint_returns_json(client):
    # Simulamos la petición
    response = client.get("/health")
    # Verificamos que el tipo de contenido de la respuesta sea JSON, no usamos igualdad estricta porque
    # puede incluir charset u otros parámetros
    assert "application/json" in response.headers["content-type"]


"""
Nota: Estos tests son básicos y se centran en la verificación de la respuesta del endpoint de health.
Si en el futuro el endpoint /health devuelve más información
(p. ej. estado de base de datos, servicios externos o timestamp),
habrá que ampliar este archivo con nuevas comprobaciones.
"""
