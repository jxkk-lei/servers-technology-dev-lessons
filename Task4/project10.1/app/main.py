from __future__ import annotations

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Task4 project 10.1")


class ErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    details: list[str] = Field(default_factory=list)


class AppException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = "application_error"
    message = "Application error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message


class CustomExceptionA(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "condition_failed"
    message = "Required condition was not met"


class CustomExceptionB(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error = "resource_not_found"
    message = "Requested resource was not found"


def error_response(exc: AppException) -> JSONResponse:
    payload = ErrorResponse(
        status_code=exc.status_code,
        error=exc.error,
        message=exc.message,
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(_, exc: CustomExceptionA) -> JSONResponse:
    print(f"CustomExceptionA: {exc.message}")
    return error_response(exc)


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(_, exc: CustomExceptionB) -> JSONResponse:
    print(f"CustomExceptionB: {exc.message}")
    return error_response(exc)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/custom-a")
def custom_a(allowed: bool = False) -> dict[str, str]:
    if not allowed:
        raise CustomExceptionA("Pass allowed=true to satisfy the condition")
    return {"status": "condition accepted"}


@app.get("/custom-b/{resource_id}")
def custom_b(resource_id: int) -> dict[str, int | str]:
    if resource_id != 1:
        raise CustomExceptionB(f"Resource with id={resource_id} was not found")
    return {"id": resource_id, "status": "found"}
