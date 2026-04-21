from fastapi import FastAPI, Header, HTTPException, Response, Depends
from pydantic import BaseModel, field_validator
from typing import Annotated
import re
from datetime import datetime

app = FastAPI()


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, value):
        pattern = r"^[a-zA-Z\-]+(,[a-zA-Z\-]+;q=\d(\.\d+)*)*$"

        if not re.match(pattern, value):
            raise ValueError("Invalid Accept-Language format")

        return value


def get_headers(
    user_agent: Annotated[str, Header(alias="User-Agent")],
    accept_language: Annotated[str, Header(alias="Accept-Language")]
) -> CommonHeaders:
    try:
        return CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Accept-Language format"
        )


@app.get("/headers")
async def headers(headers: CommonHeaders = Depends(get_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info")
async def info(
    response: Response,
    headers: CommonHeaders = Depends(get_headers)
):
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }