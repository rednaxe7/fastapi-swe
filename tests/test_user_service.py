import pytest
from unittest.mock import MagicMock
from src.services import user_service
from src.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session

# Test de creación de usuario
def test_create_user_service(mocker):
    # Datos de entrada
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role="user",
        active=True
    )
    
    # Mock de la base de datos y el repositorio
    mock_db = MagicMock(Session)
    mock_create_user = mocker.patch("src.services.user_service.user_repository.create_user", return_value=user_data)

    # Llamada al servicio
    result = user_service.create_user_service(mock_db, user_data)

    # Verificación
    mock_create_user.assert_called_once_with(mock_db, user_data)
    assert result == user_data

# Test de actualización de usuario
def test_update_user_service(mocker):
    # Datos de entrada
    user_data = UserUpdate(
        first_name="Updated",
        last_name="User",
        role="admin",
        active=False
    )
    user_id = 1

    # Mock de la base de datos y el repositorio
    mock_db = MagicMock(Session)
    mock_update_user = mocker.patch("src.services.user_service.user_repository.update_user", return_value=user_data)

    # Llamada al servicio
    result = user_service.update_user_service(mock_db, user_id, user_data)

    # Verificación
    mock_update_user.assert_called_once_with(mock_db, user_id, user_data)
    assert result == user_data

# Test de eliminación de usuario
def test_delete_user_service(mocker):
    user_id = 1

    # Mock de la base de datos y el repositorio
    mock_db = MagicMock(Session)
    mock_delete_user = mocker.patch("src.services.user_service.user_repository.delete_user", return_value=None)

    # Llamada al servicio
    result = user_service.delete_user_service(mock_db, user_id)

    # Verificación
    mock_delete_user.assert_called_once_with(mock_db, user_id)
    assert result is None

# Test de obtención de un usuario por ID
def test_get_user_service(mocker):
    user_id = 1
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role="user",
        active=True
    )
    
    # Mock de la base de datos y el repositorio
    mock_db = MagicMock(Session)
    mock_get_user = mocker.patch("src.services.user_service.user_repository.get_user_by_id", return_value=user_data)

    # Llamada al servicio
    result = user_service.get_user_service(mock_db, user_id)

    # Verificación
    mock_get_user.assert_called_once_with(mock_db, user_id)
    assert result == user_data

# Test de obtención de todos los usuarios
def test_get_users_service(mocker):
    users_data = [
        UserCreate(
            username="testuser1",
            email="test1@example.com",
            first_name="Test",
            last_name="User1",
            role="user",
            active=True
        ),
        UserCreate(
            username="testuser2",
            email="test2@example.com",
            first_name="Test",
            last_name="User2",
            role="admin",
            active=True
        )
    ]
    
    # Mock de la base de datos y el repositorio
    mock_db = MagicMock(Session)
    mock_get_users = mocker.patch("src.services.user_service.user_repository.get_users", return_value=users_data)

    # Llamada al servicio
    result = user_service.get_users_service(mock_db)

    # Verificación
    mock_get_users.assert_called_once_with(mock_db)
    assert result == users_data
