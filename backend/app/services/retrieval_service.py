import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models.document import Document
from app.models.document_content import DocumentContent
from app.models.document_chunk import DocumentChunk
from app.services.project_service import ProjectService
from app.services.rag.embedding_service import embedding_service
from app.services.rag.qdrant_service import qdrant_service
from app.services.rag.bm25_service import bm25_service
from app.services.rag.cross_encoder_service import cross_encoder_service

class RetrievalService:
    """
    Handles semantic search queries for projects.
    """
    
    @staticmethod
    async def search(db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # 1. Enforce ownership: user must own the project to search its contents
        await ProjectService.get_project(db, project_id=project_id, user_id=user_id)
        
        # 2. Vector Search (Semantic) -> Top 20
        query_vector = embedding_service.embed_text(query)
        vector_results = qdrant_service.search(project_id=project_id, query_vector=query_vector, limit=20)
        
        # 3. Keyword Search (BM25) -> Top 20
        # First, fetch all chunks for this project from DB
        stmt = (
            select(
                DocumentChunk,
                Document.id.label("doc_id"),
                Document.source_type,
                Document.repository_id,
                Document.repo_file_path
            )
            .join(DocumentContent, DocumentChunk.document_content_id == DocumentContent.id)
            .join(Document, DocumentContent.document_id == Document.id)
            .where(Document.project_id == project_id)
        )
        result = await db.execute(stmt)
        rows = result.all()
        
        db_chunks = []
        for chunk, doc_id, source_type, repository_id, repo_file_path in rows:
            db_chunks.append({
                "chunk_id": str(chunk.id),
                "document_id": str(doc_id),
                "project_id": str(project_id),
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "source_type": source_type,
                "repository_id": str(repository_id) if repository_id else None,
                "repo_file_path": repo_file_path
            })
            
        keyword_results = bm25_service.search(query=query, db_chunks=db_chunks, limit=20)
        
        # 4. Merge and Deduplicate
        merged_candidates = {}
        
        for item in vector_results:
            merged_candidates[item["chunk_id"]] = item
            
        for item in keyword_results:
            if item["chunk_id"] not in merged_candidates:
                merged_candidates[item["chunk_id"]] = item
                
        candidate_list = list(merged_candidates.values())
        
        # 5. Cross-Encoder Reranking -> Top 5
        final_results = cross_encoder_service.rerank(query=query, candidates=candidate_list, limit=limit)
        
        return final_results
