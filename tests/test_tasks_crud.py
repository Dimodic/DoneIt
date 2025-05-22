from fastapi.testclient import TestClient

def test_tasks_crud(client: TestClient):
    response = client.post("/tasks", json={"title": "Task 1", "description": "desc1", "priority": 2})
    assert response.status_code == 201
    data1 = response.json()
    assert data1["title"] == "Task 1"
    assert data1["description"] == "desc1"
    assert data1["priority"] == 2
    assert data1["completed"] is False
    assert "id" in data1

    response = client.post("/tasks", json={"title": "Task 2", "description": "desc2", "completed": True})
    assert response.status_code == 201
    data2 = response.json()
    assert data2["completed"] is True

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks_list = response.json()
    assert isinstance(tasks_list, list)
    assert len(tasks_list) >= 2
    assert tasks_list[0]["title"] == "Task 1"
    assert tasks_list[1]["title"] == "Task 2"

    task_id = data1["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    response = client.put(f"/tasks/{task_id}", json={"completed": True, "priority": 5})
    assert response.status_code == 200
    updated = response.json()
    assert updated["completed"] is True
    assert updated["priority"] == 5

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
