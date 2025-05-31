from typing import Annotated

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.repositories.users_rep import UserRepository
from src.schemas.users_schemas import CreateUserSchema
from src.unit_of_work.unit_of_work import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: UUID4):
        async with self.uow:
            return await self.uow.user.get(id=user_id)

    async def create_user(self, user_data: CreateUserSchema):
        async with self.uow:
            return await self.uow.user.create(obj_in=user_data.model_dump())
