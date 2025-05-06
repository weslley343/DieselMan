from dataclasses import dataclass, field
import uuid
from app.domain.entities.scene import Scene
from typing import List

@dataclass
class User:
    id: uuid.UUID
    username: str
    email: str
    password: str
    scenes: List[Scene] = field(default_factory=list)

