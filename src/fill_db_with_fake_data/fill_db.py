from sqlalchemy.ext.asyncio import AsyncSession

from src.fill_db_with_fake_data.metadata import fake_users
from src.logger.logger import logger
from src.models.users import User


async def fill_db(session: AsyncSession) -> None:
    for data in fake_users:
        user = User(**data)
        session.add(user)
    await session.commit()
    logger.info("Fake users added to db")
