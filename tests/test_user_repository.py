import pytest
from src.db.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.repositories.user_repository import create_user, update_user, delete_user, get_user_by_id, get_users  # Importamos la función de creación

# Test para la creación de un usuario
def test_create_user(db):
    # Datos de prueba para crear el usuario
    user_data = UserCreate(
        username="testuser2",
        email="testuser2@example.com",
        first_name="Test",
        last_name="User",
        role="guest",
        active=True
    )
    
    # Llamamos a la función para crear el usuario
    created_user = create_user(db, user_data)

    # Verificamos que el usuario haya sido creado
    assert created_user.id is not None  # Verificamos que se haya asignado un ID
    assert created_user.username == "testuser2"
    assert created_user.email == "testuser2@example.com"
    assert created_user.first_name == "Test"
    assert created_user.last_name == "User"
    assert created_user.role == "guest"
    assert created_user.active is True

    # Verificamos que el usuario esté en la base de datos
    user_in_db = db.query(User).filter(User.username == "testuser2").first()
    assert user_in_db is not None  # El usuario debe existir en la base de datos
    assert user_in_db.username == "testuser2"

# Test para actualizar un usuario exitosamente
def test_update_user_success(db):
    # Crear un usuario de prueba
    user_data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "guest",
        "active": True
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Datos de actualización
    update_data = UserUpdate(
        first_name="UpdatedTest",
        last_name="UpdatedUser"
    )

    # Llamamos a la función de actualización
    updated_user = update_user(db, user.id, update_data)

    # Verificamos que el usuario haya sido actualizado correctamente
    assert updated_user is not None
    assert updated_user.first_name == "UpdatedTest"
    assert updated_user.last_name == "UpdatedUser"    

    # Verificamos que los cambios estén reflejados en la base de datos
    user_in_db = db.query(User).filter(User.id == user.id).first()
    assert user_in_db.first_name == "UpdatedTest"
    assert user_in_db.last_name == "UpdatedUser"


# Test cuando el usuario no existe en la base de datos
def test_update_user_not_found(db):
    # Intentamos actualizar un usuario que no existe
    non_existing_user_id = 999  # ID que no existe en la base de datos
    update_data = UserUpdate(
        first_name="NonExistingTest",
        last_name="NonExistingUser"
    )

    # Llamamos a la función de actualización
    updated_user = update_user(db, non_existing_user_id, update_data)

    # Verificamos que no se haya encontrado el usuario y no se haya actualizado nada
    assert updated_user is None

# Test de eliminación de usuario exitoso
def test_delete_user_success(db):
    # Crear un usuario de prueba
    user_data = {
        "username": "testuser4",
        "email": "testuser4@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "guest",
        "active": True
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Verificar que el usuario se haya creado correctamente
    assert db.query(User).filter(User.id == user.id).first() is not None

    # Llamar a la función para eliminar el usuario
    success = delete_user(db, user.id)
    
    # Verificar que la eliminación fue exitosa
    assert success is True
    assert db.query(User).filter(User.id == user.id).first() is None  # Verificar que el usuario fue eliminado

# Test de eliminación de usuario cuando no se encuentra
def test_delete_user_not_found(db):
    # Intentar eliminar un usuario que no existe
    success = delete_user(db, 99999)  # ID no válido
    assert success is False  # La función debería devolver False cuando no se encuentra el usuario

# Test para obtener un usuario por su ID
def test_get_user_by_id(db):
    # Crear un usuario de prueba
    user_data = {
        "username": "testuser5",
        "email": "testuser5@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "guest",
        "active": True
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Llamar a la función get_user_by_id
    retrieved_user = get_user_by_id(db, user.id)

    # Verificar que el usuario obtenido es el mismo que el creado
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.username == user.username
    assert retrieved_user.email == user.email

# Test para obtener todos los usuarios
def test_get_users(db):
    # Crear algunos usuarios de prueba
    user_data1 = {
        "username": "testuser6",
        "email": "testuser6@example.com",
        "first_name": "Test1",
        "last_name": "User1",
        "role": "guest",
        "active": True
    }
    user_data2 = {
        "username": "testuser7",
        "email": "testuser7@example.com",
        "first_name": "Test2",
        "last_name": "User2",
        "role": "guest",
        "active": True
    }

    user1 = User(**user_data1)
    user2 = User(**user_data2)
    
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    # Llamar a la función get_users
    users = get_users(db)

    # Verificar que se obtienen ambos usuarios
    assert len(users) > 0  # Al menos un usuario debe existir
    assert any(user.id == user1.id for user in users)
    assert any(user.id == user2.id for user in users)