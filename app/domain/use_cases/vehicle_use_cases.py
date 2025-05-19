import uuid
from typing import List
from app.domain.entities.vehicle import Vehicle
from app.domain.interfaces.vehicle_repository_interface import IVehicleRepository
from app.application.schemas.vehicle_schema import VehicleCreate, VehicleUpdate

class VehicleUseCases:
    def __init__(self, repository: IVehicleRepository):
        self.repository = repository

    async def create_vehicle(self, user_id: uuid.UUID, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(
            id=uuid.uuid4(),
            user_id=user_id,
            model=data.model,
            brand=data.brand,
            identifier=data.identifier
        )
        return await self.repository.create(vehicle)

    # async def list_scenes(self, user_id: uuid.UUID) -> List[Vehicle]:
    #     return await self.repository.list(user_id)

    # async def get_by_id(self, scene_id: uuid.UUID) -> Vehicle | None:
    #     return await self.repository.get_by_id(scene_id)

    # async def delete_scene(self, scene_id: uuid.UUID) -> None:
    #     await self.repository.delete(scene_id)

    # # opcional, se quiser futuramente
    # async def update_scene(self, scene_id: uuid.UUID, data: VehicleUpdate) -> Vehicle:
    #     scene = await self.repository.get_by_id(scene_id)
    #     if not scene:
    #         raise ValueError("Cena não encontrada")

    #     updated = Vehicle(
    #         id=scene.id,
    #         user_id=scene.user_id,
    #         name=data.title or scene.name,
    #         brand=data.content or scene.brand,
    #         identifier=data.url or scene.identifier
    #     )
    #     return await self.repository.create(updated)  # aqui você pode ter um método update separado também



