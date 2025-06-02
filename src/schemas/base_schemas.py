from pydantic import BaseModel


class Base(BaseModel):
    pass


class SuccessSchema(Base):
    success: bool
    error: str | None = None
