from sqlalchemy.orm import Session
from src.db.models import User
from src.schemas.user import UserCreate, UserUpdate
from datetime import datetime

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
