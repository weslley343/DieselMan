from abc import ABC, abstractmethod
import uuid
from app.domain.entities.scene import Scene

class ISceneRepository(ABC):

    @abstractmethod
    async def create(self, scene: Scene) -> Scene:
        pass

    @abstractmethod
    async def list(self) -> list[Scene]:
        pass

    @abstractmethod
    async def get_by_id(self, scene_id: int) -> Scene | None:
        pass

    @abstractmethod
    async def delete(self, scene_id: int) -> bool:
        pass
