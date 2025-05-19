from typing import Optional
import uuid
import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime.datetime
    last_updated: datetime.datetime

    # class Config:
    #     from_attributes = True  # permite popular a partir de objetos ORM
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None