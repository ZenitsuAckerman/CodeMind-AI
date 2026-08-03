from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific document's metadata.
    """
    return await DocumentService.get_document(db=db, document_id=document_id, user_id=current_user.id)

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific document.
    """
    await DocumentService.delete_document(db=db, document_id=document_id, user_id=current_user.id)
