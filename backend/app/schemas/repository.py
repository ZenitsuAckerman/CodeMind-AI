import uuid
from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional

class RepositoryBase(BaseModel):
    repository_url: HttpUrl
    branch: str = "main"

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryResponse(RepositoryBase):
    id: uuid.UUID
    project_id: uuid.UUID
    commit_sha: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
