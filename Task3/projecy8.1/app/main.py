from fastapi import FastAPI
from database import get_db_connection, init_db

app = FastAPI()
init_db()

@app.post("/register")
def register(data: dict):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )
    conn.commit()
    conn.close()
    return {"message": "User registered successfully!"}