from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger.logger import logger
from src.models import User, Task
from src.repositories.base_rep import BaseRepository
from src.schemas.tasks_schema import PatchTaskSchema


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

