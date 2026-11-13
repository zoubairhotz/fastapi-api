import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def reset_state():
    main.todos.clear()
    main.next_id = 1
    yield


@pytest.fixture
def client():
    return TestClient(main.app)


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "hello"


def test_list_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    response = client.post("/todos", json={"title": "learn fastapi"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "learn fastapi", "completed": False}


def test_create_todo_missing_title(client):
    response = client.post("/todos", json={})
    assert response.status_code == 422


def test_get_todo(client):
    client.post("/todos", json={"title": "learn fastapi"})
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "learn fastapi"


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_list_todos(client):
    client.post("/todos", json={"title": "first"})
    client.post("/todos", json={"title": "second"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert [todo["title"] for todo in response.json()] == ["first", "second"]


def test_update_todo(client):
    client.post("/todos", json={"title": "learn fastapi"})
    response = client.put("/todos/1", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "learn fastapi"


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"completed": True})
    assert response.status_code == 404


def test_delete_todo(client):
    client.post("/todos", json={"title": "learn fastapi"})
    response = client.delete("/todos/1")
    assert response.status_code == 204
    assert client.get("/todos/1").status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
