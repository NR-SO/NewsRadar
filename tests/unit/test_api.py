"""
Test 
Sprint 1: Validación básica del API
Se emplea pytest para realizar pruebas unitarias.
"""


# ============================================
# Tests para verificar el endpoint raíz de la API
# ============================================

# Test para verificar que el endpoint root devuelve la información general de la API
def test_root_endpoint_returns_api_info(client):
    # Simulamos una petición HTTP GET a la ruta raíz utilizando el cliente de pruebas
    response = client.get("/")

    # Verificamos que el código de estado HTTP sea 200 OK
    assert response.status_code == 200

    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "version" in data

# Test para verificar que el endpoint root devuelve los valores correctos
def test_root_endpoint_returns_expected_docs_and_version(client):
    # Simulamos la petición
    response = client.get("/")
    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()

    assert data["docs"] == "/docs", f"Se esperaba docs='/docs' y se obtuvo {data['docs']}"
    assert data["version"] == "1.0.0", f"Se esperaba version='1.0.0' y se obtuvo {data['version']}"

# Test para verificar que el endpoint root devuelve un JSON válido
def test_root_endpoint_returns_json(client):
    # Simulamos la petición
    response = client.get("/")
    # Verificamos que el tipo de contenido de la respuesta sea JSON, no usamos igualdad estricta porque 
    # puede incluir charset u otros parámetros
    assert "application/json" in response.headers["content-type"]


# ============================================
# Tests para verificar los endpoints de documentación
# ============================================

# Test para verificar que el endpoint de documentación Swagger UI está disponible
def test_swagger_ui_available(client):
    # Simulamos una petición HTTP GET a la ruta de documentación Swagger UI
    response = client.get("/docs")
    # Verificamos que el código de estado HTTP sea 200 OK, lo que indica que la documentación está disponible
    assert response.status_code == 200

# Test para verificar que el endpoint de documentación ReDoc está disponible
def test_redoc_available(client):
    # Simulamos una petición HTTP GET a la ruta de documentación ReDoc
    response = client.get("/redoc")
    # Verificamos que el código de estado HTTP sea 200 OK, lo que indica que la documentación está disponible
    assert response.status_code == 200


# ============================================
# Tests para verificar el endpoint de documentación OpenAPI JSON
# ============================================

# Test para verificar que el endpoint de documentación OpenAPI JSON está disponible
def test_openapi_schema_available(client):
    # Simulamos una petición HTTP GET a la ruta del esquema OpenAPI JSON
    response = client.get("/openapi.json")

    assert response.status_code == 200
    # Verificamos que el tipo de contenido de la respuesta sea JSON, no usamos igualdad estricta porque
    assert "application/json" in response.headers["content-type"]

    data = response.json()
    assert "info" in data
    assert "paths" in data

# Test para verificar que el esquema OpenAPI JSON contiene la información personalizada definida en la API
def test_openapi_schema_contains_custom_metadata(client):
    # Simulamos una petición HTTP GET a la ruta del esquema OpenAPI JSON
    response = client.get("/openapi.json")
    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()

    assert data["info"]["title"] == "NEWSRADAR API"
    assert data["info"]["version"] == "1.0.0"
    assert data["info"]["description"] == "API REST para procesamiento de canales RSS"

"""
Para futuros tests mas complejos tener en cuenta la caché app.openapi_schema (la primera llamada genera el esquema
la segunda reutiliza app.openapi_schema)
"""

# ============================================
# Tests de placeholders para endpoints de articles, sources y topics
# ============================================

# Test para verificar que el endpoint de articles devuelve una estructura vacía inicialmente
def test_articles_endpoint_structure(client):
    # Simulamos una petición HTTP GET a la ruta de articles
    response = client.get("/api/v1/articles")

    # Verificamos que el código de estado HTTP sea 200 OK, lo que indica que el endpoint está disponible
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()
    assert "articles" in data
    assert "count" in data

    # Actualmente el endpoint devuelve una estructura vacía, por lo que verificamos que 
    # articles sea una lista vacía y count sea 0
    assert data["articles"] == []
    assert data["count"] == 0

# Test para verificar que el endpoint de sources devuelve una estructura vacía inicialmente
def test_sources_endpoint_structure(client):
    # Simulamos una petición HTTP GET a la ruta de sources
    response = client.get("/api/v1/sources")

    # Verificamos que el código de estado HTTP sea 200 OK, lo que indica que el endpoint está disponible
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()
    assert "sources" in data
    assert "count" in data

    # Actualmente el endpoint devuelve una estructura vacía, por lo que verificamos que 
    # sources sea una lista vacía y count sea 0
    assert data["sources"] == []
    assert data["count"] == 0

# Test para verificar que el endpoint de topics devuelve una estructura vacía inicialmente
def test_topics_endpoint_structure(client):
    # Simulamos una petición HTTP GET a la ruta de topics
    response = client.get("/api/v1/topics")

    # Verificamos que el código de estado HTTP sea 200 OK, lo que indica que el endpoint está disponible
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

    # Convertimos la respuesta en formato JSON para verificar su contenido
    data = response.json()
    assert "topics" in data
    assert "count" in data

    # Actualmente el endpoint devuelve una estructura vacía, por lo que verificamos que 
    # topics sea una lista vacía y count sea 0
    assert data["topics"] == []
    assert data["count"] == 0