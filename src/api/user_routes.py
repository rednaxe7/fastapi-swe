import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.services import user_service

# Obtener el logger configurado previamente
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating user with username: {user.username}")
        created_user = user_service.create_user_service(db, user)
        logger.info(f"User {user.username} created successfully")
        return created_user

    except IntegrityError:
        logger.warning(f"Username or email already exists: {user.username}")
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating user with ID: {user_id}")

        # Validación para no modificar el `username`
        if user.username:
            logger.warning(f"Attempt to modify username for user with ID: {user_id}")
            raise HTTPException(status_code=400, detail="Username cannot be modified")

        updated_user = user_service.update_user_service(db, user_id, user)
        
        if not updated_user:
            logger.warning(f"User with ID: {user_id} not found for update")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"User with ID: {user_id} updated successfully")
        return updated_user

    except IntegrityError:
        db.rollback()
        logger.warning(f"Conflict updating user {user_id} - likely duplicate email or username")
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting user with ID: {user_id}")
    success = user_service.delete_user_service(db, user_id)

    if not success:
        logger.warning(f"User with ID: {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User with ID: {user_id} deleted successfully")
    return {"message": "User successfully deleted"}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID: {user_id}")
    user = user_service.get_user_service(db, user_id)

    if not user:
        logger.warning(f"User with ID: {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User with ID: {user_id} found")
    return user


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
        logger.info("Fetching all users")
        users = user_service.get_users_service(db)

        if not users:
            logger.warning("No users found")
            raise HTTPException(status_code=404, detail="No users found")

        logger.info(f"{len(users)} users found")
        return users


