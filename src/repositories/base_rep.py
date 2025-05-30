from typing import Generic, TypeVar, Type, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete as sqla_delete

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id, session: AsyncSession) -> Optional[ModelType]:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list(self, session: AsyncSession) -> List[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj_in: dict, session: AsyncSession) -> ModelType:
        obj = self.model(**obj_in)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, id, session: AsyncSession) -> int:
        stmt = sqla_delete(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount
