from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal['admin', 'user', 'guest']
    active: bool = True

# Esquema para actualizar usuarios: todos los campos opcionales
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal['admin', 'user', 'guest']] = None
    active: Optional[bool] = None


#class UserBase(BaseModel):
#    username: Optional[str]
#    email: Optional[EmailStr]
#    first_name: Optional[str]
#    last_name: Optional[str]
#    role: Optional[Literal['admin', 'user', 'guest']]
#    active: Optional[bool]

#class UserCreate(UserBase):
#    username: str
#    email: EmailStr
#    first_name: str
#    last_name: str
#    role: Literal['admin', 'user', 'guest']
#    active: bool = True

#class UserUpdate(UserBase):
#    pass  # Todos los campos opcionales por herencia
