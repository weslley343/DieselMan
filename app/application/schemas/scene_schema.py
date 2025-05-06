from fastapi import Form
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr

class SceneCreate(BaseModel):
    title: str
    content: str
    url: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        url: str = Form(...)
    ):
        return cls(title=title, content=content, url=url)

class SceneRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    url: str

    class Config:
        from_attributes = True

class SceneUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    
