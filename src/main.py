from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.tasks import router as tasks_router
from src.database.db import async_engine
from src.exception_handler.exception_handler import register_exception_handlers
from src.models import Base

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app.include_router(tasks_router)

register_exception_handlers(app)
