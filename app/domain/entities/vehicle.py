from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Vehicle:
    id: uuid.UUID
    user_id: uuid.UUID
    model: str
    brand: str
    identifier: str | None
    created_at: datetime | None
    last_updated: datetime | None
