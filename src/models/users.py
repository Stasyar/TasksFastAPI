from datetime import datetime
from uuid import UUID

from pydantic import UUID4
from sqlalchemy import DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, str_100, uuid_pk


class TaskWatcher(Base):
    __tablename__ = "task_watchers"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class TaskExecutor(Base):
    __tablename__ = "task_executors"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    full_name: Mapped[str_100] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))

    watched_tasks = relationship("Task", secondary="task_watchers", back_populates="watchers")
    executed_tasks = relationship("Task", secondary="task_executors", back_populates="executors")