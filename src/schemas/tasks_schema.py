from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.models.tasks import TaskStatus


class Base(BaseModel):
    pass


class CreateTaskSchema(Base):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO


