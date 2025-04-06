from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserUpdate
from src.repositories import user_repository

def create_user_service(db: Session, user_data: UserCreate):
    return user_repository.create_user(db, user_data)

def update_user_service(db: Session, user_id: int, user_data: UserUpdate):
    return user_repository.update_user(db, user_id, user_data)

def delete_user_service(db: Session, user_id: int):
    return user_repository.delete_user(db, user_id)

def get_user_service(db: Session, user_id: int):
    return user_repository.get_user_by_id(db, user_id)

def get_users_service(db: Session):
    return user_repository.get_users(db)


