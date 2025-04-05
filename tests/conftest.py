import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base, get_db
from fastapi.testclient import TestClient
from src.main import app

# Configuración de la base de datos en memoria para pruebas
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Crea un engine y una sesión para la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos la base de datos en memoria antes de ejecutar las pruebas
@pytest.fixture(scope="session")
def create_test_db():
    # Crear las tablas de la base de datos
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)  # Limpiar la base de datos después de las pruebas

# Fixture para crear una sesión de prueba
@pytest.fixture()
def db(create_test_db):
    db = TestingSessionLocal()
    yield db
    db.close()

# Fixture para el cliente de pruebas de FastAPI
@pytest.fixture()
def client(db):
    # Inyectamos el cliente de prueba con la base de datos en memoria
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client
