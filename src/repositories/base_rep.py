from abc import ABC, abstractmethod
from typing import Any, Generic, Never, TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import delete as sqla_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AbstractRepository(ABC):
    """An abstract class implementing the CRUD operations for working with any database."""

    @abstractmethod
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting that entry."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_one_or_none(self, *args: Any, **kwargs: Any) -> Never:
        """Get one entry for the given filter, if it exists."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args: Any, **kwargs: Any) -> Never:
        """Getting all entries according to the specified filter."""
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args: Any, **kwargs: Any) -> Never:
        """Updating a single entry by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *args: Any, **kwargs: Any) -> Never:
        """Deletion of entry by passed ID."""
        raise NotImplementedError


ModelType = TypeVar("ModelType")


class BaseRepository(AbstractRepository, Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def add_one_and_get_obj(self, obj_in: dict) -> ModelType:
        obj = self.model(**obj_in)
        self.session.add(obj)
        return obj

    async def get_by_id_one_or_none(self, obj_id: int | str | UUID) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id),
        )
        instance = result.scalar_one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} entity not found")
        return instance

    async def get_all(self) -> list[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def delete_by_id(self, obj_id: int | str | UUID) -> int:
        stmt = sqla_delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.rowcount

    async def update_one_by_id(self, obj_id: UUID4, obj_data: dict) -> bool:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()

        if not instance:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} entity not found")

        for field, value in obj_data.items():
            setattr(instance, field, value)
        return True