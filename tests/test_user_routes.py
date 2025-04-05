import pytest
from src.schemas.user import UserCreate, UserResponse
from sqlalchemy.exc import IntegrityError

# Prueba para crear un usuario exitosamente
def test_create_user_success(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "test",
        "last_name": "t9",
        "role": "guest",
        "active": "true"
        }

    # Hacemos la solicitud POST para crear el usuario
    response = client.post("/users/", json=user_data)

    # Verificamos que el código de estado sea 200 (OK)
    assert response.status_code == 200
    # Verificamos que la respuesta contenga los datos del usuario creado
    user_response = response.json()
    assert "username" in user_response
    assert user_response["username"] == user_data["username"]
    assert "email" in user_response
    assert user_response["email"] == user_data["email"]

# Prueba para manejar el error de nombre de usuario duplicado
def test_create_user_duplicate_username(client):
    # Primero, creamos un usuario
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "first_name": "test",
        "last_name": "t9",
        "role": "guest",
        "active": True
    }
    client.post("/users/", json=user_data)

    # Ahora, intentamos crear otro usuario con el mismo nombre de usuario
    response = client.post("/users/", json=user_data)

    # Verificamos que el código de estado sea 400 debido a un error de duplicado
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or email already exists"}

def test_update_user_success(client):
    # Primero, crear un usuario
    create_data = {
        "username": "updateuser",
        "email": "updateuser@example.com",
        "first_name": "update",
        "last_name": "user",
        "role": "user",
        "active": True
    }
    create_response = client.post("/users/", json=create_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    # Luego, actualizar el email y/o password del usuario (NO el username)
    update_data = {
        "email": "updated_email@example.com",
        "last_name": "userx"
    }
    update_response = client.put(f"/users/{user_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["email"] == "updated_email@example.com"


def test_update_user_attempt_username_change(client):
    # Crear usuario
    create_data = {
        "username": "updateuser",
        "email": "updateuser@example.com",
        "first_name": "update",
        "last_name": "user",
        "role": "user",
        "active": True
    }
    create_response = client.post("/users/", json=create_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    # Intentar cambiar el username (esto debe fallar)
    update_data = {
        "username": "newusername",  # esto NO se permite
        "email": "newemail@example.com"
    }
    update_response = client.put(f"/users/{user_id}", json=update_data)
    assert update_response.status_code == 400
    assert update_response.json()["detail"] == "Username cannot be modified"


def test_update_nonexistent_user(client):
    # ID que no existe
    fake_id = 9999
    update_data = {
        "email": "noexist@example.com",
        "password": "irrelevant"
    }
    update_response = client.put(f"/users/{fake_id}", json=update_data)
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "User not found"

# 🧪 Test: Eliminar un usuario existente
def test_delete_user_success(client):
    # Creamos un usuario primero
    user_data = {
        "username": "user_to_delete",
        "email": "delete_me@example.com",
        "first_name": "Delete",
        "last_name": "Me",
        "role": "guest",
        "active": True
    }

    # Crear el usuario
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    user_id = created_user["id"]

    # Eliminar el usuario
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User successfully deleted"}

# 🧪 Test: Intentar eliminar un usuario inexistente
def test_delete_user_not_found(client):
    # Intentamos borrar un ID que no existe
    response = client.delete("/users/9999")  # Asumimos que no existe
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
