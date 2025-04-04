from fastapi.testclient import TestClient
from unittest.mock import patch  # Para mockear clases y métodos
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "fastapi-swe-v0.1.0"}  # Actualización a la versión correcta

# Test para el endpoint /health/db
@patch("api.database.Database")  # Mockeamos la clase Database
def test_health_check_db_success(mock_database):
    # Simulamos que el método execute_query no lanza excepciones
    mock_instance = mock_database.return_value
    mock_instance.__enter__.return_value = mock_instance  # Soporte para "with"
    mock_instance.execute_query.return_value = True

    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "connected"}

@patch("api.database.Database")  # Mockeamos la clase Database
def test_health_check_db_failure(mock_database):
    # Simulamos que el método execute_query lanza una excepción
    mock_instance = mock_database.return_value
    mock_instance.__enter__.return_value = mock_instance  # Soporte para "with"
    mock_instance.execute_query.side_effect = Exception("Mocked connection error")

    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "error", "db": "not connected"}
