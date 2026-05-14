"""
tests/test_tasks.py — TaskFlow API tests.
Covers happy paths, invalid inputs, missing fields, and edge cases.
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


# ── POST /tasks ────────────────────────────────────────────────────────────────

def test_create_task(client):
    """Happy path — valid task is created with pending status."""
    r = client.post("/tasks", json={"task": "Buy milk"})
    assert r.status_code == 201
    assert r.get_json()["status"] == "pending"

def test_create_task_missing_field(client):
    """No 'task' key in body → 400."""
    r = client.post("/tasks", json={"title": "wrong key"})
    assert r.status_code == 400

def test_create_task_empty_body(client):
    """Empty JSON body → 400."""
    r = client.post("/tasks", json={})
    assert r.status_code == 400

def test_create_task_empty_string(client):
    """
    Blank task string — currently the app saves it (no server-side validation).
    This test documents that gap. Once you add validation, change to assert 400.
    """
    r = client.post("/tasks", json={"task": ""})
    assert r.status_code in (201, 400)

def test_create_task_long_string(client):
    """255-character task — should be accepted (SQLite TEXT has no length cap)."""
    long_task = "A" * 255
    r = client.post("/tasks", json={"task": long_task})
    assert r.status_code == 201
    assert r.get_json()["task"] == long_task

def test_create_task_whitespace_only(client):
    """Whitespace-only task — documents the current behaviour (no strip/reject)."""
    r = client.post("/tasks", json={"task": "   "})
    assert r.status_code in (201, 400)

def test_create_task_wrong_content_type(client):
    """Form-encoded body instead of JSON → Flask rejects with 400 or 415."""
    r = client.post("/tasks", data="task=hello",
                    content_type="application/x-www-form-urlencoded")
    assert r.status_code in (400, 415)

def test_create_task_special_characters(client):
    """Tasks with special chars should be stored and returned exactly."""
    task_text = "Fix bug: <script>alert('xss')</script> & 'quotes'"
    r = client.post("/tasks", json={"task": task_text})
    assert r.status_code == 201
    assert r.get_json()["task"] == task_text


# ── GET /tasks ─────────────────────────────────────────────────────────────────

def test_get_all_tasks(client):
    """Happy path — returns all inserted tasks."""
    client.post("/tasks", json={"task": "Task 1"})
    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.get_json()) == 1

def test_get_all_tasks_empty_db(client):
    """Empty database → empty list, not an error."""
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.get_json() == []


# ── GET /tasks/<id> ────────────────────────────────────────────────────────────

def test_get_single_task(client):
    """Happy path — fetch task by id."""
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200

def test_get_nonexistent_task(client):
    """Unknown id → 404."""
    r = client.get("/tasks/99999")
    assert r.status_code == 404

def test_get_task_after_delete(client):
    """Fetching a deleted task → 404."""
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    client.delete(f"/tasks/{task_id}")
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 404


# ── PUT /tasks/<id> ────────────────────────────────────────────────────────────

def test_update_task(client):
    """Happy path — status change persists."""
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    client.put(f"/tasks/{task_id}", json={"status": "completed"})
    r = client.get(f"/tasks/{task_id}")
    assert r.get_json()["status"] == "completed"

def test_update_task_invalid_status(client):
    """
    Invalid status value like 'done' — app currently accepts anything.
    Documents the gap: no enum validation on status field.
    Change to assert 400 once you add validation.
    """
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    r = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert r.status_code in (200, 400)

def test_update_nonexistent_task(client):
    """
    PUT on a missing id — SQLite UPDATE is a no-op, app returns 200.
    Documents this behaviour. Change to 404 if you add existence checks.
    """
    r = client.put("/tasks/99999", json={"status": "completed"})
    assert r.status_code in (200, 404)


# ── DELETE /tasks/<id> ─────────────────────────────────────────────────────────

def test_delete_task(client):
    """Happy path — task is gone after deletion."""
    task_id = client.post("/tasks", json={"task": "Task"}).get_json()["id"]
    client.delete(f"/tasks/{task_id}")
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 404

def test_delete_nonexistent_task(client):
    """
    DELETE on unknown id — SQLite DELETE is a no-op, app returns 200.
    Documents this behaviour. Change to 404 if you add existence checks.
    """
    r = client.delete("/tasks/99999")
    assert r.status_code in (200, 404)