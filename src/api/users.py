from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import UUID4

from src.database.db import annotated_session
from src.repositories.users_rep import UserRepository
from src.schemas.users_schemas import CreateUserSchema, ResponseUserSchema, GetUserSchema
from src.services.users import UserService

router = APIRouter(prefix='/users')


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


user_service_annotated = Annotated[UserService, Depends(get_user_service)]


@router.post("/")
async def create_user_api(
        user_data: CreateUserSchema,
        session: annotated_session,
        user_service: user_service_annotated,
) -> ResponseUserSchema:

    new_user = await user_service.create_user(user_data=user_data, session=session)
    return ResponseUserSchema(success=True, user_id=new_user.id)


@router.get("/{user_id}")
async def get_user_api(
        user_id: UUID4,
        session: annotated_session,
        user_service: user_service_annotated,
) -> GetUserSchema:

    user = await user_service.get_user(user_id=user_id, session=session)
    return GetUserSchema(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        created_at=user.created_at,
    )
