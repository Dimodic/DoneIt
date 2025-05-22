from fastapi.testclient import TestClient

def test_tasks_search(client: TestClient):
    client.post("/tasks", json={"title": "First Task", "description": "Hello"})
    client.post("/tasks", json={"title": "Second Task", "description": "World"})
    client.post("/tasks", json={"title": "Another Task", "description": "something"})
    response = client.get("/tasks/search", params={"query": "first"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "First Task"
    response = client.get("/tasks/search", params={"query": "lo"})
    assert response.status_code == 200
    results = response.json()
    assert any(task["title"] == "First Task" for task in results)
    response = client.get("/tasks/search", params={"query": "xyz"})
    assert response.status_code == 200
    results = response.json()
    assert results == []
