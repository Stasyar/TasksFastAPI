from datetime import datetime, timezone

from pydantic import Field, EmailStr

from src.schemas.base_schemas import Base


class CreateUserSchema(Base):
    id: int
    full_name: str = Field(lt=100)
    email: EmailStr = Field(lt=120)


class ResponseUserSchema(Base):
    success: bool
    user_id: int
    created_at: datetime = datetime.now(timezone.utc)
