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

## Files

- `Dockerfile` - Development image (Flask auto-reload)
- `docker-compose.yml` - Development orchestration
- `.dockerignore` - Exclude unnecessary files

## Stack

- **Base:** Python 3.11-slim
- **Server:** Flask development server with auto-reload
- **Port:** 5000

See README.md for setup.
