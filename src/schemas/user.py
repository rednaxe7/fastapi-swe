from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[Literal['admin', 'user', 'guest']]
    active: Optional[bool]

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
