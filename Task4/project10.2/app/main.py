from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, conint, constr

app = FastAPI(title="Task4 project 10.2")


class ErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    details: list[str] = Field(default_factory=list)


class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: str | None = "Unknown"


class UserOut(BaseModel):
    username: str
    age: int
    email: EmailStr
    phone: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    details = [
        f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
        for error in exc.errors()
    ]
    print(f"Validation error: {details}")
    payload = ErrorResponse(
        status_code=422,
        error="validation_error",
        message="Request validation failed",
        details=details,
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/validate-user", response_model=UserOut)
def validate_user(user: User) -> UserOut:
    return UserOut(
        username=user.username,
        age=user.age,
        email=user.email,
        phone=user.phone or "Unknown",
    )
