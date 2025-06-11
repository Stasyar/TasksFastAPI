import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    logger = logging.getLogger("uvicorn.error")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": exc.errors(),
                "body": exc.body,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_custom_handler(request: Request, exc: HTTPException):
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": "Unauthorized: Access is denied due to invalid credentials.",
                },
            )
        if exc.status_code == status.HTTP_403_FORBIDDEN:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": "Forbidden: You do not have permission to access this resource.",
                },
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AttributeError)
    async def value_error_handler(request: Request, exc: AttributeError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
