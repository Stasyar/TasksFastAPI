from datetime import datetime

from pydantic import UUID4, EmailStr, Field

from src.schemas.base_schemas import Base


class CreateUserSchema(Base):
    full_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=120)


class ResponseUserSchema(Base):
    success: bool
    user_id: UUID4


class GetUserSchema(Base):
    id: UUID4
    full_name: str
    email: str
    created_at: datetime
