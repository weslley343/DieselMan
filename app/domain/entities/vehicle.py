from dataclasses import dataclass
import uuid

@dataclass
class Vehicle:
    id: uuid.UUID
    user_id: uuid.UUID
    model: str
    brand: str
    identifier: str | None
    
