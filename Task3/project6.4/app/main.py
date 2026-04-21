from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt, time

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "secret"

def create_token(username):
    payload = {"sub": username, "exp": time.time() + 3600}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.post("/login")
def login(data: dict):
    if data["username"] != "admin":
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(data["username"])}

@app.get("/protected_resource")
def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Access granted"}
    except:
        raise HTTPException(401, "Invalid token")