import time
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocumentStatus
from app.models.document_content import DocumentContent
from app.services.document_service import DocumentService
from app.services.processing.extractors.extractor_factory import ExtractorFactory

class DocumentProcessingService:
    """
    Coordinates document processing: state management, extraction invocation, and persistence.
    """

    @staticmethod
    async def process_document(db: AsyncSession, document_id: UUID, user_id: UUID) -> None:
        # 1. Fetch document and enforce ownership
        doc = await DocumentService.get_document(db, document_id=document_id, user_id=user_id)
        
        # 2. Check current status
        if doc.status in {DocumentStatus.PROCESSING, DocumentStatus.PROCESSED}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Document is currently {doc.status.value.lower()}."
            )
            
        # 3. Update status to PROCESSING
        doc.status = DocumentStatus.PROCESSING
        db.add(doc)
        await db.commit()
        
        try:
            start_time = time.time()
            
            # 4. Extract Text using Factory
            import os
            ext = os.path.splitext(doc.original_filename)[1]
            extractor = ExtractorFactory.get_extractor(ext)
            content_text = extractor.extract(doc.file_path)
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # 5. Save DocumentContent
            content = DocumentContent(
                document_id=doc.id,
                content=content_text,
                content_type=doc.mime_type,
                language="en", # default language for now
                character_count=len(content_text),
                processing_time_ms=processing_time_ms
            )
            db.add(content)
            
            # 6. Update status to PROCESSED
            doc.status = DocumentStatus.PROCESSED
            db.add(doc)
            
            await db.commit()
            
        except Exception as e:
            # If any failure occurs, mark as FAILED
            doc.status = DocumentStatus.FAILED
            db.add(doc)
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to extract document text: {str(e)}"
            )
