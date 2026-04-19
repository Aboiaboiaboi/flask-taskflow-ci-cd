from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

DB = "tasks.db"


# 🔧 helper function
def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# 🔧 create table once
def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api_info():
    return jsonify({"message": "Task Manager API with SQLite"})


# CREATE
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "task required"}), 400

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (data["task"],)
    )

    conn.commit()

    task_id = cur.lastrowid
    conn.close()

    return jsonify({
        "id": task_id,
        "task": data["task"],
        "status": "pending"
    }), 201


# READ ALL
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = connect()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(t) for t in tasks])


# READ ONE
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    conn = connect()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    conn.close()

    if task:
        return jsonify(dict(task))

    return jsonify({"error": "not found"}), 404


# UPDATE
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET task = COALESCE(?, task),
            status = COALESCE(?, status)
        WHERE id = ?
    """, (
        data.get("task"),
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()   # IMPORTANT

    return jsonify({"message": "updated"})


# DELETE
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = connect()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"deleted": id})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)