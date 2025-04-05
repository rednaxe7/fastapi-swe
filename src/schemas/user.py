from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class UserBase(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Minimum 3 characters")
    email: Optional[EmailStr] = Field(None, description="Must be a valid email")
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[Literal['admin', 'user', 'guest']] = Field(None, description="Must be 'admin', 'user' or 'guest'")
    active: Optional[bool] = Field(None)

class UserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Required and valid email")
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    role: Literal['admin', 'user', 'guest'] = Field(...)
    active: bool = Field(default=True)

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
