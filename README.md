# Flask TaskFlow

Premium task manager with Flask, SQLite, and modern UI.

## Setup

```bash
# Clone
git clone https://github.com/aboiaboiaboi/flask-taskflow-ci-cd.git
cd flask-taskflow-ci-cd

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install & run
pip install -r requirements.txt
python3 app.py

# Open http://localhost:5000
```

## Docker

```bash
docker-compose up
```

Visit `http://localhost:5000`

## Features

- CRUD operations (Create, Read, Update, Delete tasks)
- Real-time filtering (All/Pending/Completed)
- Responsive design (desktop & mobile)
- RESTful API
- SQLite persistence
- XSS protection
- Premium UI with gradients & animations

## API

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/tasks` | Get all tasks |
| `POST` | `/tasks` | Create task |
| `PUT` | `/tasks/<id>` | Update task |
| `DELETE` | `/tasks/<id>` | Delete task |

**Example:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Buy groceries"}'
```

## Database

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);
```

Reset: `rm tasks.db && python3 app.py`

## Stack

- Python 3.8+
- Flask 3.1.3
- SQLite
- Vanilla JavaScript
- Modern CSS
