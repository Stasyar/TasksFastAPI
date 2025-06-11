from fastapi import HTTPException
from pydantic import UUID4
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.logger.logger import logger
from src.models import User
from src.schemas.base_schemas import SuccessSchema
from src.schemas.users_schemas import (CreateUserSchema, GetUserSchema,
                                       ResponseUserSchema)
from src.services.base_service import BaseService


class UserService(BaseService):
    _repo = "user"

    async def get_user(self, user_id: UUID4) -> GetUserSchema:
        logger.info("Getting user by id")
        user = await super().get_by_id_one_or_none(user_id)
        if user:
            return GetUserSchema(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                created_at=user.created_at,
            )
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="User not found"
        )

    async def create_user(
        self, user_data: CreateUserSchema
    ) -> ResponseUserSchema | SuccessSchema | None:
        logger.info("Creating user")

        new_user = await super().add_one_and_get_obj(**user_data.model_dump())
        if new_user:
            return ResponseUserSchema(success=True, user_id=new_user.id)
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="User was not created"
        )
