from fastapi import FastAPI
from app.models.models import User

app = FastAPI()

my_user = User(name = "Elin", id = 19)

@app.get("/users")
def root():
    return my_user
