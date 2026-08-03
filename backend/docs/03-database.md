# Database

*(To be implemented in future sprints)*

## Schema Design
- **Users**: Core user authentication details (`id`, `email`, `password_hash`).
- **Projects**: The core container for a user's AI assets (`id`, `owner_id`, `name`, `description`).
    - *Relationship*: A User has many Projects (`One-to-Many`).
- **Documents**: Uploaded files belonging to a project (`id`, `project_id`, `title`, `stored_filename`, `status`).
    - *Relationship*: A Project has many Documents (`One-to-Many`).
    - *Statuses*: `UPLOADED`, `PROCESSING`, `PROCESSED`, `INDEXED`, `FAILED`.
- **DocumentContent**: Stores raw extracted text from a Document.
    - *Relationship*: A Document has one DocumentContent (`One-to-One`).
- **DocumentChunk**: Stores chunks of text split from a DocumentContent.
    - *Relationship*: A DocumentContent has many DocumentChunks (`One-to-Many`).

## Migrations
We use Alembic for asynchronous database migrations.
- `alembic revision --autogenerate -m "description"`
- `alembic upgrade head`
