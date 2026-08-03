# API Design

*(To be implemented in future sprints)*

## Principles
- RESTful principles
- JSON payloads
- Standard HTTP status codes
- API Versioning (`/api/v1/...`)

## Endpoints

### Auth & Users (Sprint 2)
- `POST /api/v1/auth/register`: Register new user
- `POST /api/v1/auth/login`: Authenticate and get JWT token
- `GET /api/v1/users/me`: Get current user profile

### Projects (Sprint 3)
- `POST /api/v1/projects`: Create a new project
- `GET /api/v1/projects`: List all projects for current user
- `GET /api/v1/projects/{id}`: Get a specific project
- `PATCH /api/v1/projects/{id}`: Update a project
- `DELETE /api/v1/projects/{id}`: Delete a project

### Planned (Future Sprints)
- `POST /api/v1/projects/{id}/documents`
- `POST /api/v1/projects/{id}/chat`
