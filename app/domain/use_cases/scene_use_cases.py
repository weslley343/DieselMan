# app/application/services/scene/scene_use_cases.py

import uuid
from typing import List
from app.domain.entities.scene import Scene
from app.domain.interfaces.scene_repository_interface import ISceneRepository
from app.application.schemas.scene_schema import SceneCreate, SceneUpdate
from app.domain.interfaces.storage_interface import StorageInterface  # opcional se for usar um update depois

class SceneUseCases:
    def __init__(self, repository: ISceneRepository):
        self.repository = repository

    async def create_scene(self, user_id: uuid.UUID, data: SceneCreate) -> Scene:
        scene = Scene(
            id=uuid.uuid4(),
            user_id=user_id,
            title=data.title,
            content=data.content,
            url=data.url
        )
        return await self.repository.create(scene)

    async def list_scenes(self, user_id: uuid.UUID) -> List[Scene]:
        return await self.repository.list(user_id)

    async def get_by_id(self, scene_id: uuid.UUID) -> Scene | None:
        return await self.repository.get_by_id(scene_id)

    async def delete_scene(self, scene_id: uuid.UUID) -> None:
        await self.repository.delete(scene_id)

    # opcional, se quiser futuramente
    async def update_scene(self, scene_id: uuid.UUID, data: SceneUpdate) -> Scene:
        scene = await self.repository.get_by_id(scene_id)
        if not scene:
            raise ValueError("Cena não encontrada")

        updated = Scene(
            id=scene.id,
            user_id=scene.user_id,
            title=data.title or scene.title,
            content=data.content or scene.content,
            url=data.url or scene.url
        )
        return await self.repository.create(updated)  # aqui você pode ter um método update separado também



