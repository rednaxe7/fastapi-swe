import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.services import user_service

# Obtener el logger configurado previamente
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user with username: {user.username}")
    created_user = user_service.create_user_service(db, user)
    logger.info(f"User {user.username} created successfully")
    return created_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating user with ID: {user_id}")
    updated_user = user_service.update_user_service(db, user_id, user)
    if not updated_user:
        logger.warning(f"User with ID: {user_id} not found for update")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User with ID: {user_id} updated successfully")
    return updated_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID: {user_id}")
    user = user_service.get_user_service(db, user_id)
    if not user:
        logger.warning(f"User with ID: {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User with ID: {user_id} found")
    return user