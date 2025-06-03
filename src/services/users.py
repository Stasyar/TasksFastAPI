from pydantic import UUID4

from src.logger.logger import logger
from src.models import User
from src.schemas.users_schemas import CreateUserSchema
from src.services.base_service import BaseService


class UserService(BaseService):
    _repo = "user"

    async def get_user(self, user_id: UUID4) -> User | None:
        logger.info("Getting user by id")
        return await super().get_by_id_one_or_none(user_id)

    async def create_user(self, user_data: CreateUserSchema) -> User:
        logger.info("Creating user")
        return await super().add_one_and_get_obj(**user_data.model_dump())
