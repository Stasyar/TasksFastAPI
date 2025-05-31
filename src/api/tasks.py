from typing import List, Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import annotated_session, get_async_session
from src.repositories.tasks_rep import TaskRepository
from src.schemas.base_schemas import SuccessSchema
from src.schemas.tasks_schema import CreateTaskSchema, ResponseTaskSchema, GetTaskSchema, PatchTaskSchema
from src.services.tasks import TaskService
from src.unit_of_work.unit_of_work import UnitOfWork

router = APIRouter(prefix='/tasks')



@router.post("/")
async def create_task_api(
        task_data: CreateTaskSchema,
        session: annotated_session,
) -> ResponseTaskSchema:

    task_service = TaskService(uow=UnitOfWork(session))
    new_task = await task_service.create_task(task_data=task_data)
    return ResponseTaskSchema(success=True,
                              task_id=new_task.id,
                              created_at=new_task.created_at,
                              )


@router.get("/{task_id}")
async def create_task_api(
        task_id: UUID4,
        session: annotated_session,
) -> GetTaskSchema:

    task_service = TaskService(uow=UnitOfWork(session))
    task = await task_service.get_task(task_id=task_id)
    return GetTaskSchema(id=task.id,
                         title=task.title,
                         description=task.description,
                         status=task.status,
                         )


@router.get("/", response_model=List[GetTaskSchema])
async def create_task_api(
        session: annotated_session,
) -> List[GetTaskSchema]:

    task_service = TaskService(uow=UnitOfWork(session))
    tasks = await task_service.get_tasks_crud()
    return tasks


@router.delete("/{task_id}")
async def delete_task_api(
        task_id: UUID4,
        session: annotated_session,
) -> SuccessSchema:

    task_service = TaskService(uow=UnitOfWork(session))
    task_deleted = await task_service.delete_task(task_id=task_id)

    if task_deleted:
        return SuccessSchema(success=True)
    else:
        return SuccessSchema(success=False)


@router.patch("/{task_id}")
async def patch_task_api(
        task_id: UUID4,
        task_data: PatchTaskSchema,
        session: annotated_session,
) -> SuccessSchema:

    task_service = TaskService(uow=UnitOfWork(session))
    task_patched = await task_service.adjust_task(task_id=task_id, task_data=task_data)

    if task_patched:
        return SuccessSchema(success=True)
    else:
        return SuccessSchema(success=False)

