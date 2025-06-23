from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, str_100, uuid_pk
from src.schemas.tasks_schema import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("TIMEZONE('utc', now())"),
        index=True,
    )

    author_id: Mapped[UUID] = mapped_column(nullable=False)
    assignee_id: Mapped[UUID] = mapped_column(nullable=True)
    viewer_id: Mapped[UUID] = mapped_column(nullable=True)

    column_id: Mapped[UUID] = mapped_column(
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=True,
    )
    sprint_id: Mapped[UUID] = mapped_column(
        ForeignKey("sprints.id", ondelete="CASCADE"),
        nullable=True,
    )
    board_id: Mapped[UUID] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=True,
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=True,
    )

    column = relationship("Column")
    sprint = relationship("Sprint")
    board = relationship("Board")
    group = relationship("Group")


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[uuid_pk]
    name: Mapped[str_100] = mapped_column(nullable=False, unique=True)


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[uuid_pk]
    name: Mapped[str_100] = mapped_column(nullable=False)
    board_id: Mapped[UUID] = mapped_column(ForeignKey("boards.id"))


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[uuid_pk]
    name: Mapped[str_100] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[uuid_pk]
    name: Mapped[str_100] = mapped_column(nullable=False, unique=True)
