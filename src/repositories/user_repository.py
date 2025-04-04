from sqlalchemy.orm import Session
from src.db.models import User
from src.schemas.user import UserCreate, UserUpdate
from datetime import datetime

def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()