import pytest
from fastapi.testclient import TestClient
from src.main import app  # Importa la instancia de FastAPI

# Test client para FastAPI
@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client

# Test para el endpoint raíz
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "fastapi-swe-v1.0.1"}

# Test para verificar que los logs del middleware estén funcionando correctamente
# Aunque no podemos verificar directamente los logs, podemos simular una solicitud y asegurarnos
# de que no cause errores.
def test_log_middleware(client, caplog):
    with caplog.at_level("INFO"):
        client.get("/")
    assert "Request: GET" in caplog.text
    assert "Response: 200" in caplog.text
