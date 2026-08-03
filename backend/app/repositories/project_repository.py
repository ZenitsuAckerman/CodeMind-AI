from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.base import BaseRepository

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    async def get_all_by_owner(self, db: AsyncSession, owner_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
        result = await db.execute(
            select(Project)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: ProjectCreate, owner_id: UUID) -> Project:
        db_obj = Project(
            owner_id=owner_id,
            name=obj_in.name,
            description=obj_in.description
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Project, obj_in: ProjectUpdate) -> Project:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: UUID) -> Project:
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

project_repository = ProjectRepository(Project)
