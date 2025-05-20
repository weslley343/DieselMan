# app/infrastructure/repositories/scene_repository.py

import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.interfaces.vehicle_repository_interface import IVehicleRepository
from app.domain.entities.vehicle import Vehicle
from app.infrastructure.db.models.vehicle_model import VehicleModel
from uuid import UUID
from typing import List

class VehicleRepository(IVehicleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, vehicle: Vehicle) -> Vehicle:
        now = datetime.datetime.now()
        db_vehicle = VehicleModel(  # Use VehicleModel here
            id=vehicle.id,
            user_id=vehicle.user_id,
            model=vehicle.model,
            brand=vehicle.brand,
            identifier=vehicle.identifier,
            created_at=now,
            last_updated=now
        )
        try:
            self.session.add(db_vehicle)
            await self.session.commit()
            await self.session.refresh(db_vehicle)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Error creating vehicle. Please check the data sent.")
        return Vehicle(  # Convert back to the domain entity
            id=db_vehicle.id,
            user_id=db_vehicle.user_id,
            model=db_vehicle.model,
            brand=db_vehicle.brand,
            identifier=db_vehicle.identifier
        )

    async def list(self, user_id: UUID) -> List[Vehicle]:
        result = await self.session.execute(
            select(VehicleModel).where(VehicleModel.user_id == user_id)
        )
        vehicles = result.scalars().all()
        return [
            Vehicle(
                id=v.id,
                user_id=v.user_id,
                model=v.model,
                brand=v.brand,
                identifier=v.identifier,
                created_at=v.created_at,
                last_updated=v.last_updated
            ) for v in vehicles
        ]

    async def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        result = await self.session.execute(
            select(VehicleModel).where(VehicleModel.id == vehicle_id)
        )
        vehicle = result.scalar_one_or_none()
        if vehicle is None:
            return None
        return Vehicle(
            id=vehicle.id,
            user_id=vehicle.user_id,
            name=vehicle.name,
            brand=vehicle.brand,
            identifier=vehicle.identifier
        )

    async def delete(self, vehicle_id: UUID) -> None:
        await self.session.execute(
            delete(VehicleModel).where(VehicleModel.id == vehicle_id)
        )
        await self.session.commit()
