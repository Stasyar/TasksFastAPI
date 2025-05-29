from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_100 = Annotated[str, 200]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_100: String(100)
    }
