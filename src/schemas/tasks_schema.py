import enum
from datetime import datetime

from pydantic import UUID4, BaseModel, Field, field_validator


class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Base(BaseModel):
    @field_validator("title", check_fields=False)
    @classmethod
    def validate_title_length(cls, value) -> str | None:
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        if len(value) > 255:
            raise ValueError("Title must be no more than 255 characters long")
        return value

    @field_validator("description", check_fields=False)
    @classmethod
    def validate_description_chars(cls, value: str | None) -> str | None:
        if value is None:
            return value
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.!?-()"
        )
        for char in value:
            if char not in allowed_chars:
                error_message = f"Invalid character in description: '{char}'"
                raise ValueError(error_message)
        return value


class CreateTaskSchema(Base):
    title: str = Field(max_length=255)
    description: str | None = None
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
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    author_id: UUID4 | None = None
    assignee_id: UUID4 | None = None
    column_id: UUID4 | None = None
    sprint_id: UUID4 | None = None
    board_id: UUID4 | None = None
    group_id: UUID4 | None = None
