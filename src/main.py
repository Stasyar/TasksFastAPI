from fastapi import FastAPI

from src.api.tasks import router as tasks_router
from src.api.users import router as users_router
from src.exception_handler.exception_handler import register_exception_handlers

app = FastAPI()
app.include_router(users_router)
app.include_router(tasks_router)

register_exception_handlers(app)
