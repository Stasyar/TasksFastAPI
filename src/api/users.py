from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import annotated_session, get_async_session
from src.repositories.users_rep import UserRepository
from src.schemas.users_schemas import CreateUserSchema, ResponseUserSchema, GetUserSchema
from src.services.users import UserService
from src.unit_of_work.unit_of_work import UnitOfWork

router = APIRouter(prefix='/users')


@router.post("/")
async def create_user_api(
        user_data: CreateUserSchema,
        session: annotated_session,
) -> ResponseUserSchema:

    user_service = UserService(uow=UnitOfWork(session))
    new_user = await user_service.create_user(user_data=user_data)
    return ResponseUserSchema(success=True, user_id=new_user.id)


@router.get("/{user_id}")
async def get_user_api(
        user_id: UUID4,
        session: annotated_session,
) -> GetUserSchema:

    user_service = UserService(uow=UnitOfWork(session))
    user = await user_service.get_user(user_id=user_id)
    return GetUserSchema(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        created_at=user.created_at,
    )
