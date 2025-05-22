from fastapi.testclient import TestClient
import pytest

@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "   "},
        {"title": "Ok", "priority": -1},
    ],
)
def test_create_validation_errors(client: TestClient, payload):
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 422


def test_update_validation_error(client: TestClient):
    created = client.post("/tasks", json={"title": "Good"}).json()
    tid = created["id"]

    resp = client.put(f"/tasks/{tid}", json={"title": ""})
    assert resp.status_code == 422

    resp = client.put(f"/tasks/{tid}", json={"priority": -5})
    assert resp.status_code == 422


def test_update_task_not_found(client: TestClient):
    resp = client.put("/tasks/9999", json={"title": "X"})
    assert resp.status_code == 404


def test_delete_task_not_found(client: TestClient):
    resp = client.delete("/tasks/9999")
    assert resp.status_code == 404
