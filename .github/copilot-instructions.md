# Copilot Instructions

## Architecture

**Type:** Flask + SQLite task manager  
**MVC Pattern:** Server-side rendering + client-side state management

### Backend (`app.py`)
- Connection per request pattern with `connect()` helper
- Row factory enabled for dict-like access: `conn.row_factory = sqlite3.Row`
- **Critical:** Always close connections explicitly
- API: 7 REST endpoints (CRUD + health check)

### Frontend (`frontend/`)
- Template: `templates/index.html` (Jinja2)
- State: `script.js` - in-memory `allTasks[]` array
- Styling: `style.css` - radial gradients, REM-based spacing
- Filtering: UI-only (client-side with `currentFilter` variable)

### Database
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);
```

## API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| `GET` | `/` | Serve HTML |
| `GET` | `/api` | Health check |
| `POST` | `/tasks` | Create (201) |
| `GET` | `/tasks` | Get all |
| `GET` | `/tasks/<id>` | Get one |
| `PUT` | `/tasks/<id>` | Update |
| `DELETE` | `/tasks/<id>` | Delete |

**Error Handling:** 400 (validation), 404 (not found), 201 (created)

## Key Patterns

### Database Operations
- Parameterized queries: `(?, ?, ?)` - NEVER string interpolation
- Partial updates: `COALESCE(?, field)` pattern
- Connection closure: Critical for SQLite lock release

### Frontend Flow
1. `DOMContentLoaded` → `loadTasks()` → fetch → populate `allTasks[]`
2. User action → API call → update local state → `renderTasks()`
3. Filter applied via `currentFilter` (UI-only)

### Status Values
Only: `"pending"` (default) and `"completed"`

## Styling

### Colors & System
```css
--primary-color: #764ba2
--primary-dark: #5a3880
--success-color: #2ecc71
--danger-color: #e74c3c
--dark-color: #1a1a1a
--light-color: #f5f5f5
```

### Key Classes
- **Task Items:** `display: flex`, `border-left: 3px`, hover elevation
- **Buttons:** `.btn-primary`, `.btn-danger`, `.btn-success` with shadows
- **Stats Cards:** Radial gradient (black 30% → purple), hover transform
- **Inputs:** 1px border, focus with purple outline

### Responsive
Single breakpoint at `@media (max-width: 768px)` - flex-column, full-width buttons

## Common Tasks

### Add New Field
1. Update `init_db()` schema
2. Update POST/PUT routes
3. Update HTML form
4. Update `renderTasks()` in script.js
5. Add CSS if needed

### Reset Database
```bash
rm tasks.db
python3 app.py
```

## Stack

- Python 3.8+
- Flask 3.1.3
- SQLite (no external DB)
- Vanilla JS (no frameworks)
- System fonts (no web fonts)
- CSS Grid/Flexbox

## Docker

Dev: `docker-compose up`  
Prod: `docker-compose -f docker-compose.production.yml up -d`

See DOCKER.md for details.
