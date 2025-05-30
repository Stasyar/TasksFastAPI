from typing import Annotated
from uuid import uuid4

from sqlalchemy import String, UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column

str_100 = Annotated[str, 200]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_100: String(100)
    }
