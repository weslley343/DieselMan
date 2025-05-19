from fastapi import Form
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

class VehicleCreate(BaseModel):
    model: str
    brand: str
    identifier: str
    user_id: uuid.UUID

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        brand: str = Form(...),
        identifier: str = Form(...),
        creator: uuid.UUID = Form(...)
    ):
        return cls(name=name, brand=brand, identifier=identifier, creator=creator)

class VehicleRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    model: str
    brand: str
    identifier: str

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

class VehicleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    
