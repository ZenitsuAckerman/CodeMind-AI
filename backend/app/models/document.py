import uuid
import enum
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base

class DocumentStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    INDEXING = "INDEXING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False) # Size in bytes
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED, nullable=False)
    
    source_type: Mapped[str] = mapped_column(String(50), default="upload", nullable=False)
    repository_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), nullable=True)
    repo_file_path: Mapped[str] = mapped_column(String(1024), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="documents")
    repository = relationship("Repository", back_populates="documents")
    content = relationship("DocumentContent", back_populates="document", uselist=False, cascade="all, delete-orphan")
