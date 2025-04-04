from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

# Base con campos opcionales y valor por defecto None
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal['admin', 'user', 'guest']] = None
    active: Optional[bool] = None

# Para creación: requiere todos los campos
class UserCreate(UserBase):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal['admin', 'user', 'guest']
    active: bool = True

# Para actualización: usa los campos opcionales
class UserUpdate(UserBase):
    pass  # Hereda los campos con valor None por defecto
