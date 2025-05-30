from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.tasks_rep import TaskRepository
from src.schemas.tasks_schema import CreateTaskSchema, PatchTaskSchema


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def get_task(self, session: AsyncSession, task_id: UUID4):
        return await self.repo.get(id=task_id, session=session)

    async def create_task(self, session: AsyncSession, task_data: CreateTaskSchema):
        return await self.repo.create(obj_in=task_data.model_dump(), session=session)

    async def delete_task(self, session: AsyncSession, task_id: UUID4):
        return await self.repo.delete(id=task_id, session=session)

    async def get_tasks_crud(self, session: AsyncSession):
        return await self.repo.list(session=session)

    async def adjust_task(self, task_id: UUID4, task_data: PatchTaskSchema, session: AsyncSession):
        return await self.repo.adjust(
            task_id=task_id,
            task_data=task_data.model_dump(exclude_unset=True),
            session=session
        )
