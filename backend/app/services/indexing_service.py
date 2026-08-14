import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.document_service import DocumentService
from app.services.rag.chunking_service import chunking_service
from app.services.rag.embedding_service import embedding_service
from app.services.rag.qdrant_service import qdrant_service

class IndexingService:
    """
    Coordinates the RAG indexing pipeline: chunking, storing in DB, generating embeddings, and storing in Qdrant.
    """

    @staticmethod
    async def index_document(db: AsyncSession, document_id: uuid.UUID, user_id: uuid.UUID) -> None:
        # 1. Enforce ownership and get document
        doc = await DocumentService.get_document(db, document_id=document_id, user_id=user_id)
        
        if doc.status not in {DocumentStatus.PROCESSED}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document must be PROCESSED before indexing. Current status: {doc.status.value}"
            )
            
        # Update status to INDEXING
        doc.status = DocumentStatus.INDEXING
        db.add(doc)
        await db.commit()
        
        try:
            # 2. Get DocumentContent
            # Using async load to get the associated content
            await db.refresh(doc, ["content"])
            if not doc.content:
                raise ValueError("DocumentContent not found for this document.")
                
            # 3. Chunk the text
            chunks_tuple = chunking_service.split_text(doc.content.content)
            
            # Prepare data
            qdrant_payload = []
            db_chunks = []
            
            # Generate embeddings in batch for efficiency
            texts = [c[0] for c in chunks_tuple]
            embeddings = embedding_service.embed_batch(texts)
            
            # 4. Store Chunks in PostgreSQL and prepare Qdrant payload
            for idx, (chunk_text, token_count) in enumerate(chunks_tuple):
                chunk_id = uuid.uuid4()
                
                db_chunk = DocumentChunk(
                    id=chunk_id,
                    document_content_id=doc.content.id,
                    chunk_index=idx,
                    content=chunk_text,
                    token_count=token_count
                )
                db_chunks.append(db_chunk)
                
                qdrant_payload.append({
                    "chunk_id": chunk_id,
                    "project_id": doc.project_id,
                    "document_id": doc.id,
                    "content": chunk_text,
                    "chunk_index": idx,
                    "embedding": embeddings[idx],
                    "source_type": doc.source_type,
                    "repository_id": str(doc.repository_id) if doc.repository_id else None,
                    "repo_file_path": doc.repo_file_path
                })
                
            # Add to PostgreSQL
            db.add_all(db_chunks)
            
            # 5. Store vectors in Qdrant
            qdrant_service.store_chunks(qdrant_payload)
            
            # 6. Update Status to INDEXED
            doc.status = DocumentStatus.INDEXED
            db.add(doc)
            
            await db.commit()
            
        except Exception as e:
            # Revert status to PROCESSED so it can be retried if it failed during indexing
            doc.status = DocumentStatus.FAILED
            db.add(doc)
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to index document: {str(e)}"
            )
