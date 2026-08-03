from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.document import Document
from app.repositories.base import BaseRepository
from app.schemas.document import DocumentBase

class DocumentRepository(BaseRepository[Document, DocumentBase, DocumentBase]):
    async def get_by_project(self, db: AsyncSession, project_id: UUID, skip: int = 0, limit: int = 100) -> List[Document]:
        result = await db.execute(
            select(Document)
            .filter(Document.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_document(self, db: AsyncSession, project_id: UUID, document_data: dict) -> Document:
        db_obj = Document(
            project_id=project_id,
            **document_data
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: UUID) -> Document:
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

document_repository = DocumentRepository(Document)
