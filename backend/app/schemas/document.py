import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.document import DocumentStatus

class DocumentBase(BaseModel):
    title: str
    original_filename: str
    mime_type: str
    file_size: int
    status: DocumentStatus

class DocumentResponse(DocumentBase):
    id: uuid.UUID
    project_id: uuid.UUID
    source_type: str
    repository_id: uuid.UUID | None = None
    repo_file_path: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
