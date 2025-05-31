from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session_maker
from src.repositories.tasks_rep import TaskRepository
from src.repositories.users_rep import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.task = TaskRepository(self._session)
        self.user = UserRepository(self._session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()

    async def flush(self) -> None:
        await self._session.flush()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def session_add(self, obj: Any) -> None:
        self._session.add(obj)

    async def session_refresh(self, obj: Any) -> None:
        await self._session.refresh(obj)

    # def __getattr__(self, name: str) -> None:
    #     err_msg = f"'{self.__class__.__name__}' object has no attribute '{name}'"
    #     if name in self.__slots__ and not self.is_open:
    #         err_msg = f"Attempting to access '{name}' with a closed UnitOfWork"
    #     raise AttributeError(err_msg)


