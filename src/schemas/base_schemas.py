from typing import Optional

from pydantic import BaseModel


class Base(BaseModel):
    pass


class SuccessSchema(Base):
    success: bool
    error: Optional[str] = None