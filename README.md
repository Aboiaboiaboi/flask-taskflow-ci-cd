# 📝 Flask TaskFlow - Premium Task Manager

A modern, minimalist task management application built with Flask and SQLite. Features a beautiful gradient UI with smooth animations and a focus on simplicity and elegance.

## ✨ Features

- ✅ **Create, Read, Update, Delete** tasks (CRUD operations)
- ✅ **Real-time filtering** by task status (All/Pending/Completed)
- ✅ **Premium minimalist design** with smooth animations
- ✅ **Responsive layout** - works perfectly on desktop and mobile
- ✅ **SQLite database** for persistent storage
- ✅ **RESTful API** endpoints for all operations
- ✅ **XSS protection** via HTML escaping
- ✅ **Beautiful gradient backgrounds** and modern typography

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aboiaboiaboi/flask-taskflow-ci-cd.git
   cd flask-taskflow-ci-cd
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python3 app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:5000`
   - Start managing your tasks!

## 📁 Project Structure

```
flask-taskflow-ci-cd/
├── app.py                          # Flask application & API routes
├── requirements.txt                # Python dependencies
├── tasks.db                        # SQLite database (auto-generated)
├── frontend/
│   ├── templates/
│   │   └── index.html             # Main HTML template
│   └── static/
│       ├── style.css              # Premium styling with radial gradients
│       └── script.js              # Client-side state management
├── .github/
│   └── copilot-instructions.md    # AI agent development guide
└── README.md                       # This file
```

## 🎨 Design & Styling

### Premium Features
- **Radial gradients** from black center (30%) to purple (100%) on header, body, and stats
- **System font stack** for cross-platform consistency
- **Sophisticated shadow system** with hover elevation effects
- **REM-based spacing** for perfect vertical/horizontal rhythm
- **12px border radius** for modern rounded aesthetics
- **Material Design animations** with cubic-bezier timing

### Responsive Breakpoints
- **Desktop:** Full layout with multi-column stats grid
- **Tablet/Mobile (≤768px):** Single column layout, full-width buttons, edge-to-edge design

## 🔌 API Endpoints

### Health Check
- `GET /api` - Returns API info

### Tasks Operations
| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| `GET` | `/tasks` | Fetch all tasks | `[{id, task, status}, ...]` |
| `POST` | `/tasks` | Create new task | `{id, task, status}` (201) |
| `GET` | `/tasks/<id>` | Fetch single task | `{id, task, status}` or 404 |
| `PUT` | `/tasks/<id>` | Update task | `{"message": "updated"}` |
| `DELETE` | `/tasks/<id>` | Delete task | `{"deleted": id}` |

### Request/Response Examples

**Create Task:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Buy groceries"}'
```

**Update Task Status:**
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## 🗄️ Database

### Schema
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);
```

### Reset Database
To start with a fresh database:
```bash
rm tasks.db
python3 app.py  # Will auto-create new tasks.db
```

## 🛠️ Development

### Virtual Environment Management

**Deactivate venv:**
```bash
deactivate
```

**Delete venv (to clean up):**
```bash
rm -rf venv/
```

### Rebuild Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Project-Specific Notes

- **Framework:** Flask with SQLite3
- **Architecture:** MVC pattern with server-side rendering + client-side state management
- **Frontend State:** Client-side `allTasks[]` array (in-memory, no persistence except via API)
- **Filtering:** UI-only (all filtering happens client-side)
- **Security:** XSS protection via `escapeHtml()` function

## 📚 AI Development Guide

For AI agents and automated development tools, see `.github/copilot-instructions.md` for:
- Detailed architecture explanation
- Code patterns and conventions
- Database operation guidelines
- Component styling reference
- Common development tasks

## 🎯 Common Tasks

### Adding a New Task Field

1. **Update database schema** in `app.py` `init_db()` function
2. **Update API routes** to handle the new field
3. **Update HTML form** in `frontend/templates/index.html`
4. **Update JavaScript** in `frontend/static/script.js` for state and rendering
5. **Add CSS styling** in `frontend/static/style.css` if needed

### Troubleshooting

**Port 5000 already in use:**
```bash
# On macOS/Linux, find and kill the process:
lsof -i :5000
kill -9 <PID>

# Or run on different port:
flask run --port 5001
```

**Virtual environment issues:**
```bash
# Completely clean and rebuild
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Database locked error:**
```bash
# Reset the database
rm tasks.db
python3 app.py
```

## 📖 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite3 Python Docs](https://docs.python.org/3/library/sqlite3.html)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📝 License

This project is open source and available for learning and personal use.

## 👨‍💻 Contributing

Feel free to fork, modify, and improve! Some ideas:
- Add task due dates
- Implement task categories/tags
- Add task priority levels
- Dark/light theme toggle
- User authentication
- Task search functionality

---

**Made with ❤️ - Premium Task Management for Everyone**

Last updated: April 19, 2026
