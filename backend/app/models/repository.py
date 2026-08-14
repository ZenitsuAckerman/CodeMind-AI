import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False)
    repository_url: Mapped[str] = mapped_column(String(512), nullable=False)
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="repositories")
    documents = relationship("Document", back_populates="repository", cascade="all, delete-orphan")
