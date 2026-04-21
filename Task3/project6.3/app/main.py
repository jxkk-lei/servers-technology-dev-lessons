from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "DEV")
DOCS_USER = os.getenv("DOCS_USER", "")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "")

if MODE not in ("DEV", "PROD"):
    raise ValueError("MODE must be DEV or PROD")

# Всегда отключаем стандартные docs/openapi/redoc
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

security = HTTPBasic()


def docs_auth(credentials: HTTPBasicCredentials = Depends(security)):
    is_valid_user = secrets.compare_digest(credentials.username, DOCS_USER)
    is_valid_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)

    if not (is_valid_user and is_valid_password):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/")
def root():
    return {"message": f"App is running in {MODE} mode"}


# Документация доступна только в DEV и только с Basic Auth
if MODE == "DEV":

    @app.get("/docs", include_in_schema=False)
    def custom_docs(_: HTTPBasicCredentials = Depends(docs_auth)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="Protected Docs"
        )

    @app.get("/openapi.json", include_in_schema=False)
    def custom_openapi(_: HTTPBasicCredentials = Depends(docs_auth)):
        return JSONResponse(app.openapi())