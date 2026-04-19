# Docker

## Quick Start

```bash
# Development
docker-compose up
# Open http://localhost:5000
```

## Build

```bash
# Build image
docker build -t flask-taskflow .
```

## Commands

```bash
# Run container
docker run -p 5000:5000 flask-taskflow

# Run with volume (development)
docker run -p 5000:5000 -v $(pwd):/app flask-taskflow

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Architecture: Separate App & Database Containers

**Multi-container design** with service separation:

| Service | Image | Role | Volume |
|---------|-------|------|--------|
| `flask-app` | Python 3.11-slim | Flask dev server (port 5000) | `.:/app` (code), `taskflow-db:/app/data` (db) |
| `db` | busybox:latest | Persistent storage holder | `taskflow-db:/data` |

**Key Details:**
- Named volume `taskflow-db` persists SQLite database across container restarts
- Both services on `taskflow-network` (bridge)
- Flask app depends on db service (startup ordering)
- Database file: `/app/data/tasks.db`

## Files

- `Dockerfile` - Development image (Flask auto-reload)
- `docker-compose.yml` - Development orchestration with app + db services
- `.dockerignore` - Exclude unnecessary files (includes `tasks.db`)

## Stack

- **Base:** Python 3.11-slim (app), busybox:latest (data)
- **Server:** Flask development server with auto-reload
- **Database:** SQLite (file-based, containerized volume)
- **Port:** 5000 (app)
- **Orchestration:** Docker Compose v3.9

See README.md for setup.
