import os
import logging
from typing import List
from uuid import UUID
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.repositories.document_repository import document_repository
from app.services.project_service import ProjectService
from app.services.storage_service import StorageService

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".txt", ".md", ".java", 
    ".py", ".js", ".ts", ".json", ".yaml", 
    ".yml", ".xml"
}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

class DocumentService:
    @staticmethod
    async def validate_and_save_file(file: UploadFile) -> tuple[str, str, int, str]:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"File extension '{ext}' is not allowed."
            )
            
        stored_filename, file_path, file_size, file_hash = await StorageService.save_file(file)
        
        if file_size > MAX_FILE_SIZE:
            StorageService.delete_file(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="File size exceeds the 25 MB limit."
            )
            
        return stored_filename, file_path, file_size, file_hash

    @staticmethod
    async def upload_document(db: AsyncSession, project_id: UUID, user_id: UUID, title: str, file: UploadFile) -> Document:
        # Enforce project ownership
        await ProjectService.get_project(db, project_id=project_id, user_id=user_id)
        
        stored_filename, file_path, file_size, file_hash = await DocumentService.validate_and_save_file(file)
        
        doc_data = {
            "title": title,
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_path": file_path,
            "mime_type": file.content_type or "application/octet-stream",
            "file_size": file_size,
            "sha256_hash": file_hash,
            "status": DocumentStatus.UPLOADED
        }
        
        return await document_repository.create_document(db, project_id=project_id, document_data=doc_data)

    @staticmethod
    async def get_project_documents(db: AsyncSession, project_id: UUID, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Document]:
        # Enforce project ownership
        await ProjectService.get_project(db, project_id=project_id, user_id=user_id)
        return await document_repository.get_by_project(db, project_id=project_id, skip=skip, limit=limit)

    @staticmethod
    async def get_document(db: AsyncSession, document_id: UUID, user_id: UUID) -> Document:
        doc = await document_repository.get(db, id=document_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        # Enforce project ownership via the document's project
        await ProjectService.get_project(db, project_id=doc.project_id, user_id=user_id)
        return doc

    @staticmethod
    async def delete_document(db: AsyncSession, document_id: UUID, user_id: UUID) -> None:
        doc = await DocumentService.get_document(db, document_id, user_id)
        
        # Delete vectors from Qdrant first
        from app.services.rag.qdrant_service import qdrant_service
        try:
            qdrant_service.delete_document_vectors(document_id=doc.id, project_id=doc.project_id)
        except Exception as e:
            logger.error(f"Failed to delete Qdrant vectors for document {doc.id}: {e}")
            raise # Fail the deletion if vectors cannot be removed to prevent orphaned data

        # Delete file from local storage
        StorageService.delete_file(doc.file_path)
        # Delete from DB
        await document_repository.delete(db, id=document_id)
