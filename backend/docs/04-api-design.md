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
- `POST /api/v1/projects/{project_id}/documents`: Upload a document
- `GET /api/v1/projects/{project_id}/documents`: List documents

### Documents (Milestone 2 & Sprint 4)
- `GET /api/v1/documents/{id}`: Fetch document metadata
- `DELETE /api/v1/documents/{id}`: Delete document and stored file
- `POST /api/v1/projects/{project_id}/documents/{document_id}/process`: Process and extract raw text from a document

### Search & Indexing (RAG Pipeline)
- `POST /api/v1/projects/{project_id}/documents/{document_id}/index`: Run the RAG indexing pipeline on a document
- `POST /api/v1/projects/{project_id}/search`: Perform semantic search against indexed documents
- `POST /api/v1/projects/{project_id}/chat`: Ask a natural language question about the project's documents

### Planned (Future Sprints)
- `POST /api/v1/projects/{id}/chat`
