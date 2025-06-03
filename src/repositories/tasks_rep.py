from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Task
from src.repositories.base_rep import BaseRepository


class TaskRepository(BaseRepository[Task]):
    _model = Task

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
