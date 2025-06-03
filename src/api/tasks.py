from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED

from src.schemas.base_schemas import SuccessSchema
from src.schemas.tasks_schema import (CreateTaskSchema, GetTaskSchema,
                                      PatchTaskSchema, ResponseTaskSchema)
from src.services.tasks import TaskService

router = APIRouter(prefix="/tasks")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED
)
async def create_task_api(
    task_data: CreateTaskSchema,
    task_service: TaskService = Depends(TaskService),
) -> ResponseTaskSchema:

    new_task = await task_service.create_task(task_data=task_data)
    return ResponseTaskSchema(
        success=True,
        task_id=new_task.id,
        created_at=new_task.created_at,
    )


@router.get(path="/{task_id}")
async def get_task_by_id_api(
    task_id: UUID4,
    task_service: TaskService = Depends(TaskService),
) -> GetTaskSchema:

    task = await task_service.get_task(task_id=task_id)
    return GetTaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
    )


@router.get(
    path="/",
    response_model=list[GetTaskSchema]
)
async def get_tasks_api(
    task_service: TaskService = Depends(TaskService),
) -> list[GetTaskSchema]:

    tasks = await task_service.get_tasks_crud()
    return tasks


@router.delete(path="/{task_id}")
async def delete_task_api(
    task_id: UUID4,
    task_service: TaskService = Depends(TaskService),
) -> SuccessSchema:

    return await task_service.delete_by_ids(task_id=task_id)


@router.patch(path="/{task_id}")
async def patch_task_api(
    task_id: UUID4,
    task_data: PatchTaskSchema,
    task_service: TaskService = Depends(TaskService),
) -> SuccessSchema:

    return await task_service.adjust_task(task_id=task_id, task_data=task_data)
