from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # permite popular a partir de objetos ORM

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None