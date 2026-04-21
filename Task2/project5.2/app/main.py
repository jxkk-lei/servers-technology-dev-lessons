from fastapi import FastAPI, Response, Request, HTTPException, status
from pydantic import BaseModel
from itsdangerous import URLSafeSerializer, BadSignature
import uuid

app = FastAPI()

SECRET_KEY = "SUPER_SECRET_KEY"

serializer = URLSafeSerializer(SECRET_KEY, salt="session-cookie")

fake_users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com"
    }
}

user_sessions = {}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(data: LoginRequest, response: Response):
    user = fake_users_db.get(data.username)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())

    user_sessions[user_id] = user["username"]

    signed_value = serializer.dumps(user_id)

    response.set_cookie(
        key="session_token",
        value=signed_value,
        httponly=True,
        max_age=3600, 
        samesite="lax"
    )

    return {"message": "Login successful"}


@app.get("/profile")
async def profile(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    try:
        user_id = serializer.loads(session_token)
    except BadSignature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    username = user_sessions.get(user_id)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    user = fake_users_db.get(username)

    return {
        "user_id": user_id,
        "username": user["username"],
        "email": user["email"]
    }