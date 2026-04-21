from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
import secrets

app = FastAPI()

security = HTTPBasic()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

fake_users_db: dict[str, dict[str, str]] = {}


class User(BaseModel):
    username: str
    password: str


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    entered_username = credentials.username
    entered_password = credentials.password

    found_user = None
    found_username = None

    for stored_username, user_data in fake_users_db.items():
        if secrets.compare_digest(entered_username, stored_username):
            found_user = user_data
            found_username = stored_username
            break

    if not found_user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    if not pwd_context.verify(entered_password, found_user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return found_username


@app.post("/register")
def register(user: User):
    hashed_password = pwd_context.hash(user.password)

    fake_users_db[user.username] = {
        "hashed_password": hashed_password
    }

    return {"message": "User created"}


@app.get("/login")
def login(username: str = Depends(auth_user)):
    return {"message": f"Welcome, {username}!"}