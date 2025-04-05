import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.database import Base, get_db
from src.db import models  # 👈 Importante para registrar los modelos

# Base de datos de pruebas (en archivo local, también puedes usar ":memory:" si quieres)
TEST_DATABASE_URL = "sqlite:///./test.db"

# Crear engine y sesión para test
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Crear las tablas al iniciar
Base.metadata.create_all(bind=engine)

# Dependency override para FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Reemplazar la dependencia en la app
app.dependency_overrides[get_db] = override_get_db

# Cliente de pruebas
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para acceder a la base de datos directamente
@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
