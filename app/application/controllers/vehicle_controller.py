import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.deps import get_session

from app.application.schemas.vehicle_schema import VehicleRead, VehicleCreate
from app.domain.use_cases.vehicle_use_cases import VehicleUseCases
from app.infrastructure.repositories.vehicle_repository import VehicleRepository

router = APIRouter(prefix="/vehicles", tags=["Vehicle"])

@router.post("/", response_model=VehicleRead, status_code=201)
async def create_user(data: VehicleCreate, session: AsyncSession = Depends(get_session)):
    repo = VehicleRepository(session)
    use_case = VehicleUseCases(repo)
    try:
        vehicle = await use_case.create_vehicle(user_id=data.user_id,data=data)
        return vehicle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/", response_model=list[UserRead])
# async def list_users(session: AsyncSession = Depends(get_session)):
#     repo = UserRepository(session)
#     use_case = UserUseCases(repo)
#     return await use_case.list_users()

# @router.get("/{user_id}", response_model=UserRead)
# async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
#     repo = UserRepository(session)
#     use_case = UserUseCases(repo)
#     user = await use_case.get_by_id(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.delete("/{user_id}", status_code=204)
# async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
#     repo = UserRepository(session)
#     use_case = UserUseCases(repo)
#     deleted = await use_case.delete_user(user_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="User not found")

# @router.put("/{user_id}", response_model=UserUpdate)
# async def update_user(
#     user_id: uuid.UUID,
#     user_data: UserUpdate,
#     session: AsyncSession = Depends(get_session)
# ):
#     use_case = UserUseCases(UserRepository(session))
#     try:
#         return await use_case.update_user(user_id, user_data)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))

