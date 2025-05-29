from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users_schemas import CreateUserSchema
from src.models.users import User
from src.logger.logger import logger


class UserService:
    async def create_user_crud(self, user_data: CreateUserSchema, session: AsyncSession):
        new_user = User(**user_data.model_dump())
        logger.info("New user created")
        session.add(new_user)
        await session.commit()
        logger.info("New user added to db")
        return new_user
