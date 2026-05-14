"""
tests/test_tasks.py — Minimal tests for TaskFlow API.
One test per endpoint, proving the happy path works.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import app as flask_app


@pytest.fixture
def client(monkeypatch, tmp_path):
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr(flask_app, "DB", test_db)
    flask_app.app.config["TESTING"] = True
    flask_app.init_db()
    return flask_app.app.test_client()


def test_create_task(client):
    r = client.post("/tasks", json={"task": "Buy milk"})
    assert r.status_code == 201
    assert r.get_json()["status"] == "pending"

def test_get_all_tasks(client):
    client.post("/tasks", json={"task": "Task 1"})
    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.get_json()) == 1

def test_get_single_task(client):
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200

def test_update_task(client):
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    client.put(f"/tasks/{task_id}", json={"status": "completed"})
    r = client.get(f"/tasks/{task_id}")
    assert r.get_json()["status"] == "completed"

def test_delete_task(client):
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    client.delete(f"/tasks/{task_id}")
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 404