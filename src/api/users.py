from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED

from src.schemas.users_schemas import (CreateUserSchema, GetUserSchema,
                                       ResponseUserSchema)
from src.services.users import UserService

router = APIRouter(prefix="/users")


@router.post(path="/", status_code=HTTP_201_CREATED)
async def create_user_api(
    user_data: CreateUserSchema,
    user_service: UserService = Depends(UserService),
) -> ResponseUserSchema:

    return await user_service.create_user(user_data=user_data)


@router.get(path="/{user_id}")
async def get_user_api(
    user_id: UUID4,
    user_service: UserService = Depends(UserService),
) -> GetUserSchema:

    return await user_service.get_user(user_id=user_id)
