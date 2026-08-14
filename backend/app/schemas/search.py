from typing import List
import uuid
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class SearchResult(BaseModel):
    chunk_id: uuid.UUID
    score: float
    document_id: uuid.UUID
    content: str
    chunk_index: int
    source_type: str | None = None
    repository_id: uuid.UUID | None = None
    repo_file_path: str | None = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
