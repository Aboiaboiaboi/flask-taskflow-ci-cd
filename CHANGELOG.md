# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Separate database container using `busybox:latest` image
- Named Docker volume `taskflow-db` for persistent database storage
- Automatic `data/` directory creation in Flask app on startup
- Database service (`db`) in docker-compose orchestration
- Service dependency (`depends_on`) ensuring db starts before Flask app

### Changed
- **docker-compose.yml**
  - Added `db` service (busybox container holding the volume)
  - Updated `flask-app` service to mount `taskflow-db` volume at `/app/data`
  - Added `depends_on` constraint: Flask app waits for db service
  - Added top-level `volumes:` section with `taskflow-db` (local driver)
  
- **app.py**
  - Added `import os` for directory operations
  - Added `os.makedirs('data', exist_ok=True)` to create data directory on startup
  - Changed database path from `"tasks.db"` to `"data/tasks.db"` for volume-mounted location

### Technical Details
- **Database Isolation:** SQLite database now lives in a separate volume, independent of the Flask container lifecycle
- **Data Persistence:** Named volume survives `docker-compose down` (persists unless `docker-compose down -v` is used)
- **File-based Access:** Both containers access the same SQLite file via the shared volume mount
- **Container Separation:** Follows best practice of separating application from data layers

### Testing
✓ Task creation verified after containerization  
✓ Data persistence confirmed after container restart  
✓ Named volume created and tracked by Docker  
✓ API endpoints (`POST /tasks`, `GET /tasks`) functional with new setup  

### Migration Notes
- Existing `tasks.db` in workspace root is no longer used; data now stored in Docker volume
- First run creates new database in volume if not present
- Run `docker-compose down -v` to remove volume and reset database
