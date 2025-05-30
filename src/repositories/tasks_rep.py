from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger.logger import logger
from src.models import Task
from src.repositories.base_rep import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self):
        super().__init__(Task)

    async def adjust(self, task_id: UUID4, task_data: dict, session: AsyncSession) -> bool:
        logger.info("Adjusting task")
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return False

        for field, value in task_data.items():
            setattr(task, field, value)

        await session.commit()
        await session.refresh(task)
        logger.info("Task adjusted")
        return True

