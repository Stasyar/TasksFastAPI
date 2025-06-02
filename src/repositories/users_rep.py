from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.repositories.base_rep import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)
