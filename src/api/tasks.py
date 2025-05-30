from typing import List, Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.database.db import annotated_session
from src.repositories.tasks_rep import TaskRepository
from src.schemas.base_schemas import SuccessSchema
from src.schemas.tasks_schema import CreateTaskSchema, ResponseTaskSchema, GetTaskSchema, PatchTaskSchema
from src.services.tasks import TaskService

router = APIRouter(prefix='/tasks')


def get_user_repository() -> TaskRepository:
    return TaskRepository()


def get_user_service(
    repo: TaskRepository = Depends(get_user_repository),
) -> TaskService:
    return TaskService(repo)


task_service_annotated = Annotated[TaskService, Depends(get_user_service)]


@router.post("/")
async def create_task_api(
        task_data: CreateTaskSchema,
        session: annotated_session,
        task_service: task_service_annotated,
) -> ResponseTaskSchema:

    new_task = await task_service.create_task(task_data=task_data, session=session)
    return ResponseTaskSchema(success=True,
                              task_id=new_task.id,
                              created_at=new_task.created_at,
                              )


@router.get("/{task_id}")
async def create_task_api(
        task_id: UUID4,
        session: annotated_session,
        task_service: task_service_annotated,
) -> GetTaskSchema:

    task = await task_service.get_task(task_id=task_id, session=session)
    return GetTaskSchema(id=task.id,
                         title=task.title,
                         description=task.description,
                         status=task.status,
                         )


@router.get("/", response_model=List[GetTaskSchema])
async def create_task_api(
        session: annotated_session,
        task_service: task_service_annotated,
) -> List[GetTaskSchema]:

    tasks = await task_service.get_tasks_crud(session=session)
    return tasks


@router.delete("/{task_id}")
async def delete_task_api(
        task_id: UUID4,
        session: annotated_session,
        task_service: task_service_annotated,
) -> SuccessSchema:

    task_deleted = await task_service.delete_task(task_id=task_id, session=session)

    if task_deleted:
        return SuccessSchema(success=True)
    else:
        return SuccessSchema(success=False)


@router.patch("/{task_id}")
async def patch_task_api(
        task_id: UUID4,
        task_data: PatchTaskSchema,
        session: annotated_session,
        task_service: task_service_annotated,
) -> SuccessSchema:

    task_patched = await task_service.adjust_task(task_id=task_id, task_data=task_data, session=session)

    if task_patched:
        return SuccessSchema(success=True)
    else:
        return SuccessSchema(success=False)

