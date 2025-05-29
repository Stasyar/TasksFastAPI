from datetime import datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, str_100


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str_100] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("TIMEZONE('utc', now())"))

    watched_tasks = relationship("Task", secondary="TaskWatcher", back_populates="watchers")
    executed_tasks = relationship("Task", secondary="TaskExecutor", back_populates="executors")