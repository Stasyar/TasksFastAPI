from fastapi import APIRouter, Depends

from src.database.db import annotated_session
from src.schemas.users_schemas import CreateUserSchema, ResponseUserSchema
from src.services.users import UserService

router = APIRouter(prefix='/users')


@router.post("/")
async def create_user_api(
        user_data: CreateUserSchema,
        session: annotated_session,
):
    user_service = UserService()
    new_user = await user_service.create_user_crud(user_data=user_data, session=session)
    return ResponseUserSchema(success=True, user_id=new_user.id)
