from pydantic import UUID4

from src.logger.logger import logger
from src.models import Task
from src.schemas.base_schemas import SuccessSchema
from src.schemas.tasks_schema import CreateTaskSchema, PatchTaskSchema
from src.services.base_service import BaseService


class TaskService(BaseService):
    _repo = "task"

    async def get_task(self, task_id: UUID4) -> Task | None:
        logger.info("Getting task by id")
        return await super().get_by_id_one_or_none(task_id)

    async def create_task(self, task_data: CreateTaskSchema) -> Task:
        logger.info("Creating task")
        return await super().add_one_and_get_obj(**task_data.model_dump())

    async def delete_by_ids(self, task_id: UUID4) -> SuccessSchema:
        logger.info("Deleting task by id")
        await super().delete_by_id(task_id)
        return SuccessSchema(success=True)

    async def get_tasks_crud(self) -> list[Task]:
        logger.info("Getting all tasks")
        return await super().get_all()

    async def adjust_task(
        self, task_id: UUID4, task_data: PatchTaskSchema
    ) -> SuccessSchema:
        logger.info("Adjusting task by id")
        updated = await super().update_one_by_id(
            obj_id=task_id, **task_data.model_dump(exclude_unset=True)
        )
        return SuccessSchema(success=bool(updated))

    async def get_executing_tasks_count_by_id(self, user_id: UUID4) -> SuccessSchema:
        logger.info("Deleting task by id")
        await super().get_executing_tasks_count_by_id(user_id)
        return SuccessSchema(success=True)

    async def get_viewing_tasks_count_by_id(self, user_id: UUID4) -> SuccessSchema:
        logger.info("Deleting task by id")
        await super().get_viewing_tasks_count_by_id(user_id)
        return SuccessSchema(success=True)
