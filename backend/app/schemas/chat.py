from typing import List
import uuid
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class Citation(BaseModel):
    document_id: uuid.UUID
    chunk_index: int

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
