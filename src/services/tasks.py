from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.tasks_schema import CreateTaskSchema, PatchTaskSchema
from src.unit_of_work.unit_of_work import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_task(self, task_id: UUID4):
        async with self.uow:
            return await self.uow.task.get(id=task_id)

    async def create_task(self, task_data: CreateTaskSchema):
        async with self.uow:
            return await self.uow.task.create(obj_in=task_data.model_dump())

    async def delete_task(self, task_id: UUID4):
        async with self.uow:
            return await self.uow.task.delete(id=task_id)

    async def get_tasks_crud(self):
        async with self.uow:
            return await self.uow.task.list()

    async def adjust_task(self, task_id: UUID4, task_data: PatchTaskSchema):
        async with self.uow:
            return await self.uow.task.adjust(
                task_id=task_id,
                task_data=task_data.model_dump(exclude_unset=True)
            )
