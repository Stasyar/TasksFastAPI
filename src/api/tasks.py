from fastapi import APIRouter
from src.schemas.tasks_schema import CreateTaskSchema
from src.services.tasks import TaskService

router = APIRouter(prefix='/tasks')


@router.post("/")
async def create_user_api(task_data: CreateTaskSchema):
    await UserService.create_user_crud(user_data=user_data)