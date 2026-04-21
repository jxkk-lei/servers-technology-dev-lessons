from fastapi import FastAPI, HTTPException

app = FastAPI()

todos = {}
counter = 1

@app.post("/todos")
def create(todo: dict):
    global counter
    todo["id"] = counter
    todo["completed"] = False
    todos[counter] = todo
    counter += 1
    return todo

@app.get("/todos/{id}")
def read(id: int):
    if id not in todos:
        raise HTTPException(404)
    return todos[id]

@app.put("/todos/{id}")
def update(id: int, data: dict):
    if id not in todos:
        raise HTTPException(404)
    todos[id].update(data)
    return todos[id]

@app.delete("/todos/{id}")
def delete(id: int):
    if id not in todos:
        raise HTTPException(404)
    del todos[id]
    return {"message": "Deleted"}