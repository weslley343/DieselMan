from abc import ABC, abstractmethod
import uuid
from app.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def list(self) -> list[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def update_user(self, user_id: uuid.UUID, user: User) -> User:
        pass