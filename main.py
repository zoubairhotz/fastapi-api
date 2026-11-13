from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

todos: dict[int, Todo] = {}
next_id = 1

@app.get("/")
def hello():
    return "hello"

@app.get("/todos")
def list_todos():
    return list(todos.values())

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = todos.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", status_code=201)
def create_todo(payload: TodoCreate):
    global next_id
    todo = Todo(id=next_id, **payload.model_dump())
    todos[next_id] = todo
    next_id += 1
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, payload: TodoUpdate):
    todo = todos.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(todo, key, value)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]  