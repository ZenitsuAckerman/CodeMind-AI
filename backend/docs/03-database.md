# Database

*(To be implemented in future sprints)*

## Schema Design
- **Users**: Core user authentication details.
- **Projects**: Workspaces containing multiple artifacts.
- **Documents/Artifacts**: Metadata about uploaded files.

## Migrations
We use Alembic for asynchronous database migrations.
- `alembic revision --autogenerate -m "description"`
- `alembic upgrade head`
