from dataclasses import dataclass
import uuid

@dataclass
class Scene:
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    url: str
    
