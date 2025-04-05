from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal['admin', 'user', 'guest']] = None
    active: Optional[bool] = None

class UserCreate(UserBase):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal['admin', 'user', 'guest']
    active: bool = True

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
