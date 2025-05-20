import datetime
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
    created_at: datetime.datetime
    last_updated: datetime.datetime

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

class VehicleUpdate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    identifier: Optional[str] = None
    
