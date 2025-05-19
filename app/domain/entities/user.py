from dataclasses import dataclass, field
import uuid
from datetime import datetime
from app.domain.entities.vehicle import Vehicle
from typing import List

@dataclass
class User:
    id: uuid.UUID
    username: str
    email: str
    password: str
    created_at: datetime | None
    last_updated: datetime | None
    vehicles: List[Vehicle] = field(default_factory=list)

