# app/interfaces/controllers/scene_controller.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.domain.interfaces.storage_interface import StorageInterface
from app.domain.use_cases import scene_use_cases
from app.infrastructure.db.deps import get_session
from app.infrastructure.repositories.scene_repository import SceneRepository
from app.domain.use_cases.scene_use_cases import SceneUseCases
from app.application.schemas.scene_schema import SceneCreate, SceneRead

router = APIRouter(prefix="/scenes", tags=["Scenes"])


def get_scene_usecase(session: AsyncSession = Depends(get_session)) -> SceneUseCases:
    repo = SceneRepository(session)
    return SceneUseCases(repo)


@router.post("/", response_model=SceneRead, status_code=status.HTTP_201_CREATED)
async def create_scene(
    scene: SceneCreate,
    user_id: UUID,  # Esse user_id poderia vir de um token no futuro
    usecase: SceneUseCases = Depends(get_scene_usecase)
):
    return await usecase.create_scene(user_id, scene)


@router.get("/", response_model=List[SceneRead])
async def list_scenes(
    user_id: UUID,
    usecase: SceneUseCases = Depends(get_scene_usecase)
):
    return await usecase.list_scenes(user_id)


@router.get("/{scene_id}", response_model=SceneRead)
async def get_scene_by_id(
    scene_id: UUID,
    usecase: SceneUseCases = Depends(get_scene_usecase)
):
    scene = await usecase.get_by_id(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Cena não encontrada")
    return scene


@router.delete("/{scene_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scene(
    scene_id: UUID,
    usecase: SceneUseCases = Depends(get_scene_usecase)
):
    await usecase.delete_scene(scene_id)


