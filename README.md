# Flask TaskFlow

A simple task manager built with Flask + SQLite featuring a modern UI, REST API, and Docker support.

---

## 🚀 Run with Docker (Recommended)

Pull and run directly from Docker Hub:

```bash
docker run -d \
-p 5000:5000 \
-v taskflow-data:/app/data \
--name taskflow \
aboiaboiaboi/flask-taskflow
```

Open:
http://localhost:5000

✔ Includes persistent database using Docker volume

---

## 🐳 Run with Docker Compose (From GitHub)

### 1. Clone the repository

```bash
git clone https://github.com/aboiaboiaboi/flask-taskflow-ci-cd.git
cd flask-taskflow-ci-cd
```

### 2. Start the application

```bash
docker compose up --build
```

### 3. Access app

http://localhost:5000

✔ Auto-handles volumes, ports, and environment

---

## 💻 Manual Setup (Development Mode)

### 1. Clone repo

```bash
git clone https://github.com/aboiaboiaboi/flask-taskflow-ci-cd.git
cd flask-taskflow-ci-cd
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run application

```bash
python3 app.py
```

Open:
http://localhost:5000

---

## 📦 Features

- Create, update, delete tasks (CRUD)
- Filter tasks (All / Pending / Completed)
- REST API support
- SQLite persistence
- Responsive modern UI
- XSS-safe input handling
- Lightweight Flask backend

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| POST | /tasks | Create a task |
| PUT | /tasks/<id> | Update task |
| DELETE | /tasks/<id> | Delete task |

### Example request:

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Buy groceries"}'
```

---

## 🗄 Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);
```

Reset database:

```bash
rm data/tasks.db
```

---

## 🧱 Tech Stack

- Python 3.11
- Flask
- SQLite
- Docker
- Docker Compose
- HTML / CSS / JavaScript

---

## 🧠 Notes

- Docker version uses persistent volume (`taskflow-data`)
- Compose version automatically configures everything
- Manual setup is for development only

