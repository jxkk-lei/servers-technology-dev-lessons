from fastapi import FastAPI, Response, Request, HTTPException, status
from pydantic import BaseModel
from itsdangerous import URLSafeSerializer, BadSignature
import uuid
import time

app = FastAPI()

SECRET_KEY = "SUPER_SECRET_KEY"
serializer = URLSafeSerializer(SECRET_KEY, salt="session")

SESSION_LIFETIME = 300
REFRESH_THRESHOLD = 180

fake_users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com"
    }
}

sessions = {}


class LoginRequest(BaseModel):
    username: str
    password: str


def create_session_token(user_id: str, timestamp: int) -> str:
    data = f"{user_id}.{timestamp}"
    signature = serializer.dumps(data)
    signed = serializer.dumps({"user_id": user_id, "ts": timestamp})
    return signed


def parse_session_token(token: str):
    try:
        data = serializer.loads(token)
        user_id = data["user_id"]
        timestamp = data["ts"]
        return user_id, timestamp
    except BadSignature:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )


@app.post("/login")
async def login(data: LoginRequest, response: Response):
    user = fake_users_db.get(data.username)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    sessions[user_id] = user["username"]

    current_time = int(time.time())

    token = create_session_token(user_id, current_time)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,
        max_age=SESSION_LIFETIME
    )

    return {"message": "Login successful"}


@app.get("/profile")
async def profile(request: Request, response: Response):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )


    user_id, last_activity = parse_session_token(token)

    if user_id not in sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    current_time = int(time.time())
    elapsed = current_time - last_activity

    if elapsed > SESSION_LIFETIME:
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    if REFRESH_THRESHOLD <= elapsed <= SESSION_LIFETIME:
        new_time = current_time
        new_token = create_session_token(user_id, new_time)

        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=SESSION_LIFETIME
        )

    username = sessions[user_id]
    user = fake_users_db[username]

    return {
        "user_id": user_id,
        "username": user["username"],
        "email": user["email"],
        "last_activity": last_activity,
        "current_time": current_time,
        "elapsed_seconds": elapsed
    }