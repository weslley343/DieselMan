from abc import ABC, abstractmethod
import uuid
from app.domain.entities.vehicle import Vehicle

class IVehicleRepository(ABC):

    @abstractmethod
    async def create(self, scene: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    async def list(self) -> list[Vehicle]:
        pass

    @abstractmethod
    async def get_by_id(self, scene_id: uuid) -> Vehicle | None:
        pass

    @abstractmethod
    async def delete(self, scene_id: uuid) -> bool:
        pass
