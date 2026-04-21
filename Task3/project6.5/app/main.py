from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
import jwt, time, secrets
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "secret"

db = {}

def create_token(username):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm="HS256")

@app.post("/register")
@limiter.limit("1/minute")
def register(request: Request, data: dict):
    if data["username"] in db:
        raise HTTPException(409, "User already exists")

    db[data["username"]] = pwd_context.hash(data["password"])
    return {"message": "New user created"}

@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: dict):
    user = db.get(data["username"])

    if not user:
        raise HTTPException(404, "User not found")

    if not pwd_context.verify(data["password"], user):
        raise HTTPException(401, "Authorization failed")

    return {
        "access_token": create_token(data["username"]),
        "token_type": "bearer"
    }