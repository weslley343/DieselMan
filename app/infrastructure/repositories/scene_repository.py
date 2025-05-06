# app/infrastructure/repositories/scene_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.interfaces.scene_repository_interface import ISceneRepository
from app.domain.entities.scene import Scene
from app.infrastructure.db.models.scene_model import SceneModel
from uuid import UUID
from typing import List

class SceneRepository(ISceneRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, scene: Scene) -> Scene:
        db_scene = SceneModel(
            id=scene.id,
            user_id=scene.user_id,
            title=scene.title,
            content=scene.content,
            url=scene.url
        )
        self.session.add(db_scene)
        await self.session.commit()
        await self.session.refresh(db_scene)
        return Scene(
            id=db_scene.id,
            user_id=db_scene.user_id,
            title=db_scene.title,
            content=db_scene.content,
            url=db_scene.url
        )

    async def list(self, user_id: UUID) -> List[Scene]:
        result = await self.session.execute(
            select(SceneModel).where(SceneModel.user_id == user_id)
        )
        scenes = result.scalars().all()
        return [
            Scene(
                id=s.id,
                user_id=s.user_id,
                title=s.title,
                content=s.content,
                url=s.url
            ) for s in scenes
        ]

    async def get_by_id(self, scene_id: UUID) -> Scene | None:
        result = await self.session.execute(
            select(SceneModel).where(SceneModel.id == scene_id)
        )
        scene = result.scalar_one_or_none()
        if scene is None:
            return None
        return Scene(
            id=scene.id,
            user_id=scene.user_id,
            title=scene.title,
            content=scene.content,
            url=scene.url
        )

    async def delete(self, scene_id: UUID) -> None:
        await self.session.execute(
            delete(SceneModel).where(SceneModel.id == scene_id)
        )
        await self.session.commit()
