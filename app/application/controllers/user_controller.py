import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.deps import get_session

from app.application.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.domain.use_cases.user_use_cases import UserUseCases
from app.infrastructure.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    use_case = UserUseCases(repo)
    try:
        user = await use_case.create_user(
            username=data.username,
            email=data.email,
            password=data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserRead])
async def list_users(session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    use_case = UserUseCases(repo)
    return await use_case.list_users()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    use_case = UserUseCases(repo)
    user = await use_case.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    use_case = UserUseCases(repo)
    deleted = await use_case.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    use_case = UserUseCases(UserRepository(session))
    try:
        return await use_case.update_user(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

