from typing import List, Optional
import uuid
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class Citation(BaseModel):
    document_id: uuid.UUID
    chunk_index: int
    source_type: str
    repository_id: Optional[uuid.UUID] = None
    repo_file_path: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
