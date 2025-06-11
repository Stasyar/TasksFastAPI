"""Contains helper functions for tests."""

from collections.abc import Callable, Iterable, Sequence
from contextlib import AbstractContextManager, nullcontext
from typing import Any, TypeVar

from pydantic import BaseModel
from requests import Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from starlette.status import HTTP_200_OK


Check = Callable[[dict[str, Any]], bool]
T = TypeVar('T')


class BaseConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class TestDescription(BaseConfig):
    description: str = ''


class TestExpectation(BaseConfig):
    expected_error: AbstractContextManager = nullcontext()
    expected_status: int = HTTP_200_OK
    expected_data: Any = None
    checks: Iterable[Check] | None = None


class BaseTestCase(TestDescription, TestExpectation):
    data: dict | None = None


class RequestTestCase(BaseTestCase):
    url: str = ""
    headers: dict | None = None


async def bulk_save_models(
    session: AsyncSession,
    model: type[DeclarativeBase],
    data: Iterable[dict[str, Any]],
    *,
    commit: bool = False,
) -> None:
    """Bulk saves model objects to the database."""
    for values in data:
        await session.execute(insert(model).values(**values))

    if commit:
        await session.commit()
    else:
        await session.flush()


def prepare_payload(response: Response, exclude: Sequence[str] | None = None) -> dict:
    """Extracts the payload from the response."""
    payload = response.json()

    if exclude is None:
        return payload

    for key in exclude:
        if key in payload:
            payload.pop(key, None)

    return payload


