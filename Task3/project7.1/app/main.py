from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

app = FastAPI()

SECRET_KEY = "secret"
security = HTTPBearer()

users_db = {
    "admin": {"role": "admin"},
    "user1": {"role": "user"},
    "guest1": {"role": "guest"}
}

roles_permissions = {
    "admin": ["read", "create", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"]
}


def create_token(username):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm="HS256")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")

        if username not in users_db:
            raise HTTPException(401, "Invalid user")

        return username

    except:
        raise HTTPException(401, "Invalid token")


def check_permission(required_permission: str):
    def permission_checker(username: str = Depends(get_current_user)):
        role = users_db[username]["role"]

        if required_permission not in roles_permissions[role]:
            raise HTTPException(403, "Forbidden")

        return username

    return permission_checker


@app.post("/login")
def login(data: dict):
    if data["username"] not in users_db:
        raise HTTPException(404, "User not found")

    return {"access_token": create_token(data["username"])}


@app.get("/read")
def read_data(user: str = Depends(check_permission("read"))):
    return {"message": f"{user} can READ"}


@app.put("/update")
def update_data(user: str = Depends(check_permission("update"))):
    return {"message": f"{user} can UPDATE"}


@app.post("/create")
def create_data(user: str = Depends(check_permission("create"))):
    return {"message": f"{user} can CREATE"}


@app.delete("/delete")
def delete_data(user: str = Depends(check_permission("delete"))):
    return {"message": f"{user} can DELETE"}