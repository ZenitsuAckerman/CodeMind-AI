from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy declarative base model.
    All database models should inherit from this class.
    """
    pass

# Import all models here so Alembic can find them in its env.py
from app.models.user import User  # noqa
from app.models.project import Project  # noqa
from app.models.document import Document  # noqa
from app.models.document_content import DocumentContent  # noqa
from app.models.document_chunk import DocumentChunk  # noqa
