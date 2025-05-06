import uuid
from app.application.schemas.user_schema import UserUpdate
from app.domain.entities.user import User
from app.domain.interfaces.user_repository_interface import IUserRepository

class UserUseCases:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, username: str, email: str, password: str) -> User:
        # Aqui poderia ter validação de negócio, como verificar email duplicado etc.
        new_user = User(id=None, username=username, email=email, password=password)
        created_user = await self.repository.create(new_user)
        return created_user

    async def list_users(self) -> list[User]:
        return await self.repository.list()

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)
    async def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        # Atualiza somente os campos enviados
        updated_user = User(
            id=user.id,
            username=user_data.username or user.username,
            email=user_data.email or user.email,
            password=user_data.password or user.password,
        )

        return await self.repository.update_user(user_id, updated_user)