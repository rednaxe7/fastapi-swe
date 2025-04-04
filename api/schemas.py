from pydantic import BaseModel, EmailStr
from typing import Literal

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal['admin', 'user', 'guest']
    active: bool = True
    