import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logger.exception("Unexpected error during user creation")
        raise HTTPException(status_code=500, detail="Unexpected error")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating user with ID: {user_id}")
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

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error during user update: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception(f"Unexpected error updating user {user_id}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        success = user_service.delete_user_service(db, user_id)

        if not success:
            logger.warning(f"User with ID: {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"User with ID: {user_id} deleted successfully")
        return {"message": "User successfully deleted"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error during deletion")

    except Exception as e:
        logger.exception(f"Unexpected error deleting user {user_id}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        user = user_service.get_user_service(db, user_id)

        if not user:
            logger.warning(f"User with ID: {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"User with ID: {user_id} found")
        return user

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception(f"Unexpected error while fetching user {user_id}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all users")
        users = user_service.get_users_service(db)

        if not users:
            logger.warning("No users found")
            raise HTTPException(status_code=404, detail="No users found")

        logger.info(f"{len(users)} users found")
        return users

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        logger.exception("Unexpected error while fetching users")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")