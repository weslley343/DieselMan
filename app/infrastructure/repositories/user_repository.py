import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.entities.user import User
from app.domain.interfaces.user_repository_interface import IUserRepository
from app.infrastructure.db.models.user_model import UserModel

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        db_user = UserModel(username=user.username, email=user.email, password=user.password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return User(id=db_user.id, username=db_user.username, email=db_user.email, password=db_user.password)

    async def list(self) -> list[User]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [User(id=u.id, username=u.username, email=u.email, password=u.password) for u in users]

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return User(id=user.id, username=user.username, email=user.email, password=user.password)
        return None

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.session.commit()
        return result.rowcount > 0

    async def update_user(self, user_id: uuid.UUID, user: User) -> User:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        user_model = result.scalar_one_or_none()
        if not user_model:
            raise ValueError("Usuário não encontrado")

        user_model.username = user.username
        user_model.email = user.email
        user_model.password = user.password

        await self.session.commit()
        await self.session.refresh(user_model)

        return User(id=user_model.id, username=user_model.username, email=user_model.email, password=user_model.password)