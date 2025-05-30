from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4

from src.models.tasks import TaskStatus


class Base(BaseModel):
    pass


class CreateTaskSchema(Base):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    author_id: UUID4


class ResponseTaskSchema(Base):
    success: bool
    task_id: UUID4
    created_at: datetime


class GetTaskSchema(Base):
    id: UUID4
    title: str
    description: str
    status: TaskStatus

    class Config:
        orm_mode = True


class PatchTaskSchema(Base):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    author_id: Optional[UUID4] = None
    assignee_id: Optional[UUID4] = None
    column_id: Optional[UUID4] = None
    sprint_id: Optional[UUID4] = None
    board_id: Optional[UUID4] = None
    group_id: Optional[UUID4] = None
