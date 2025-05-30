from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users_rep import UserRepository
from src.schemas.users_schemas import CreateUserSchema


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, session: AsyncSession, user_id: UUID4):
        return await self.repo.get(id=user_id, session=session)

    async def create_user(self, session: AsyncSession, user_data: CreateUserSchema):
        return await self.repo.create(obj_in=user_data.model_dump(), session=session)
