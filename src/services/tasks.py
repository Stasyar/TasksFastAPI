from pydantic import UUID4

from src.logger.logger import logger
from src.models import Task
from src.schemas.tasks_schema import CreateTaskSchema, PatchTaskSchema
from src.schemas.base_schemas import SuccessSchema
from src.services.base_service import BaseService


class TaskService(BaseService):
    _repo = "task"

    async def get_task(self, task_id: UUID4) -> Task | None:
        async with self.uow:
            logger.info("Getting task by id")
            return await self.uow.task.get_by_id_one_or_none(task_id)

    async def create_task(self, task_data: CreateTaskSchema) -> Task:
        async with self.uow:
            logger.info("Creating task")
            return await self.uow.task.add_one_and_get_obj(
                obj_in=task_data.model_dump(),
            )

    async def delete_by_ids(self, task_id: UUID4) -> SuccessSchema:
        async with self.uow:
            logger.info("Deleting task by id")
            deleted = await self.uow.task.delete_by_id(obj_id=task_id)
            return SuccessSchema(success=bool(deleted))

    async def get_tasks_crud(self) -> list[Task]:
        async with self.uow:
            logger.info("Getting all tasks")
            return await self.uow.task.get_all()

    async def adjust_task(self, task_id: UUID4, task_data: PatchTaskSchema) -> SuccessSchema:
        async with self.uow:
            logger.info("Adjusting task by id")
            updated = await self.uow.task.update_one_by_id(
                obj_id=task_id,
                obj_data=task_data.model_dump(exclude_unset=True),
            )
            return SuccessSchema(success=bool(updated))
