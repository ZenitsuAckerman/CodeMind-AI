from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import project_repository

class ProjectService:
    @staticmethod
    async def get_project(db: AsyncSession, project_id: UUID, user_id: UUID) -> Project:
        project = await project_repository.get(db, id=project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return project

    @staticmethod
    async def create_project(db: AsyncSession, project_in: ProjectCreate, user_id: UUID) -> Project:
        return await project_repository.create(db, obj_in=project_in, owner_id=user_id)

    @staticmethod
    async def get_user_projects(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
        return await project_repository.get_all_by_owner(db, owner_id=user_id, skip=skip, limit=limit)

    @staticmethod
    async def update_project(db: AsyncSession, project_id: UUID, project_in: ProjectUpdate, user_id: UUID) -> Project:
        project = await ProjectService.get_project(db, project_id, user_id)
        return await project_repository.update(db, db_obj=project, obj_in=project_in)

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: UUID, user_id: UUID) -> None:
        project = await ProjectService.get_project(db, project_id, user_id)
        await project_repository.delete(db, id=project.id)
