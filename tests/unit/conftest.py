from fastapi.testclient import TestClient
from src.backend.main import app

import pytest

# Este fixture permite crear un cliente reutilizable para los tests. Nos permite probar endpoints de forma controlada.
@pytest.fixture
def client():
    # Con TestClient(app) podemos realizar peticiones a nuestra API sin necesidad de levantar un 
    # servidor real, es decir, no se va a arrancar uvicorn.
    return TestClient(app)