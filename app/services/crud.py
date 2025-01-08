from typing import Generic, TypeVar
from repositories.base_repository import BaseRepository

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def create(self, data: dict) -> T:
        return await self.repository.create(data)

    async def get(self, id: int) -> T | None:
        return await self.repository.get(id)

    async def list(self, offset: int = 0, limit: int = 10):
        return await self.repository.list(offset, limit)

    async def update(self, id: int, data: dict):
        return await self.repository.update(id, data)

    async def delete(self, id: int):
        return await self.repository.delete(id)
