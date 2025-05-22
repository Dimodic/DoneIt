from fastapi.testclient import TestClient

def test_tasks_top(client: TestClient):
    client.post("/tasks", json={"title": "Task A", "priority": 1})
    client.post("/tasks", json={"title": "Task B", "priority": 5})
    client.post("/tasks", json={"title": "Task C", "priority": 3})
    client.post("/tasks", json={"title": "Task D", "priority": 10})
    response = client.get("/tasks/top")
    assert response.status_code == 200
    top_tasks = response.json()
    priorities = [task["priority"] for task in top_tasks]
    assert priorities == sorted(priorities, reverse=True)
    response = client.get("/tasks/top", params={"limit": 2})
    assert response.status_code == 200
    top_tasks = response.json()
    assert len(top_tasks) == 2
    priorities = [task["priority"] for task in top_tasks]
    assert priorities == sorted(priorities, reverse=True)
