# Database

*(To be implemented in future sprints)*

## Schema Design
- **Users**: Core user authentication details (`id`, `email`, `password_hash`).
- **Projects**: The core container for a user's AI assets (`id`, `owner_id`, `name`, `description`).
    - *Relationship*: A User has many Projects (`One-to-Many`).
- **Documents/Artifacts**: Metadata about uploaded files. *(Future)*

## Migrations
We use Alembic for asynchronous database migrations.
- `alembic revision --autogenerate -m "description"`
- `alembic upgrade head`
