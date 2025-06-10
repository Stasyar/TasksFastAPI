from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.repositories.base_rep import BaseRepository


class UserRepository(BaseRepository[User]):
    _model = User
