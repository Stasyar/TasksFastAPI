from fastapi import FastAPI

from src.api.users import router as users_router
from src.api.tasks import router as tasks_router
from src.database.db import async_engine
from src.models.base import Base
from src.models import users, tasks


app = FastAPI()
app.include_router(users_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def create_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
