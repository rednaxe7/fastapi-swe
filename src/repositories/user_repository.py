from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from src.db.models import User
from src.schemas.user import UserCreate, UserUpdate
from datetime import datetime
from typing import List, Dict

COLUMN_INDEXES = {
    1: User.id, 
    2: User.username,
    3: User.email, 
    4: User.created_at, 
    # Agrega más columnas si es necesario
}

# Crear Usuario
def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Actualizar Usuario
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return user

# Eliminar Usuario
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False  # Si no se encuentra el usuario
    db.delete(user)
    db.commit()
    return True  # Usuario eliminado con éxito

# Obtener Usuario por id
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Obtener todos los usuarios
def get_users(db: Session) -> list[User]:
    return db.query(User).all()



# Obtener usuarios con paginación, ordenamiento y totales
def get_users_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    order_by_index: int = 1,  # Usamos un índice
    descending: bool = False,
    filtro_buscar: str = None
) -> Dict:
    skip = (page - 1) * page_size

    # Filtrado
    query = db.query(User)
    if filtro_buscar and filtro_buscar.strip():
        # Filtrar por username o email
        query = query.filter(
            (User.username.ilike(f"%{filtro_buscar}%")) | 
            (User.email.ilike(f"%{filtro_buscar}%"))
        )

    # Ordenamiento  
    # Obtener la columna basada en el índice
    if order_by_index not in COLUMN_INDEXES:
        raise ValueError("Invalid column index.")
    
    order_column = COLUMN_INDEXES[order_by_index]
    order_clause = desc(order_column) if descending else asc(order_column)
    
    # Obtener los usuarios
    users = query.order_by(order_clause).offset(skip).limit(page_size).all()

    # Obtener el total de registros
    total_count = query.count()

    # Calcular el número total de páginas
    total_pages = (total_count + page_size - 1) // page_size  # Redondeo hacia arriba

    return {
        "total_count": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "users": users
    }
